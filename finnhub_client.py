import os
import requests
from dotenv import load_dotenv
from datetime import datetime, timedelta


load_dotenv()  # reads your .env file and loads its key=value pairs into environment variables

API_KEY = os.getenv("FINNHUB_API_KEY")  # pulls the key from env vars — never hardcoded here
BASE_URL = "https://finnhub.io/api/v1"

def get_quote(ticker):
    """
    Fetch current price data for a given stock ticker.
    """
    url = f"{BASE_URL}/quote"
    params = {
        "symbol": ticker,
        "token": API_KEY
    }
    
    response = requests.get(url, params=params)
    
    if response.status_code != 200:
        raise Exception(f"Finnhub API error {response.status_code}: {response.text}")
    
    data = response.json()

    if data.get("c") == 0:
        raise Exception(f"No data found for ticker '{ticker}' — check the symbol is correct.")

    return data


def get_fundamentals(ticker):
    """
    Fetch a curated set of fundamental metrics for a given stock ticker.
    """
    url = f"{BASE_URL}/stock/metric"
    params = {
        "symbol": ticker,
        "token": API_KEY,
        "metric": "all"
    }
    response = requests.get(url, params=params)
    if response.status_code != 200:
        raise Exception(f"Finnhub API error {response.status_code}: {response.text}")
    data = response.json()
    all_metrics = data["metric"]

    curated = {
        "pe_ratio": all_metrics.get("peTTM"),
        "market_cap": all_metrics.get("marketCapitalization"),
        "52_week_high": all_metrics.get("52WeekHigh"),
        "52_week_low": all_metrics.get("52WeekLow"),
        "dividend_yield": round(all_metrics.get("dividendYieldIndicatedAnnual"), 2) if all_metrics.get("dividendYieldIndicatedAnnual") else None,
        "eps": all_metrics.get("epsTTM"),
        "beta": all_metrics.get("beta"),
    }
    return curated

def get_news(ticker, days_back=7, limit=5):
    """
    Fetch recent company news for a given stock ticker, curated to key fields.
    """
    today = datetime.now()
    week_ago = today - timedelta(days=days_back)
    to_date = today.strftime("%Y-%m-%d")
    from_date = week_ago.strftime("%Y-%m-%d")
    url = f"{BASE_URL}/company-news"
    params = {
        "symbol": ticker,
        "from": from_date,
        "to": to_date,
        "token": API_KEY
    }
    response = requests.get(url, params=params)
    if response.status_code != 200:
        raise Exception(f"Finnhub API error {response.status_code}: {response.text}")
    data = response.json()

    curated_news = []
    for article in data[:limit]:
        curated_news.append({
            "headline": article.get("headline"),
            "summary": article.get("summary"),
            "source": article.get("source"),
            "datetime": article.get("datetime"),
            "url": article.get("url"),
        })
    return curated_news

if __name__ == "__main__":
    result = get_quote("AAPL")
    print(result)
    print(datetime.fromtimestamp(result["t"]))

    fundamentals = get_fundamentals("AAPL")
    print(fundamentals)

    print(datetime.now().strftime("%Y-%m-%d"))

    news = get_news("AAPL")
    print(len(news))
    for article in news:
        print(article)