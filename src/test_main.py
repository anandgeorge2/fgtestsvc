import pytest
from fastapi.testclient import TestClient
from main import app, price_cache
import aiohttp
from datetime import datetime

client = TestClient(app)

def mock_alphavantage_response():
    return {
        "Time Series (Daily)": {
            "2025-04-16": {"4. close": "300.00"},
            "2025-04-15": {"4. close": "310.00"},
            "2025-04-14": {"4. close": "320.00"},
            "2025-04-13": {"4. close": "330.00"},
            "2025-04-12": {"4. close": "340.00"},
        }
    }

class MockResponse:
    def __init__(self, json_data, status_code=200):
        self.json_data = json_data
        self.status = status_code
    
    async def json(self):
        return self.json_data
        
    async def __aenter__(self):
        return self
        
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        pass
        
    def raise_for_status(self):
        if self.status != 200:
            raise aiohttp.ClientError(f"HTTP {self.status}")

class MockClientSession:
    def __init__(self, mock_response):
        self.mock_response = mock_response
    
    async def __aenter__(self):
        return self
        
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        pass
        
    def get(self, *args, **kwargs):
        return self.mock_response

@pytest.fixture(autouse=True)
def clear_cache():
    price_cache.clear()
    yield

@pytest.fixture
def mock_aiohttp_get(monkeypatch):
    def mock_client_session(*args, **kwargs):
        mock_response = MockResponse(mock_alphavantage_response())
        return MockClientSession(mock_response)
    monkeypatch.setattr("aiohttp.ClientSession", mock_client_session)

def test_get_stock_prices_success(mock_aiohttp_get):
    response = client.get("/stock-prices")
    assert response.status_code == 200
    data = response.json()
    assert data["symbol"] == "MSFT"
    assert data["ndays"] == 5
    assert len(data["closing_prices"]) == 5
    assert data["average_closing_price"] == 320.0

def test_get_stock_prices_api_error(monkeypatch):
    def mock_client_session(*args, **kwargs):
        mock_response = MockResponse({}, status_code=503)
        return MockClientSession(mock_response)
    monkeypatch.setattr("aiohttp.ClientSession", mock_client_session)

    response = client.get("/stock-prices")
    assert response.status_code == 503
    assert "Error fetching data from API" in response.json()["detail"]

def test_get_stock_prices_invalid_response(monkeypatch):
    def mock_client_session(*args, **kwargs):
        mock_response = MockResponse({})
        return MockClientSession(mock_response)
    monkeypatch.setattr("aiohttp.ClientSession", mock_client_session)

    response = client.get("/stock-prices")
    assert response.status_code == 400
    assert "Invalid response from API" in response.json()["detail"]

def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert "timestamp" in data

def test_readiness_check():
    response = client.get("/ready")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ready"
    assert "timestamp" in data

def test_metrics_endpoint():
    response = client.get("/metrics")
    assert response.status_code == 200
    assert response.headers["content-type"] == "text/plain; version=0.0.4; charset=utf-8"
    # Verify that our custom metrics are present in the response
    metrics_text = response.text
    assert "http_requests_total" in metrics_text
    assert "http_request_duration_seconds" in metrics_text
    assert "external_api_errors_total" in metrics_text