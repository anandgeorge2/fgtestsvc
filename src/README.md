from fastapi import FastAPI, HTTPException
import os
import requestsPI-based web service that fetches the last NDAYS of closing prices for a specific stock symbol and calculates the average closing price.

app = FastAPI()s

API_KEY = "C227WD9W3LUVKVV9"ystem
BASE_URL = "https://www.alphavantage.co/query" provided but may expire)

SYMBOL = os.getenv("SYMBOL", "MSFT")
NDAYS = int(os.getenv("NDAYS", 5))
- `SYMBOL`: The stock symbol to look up (default: `MSFT`)
@app.get("/stock-prices")days to fetch data for (default: `5`)
def get_stock_prices():
    try:un the Docker Image
        params = {
            "apikey": API_KEY,
            "function": "TIME_SERIES_DAILY",
            "symbol": SYMBOLcker build -t stock-ticker .
        }
        response = requests.get(BASE_URL, params=params)
        response.raise_for_status()  # Raise an HTTPError for bad responses (4xx and 5xx)2. Run the Docker container:
        data = response.json()
tock-ticker
        if "Time Series (Daily)" not in data:   ```
            raise ValueError("Invalid response from API: 'Time Series (Daily)' not found")
ce at `http://localhost:8000/stock-prices`.
        time_series = data["Time Series (Daily)"]
        closing_prices = []

        for date, metrics in sorted(time_series.items(), reverse=True)[:NDAYS]:- `GET /stock-prices`: Returns the last NDAYS of closing prices and their average for the specified stock symbol.            closing_prices.append({"date": date, "closing_price": float(metrics["4. close"])})        if not closing_prices:            raise ValueError("No closing prices available for the given symbol and days")        average_price = sum(item["closing_price"] for item in closing_prices) / len(closing_prices)        return {
            "symbol": SYMBOL,
            "ndays": NDAYS,
            "closing_prices": closing_prices,
            "average_closing_price": average_price
        }

    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=503, detail=f"Error fetching data from API: {str(e)}")
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {str(e)}")