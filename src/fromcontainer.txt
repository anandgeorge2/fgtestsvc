from fastapi import FastAPI, HTTPException, Response, Request, APIRouter
import os
from datetime import datetime
import aiohttp
import time
import uvicorn
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST
import structlog
from cachetools import TTLCache
from tenacity import retry, stop_after_attempt, wait_exponential
import logging
from contextlib import asynccontextmanager

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = structlog.get_logger()

# Initialize metrics
REQUEST_COUNT = Counter('http_requests_total', 'Total HTTP requests')
REQUEST_LATENCY = Histogram('http_request_duration_seconds', 'HTTP request latency')
API_ERRORS = Counter('external_api_errors_total', 'External API errors')

# Initialize cache with 5-minute TTL
price_cache = TTLCache(maxsize=100, ttl=300)

# Create routers
system_router = APIRouter(tags=["System"])

@system_router.get("/health")
async def health_check():
    """Health check endpoint for kubernetes liveness probe"""
    logger.debug("health_check_called")
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat()
    }

@system_router.get("/ready")
async def readiness_check():
    """Readiness check endpoint for kubernetes readiness probe"""
    logger.debug("readiness_check_called")
    return {
        "status": "ready",
        "timestamp": datetime.utcnow().isoformat()
    }

@system_router.get("/metrics")
async def metrics():
    """Prometheus metrics endpoint"""
    logger.debug("metrics_called")
    return Response(
        generate_latest(),
        media_type=CONTENT_TYPE_LATEST
    )

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Initialize any resources on startup"""
    logger.info("application_starting")
    yield
    logger.info("application_stopping")

# Create FastAPI app with explicit routes for OpenAPI docs
app = FastAPI(
    title="Stock Price Service",
    description="A service to fetch and analyze stock prices",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
    lifespan=lifespan
)

# Add middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(GZipMiddleware)

# Include routers
app.include_router(system_router)

# Configuration
API_KEY = os.getenv("APIKEY", "C227WD9W3LUVKVV9")
BASE_URL = "https://www.alphavantage.co/query"
SYMBOL = os.getenv("SYMBOL", "MSFT")
NDAYS = int(os.getenv("NDAYS", 5))
REQUEST_TIMEOUT = int(os.getenv("REQUEST_TIMEOUT", 10))

@app.get("/", tags=["System"])
async def root():
    """Root endpoint showing application status and available routes"""
    routes = [
        {"path": route.path, "name": route.name, "methods": route.methods}
        for route in app.routes
    ]
    return {
        "status": "running",
        "timestamp": datetime.utcnow().isoformat(),
        "routes": routes
    }

@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=4, max=10),
    reraise=True
)
async def fetch_stock_data(symbol: str) -> dict:
    cache_key = f"{symbol}_{datetime.now().date()}"
    if cache_key in price_cache:
        logger.info("cache_hit", symbol=symbol)
        return price_cache[cache_key]

    async with aiohttp.ClientSession() as session:
        try:
            params = {
                "apikey": API_KEY,
                "function": "TIME_SERIES_DAILY",
                "symbol": symbol
            }
            async with session.get(BASE_URL, params=params, timeout=REQUEST_TIMEOUT) as response:
                response.raise_for_status()
                data = await response.json()

                if not data or "Time Series (Daily)" not in data:
                    API_ERRORS.inc()
                    logger.error("api_call_failed", symbol=symbol, error="Invalid response format")
                    raise HTTPException(status_code=400, detail="Invalid response from API: 'Time Series (Daily)' not found")

                price_cache[cache_key] = data
                logger.info("api_call_success", symbol=symbol)
                return data
        except aiohttp.ClientError as e:
            API_ERRORS.inc()
            logger.error("api_call_failed", symbol=symbol, error=str(e))
            raise HTTPException(status_code=503, detail=f"Error fetching data from API: {str(e)}")
        except Exception as e:
            if isinstance(e, HTTPException):
                raise
            API_ERRORS.inc()
            logger.error("api_call_failed", symbol=symbol, error=str(e))
            raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {str(e)}")

@app.get("/stock-prices")
async def get_stock_prices(request: Request):
    request_start = time.time()
    REQUEST_COUNT.inc()
    
    try:
        data = await fetch_stock_data(SYMBOL)
        time_series = data["Time Series (Daily)"]
        closing_prices = []

        for date, metrics in sorted(time_series.items(), reverse=True)[:NDAYS]:
            closing_prices.append({"date": date, "closing_price": float(metrics["4. close"])})

        if not closing_prices:
            raise ValueError("No closing prices available for the given symbol and days")

        average_price = sum(item["closing_price"] for item in closing_prices) / len(closing_prices)

        result = {
            "symbol": SYMBOL,
            "ndays": NDAYS,
            "closing_prices": closing_prices,
            "average_closing_price": average_price
        }

        request_duration = time.time() - request_start
        REQUEST_LATENCY.observe(request_duration)
        
        logger.info(
            "request_processed",
            symbol=SYMBOL,
            ndays=NDAYS,
            duration=request_duration
        )
        
        return result

    except Exception as e:
        if isinstance(e, HTTPException):
            raise
        logger.error("unexpected_error", error=str(e))
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {str(e)}")