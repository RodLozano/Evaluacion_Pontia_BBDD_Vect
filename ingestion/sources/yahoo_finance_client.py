import yfinance as yf
from datetime import datetime, timezone

TICKERS_TO_TRACK = [
    "AAPL", "MSFT", "GOOGL", "AMZN", "NVDA",
    "TSLA", "META", "BRK-B", "JPM", "V",
]


def fetch_ticker_data(ticker: str) -> dict | None:
    """Fetcha el precio y métricas actuales de un ticker."""
    try:
        stock = yf.Ticker(ticker)
        info = stock.info

        price = info.get("currentPrice") or info.get("regularMarketPrice")
        prev_close = info.get("previousClose") or info.get("regularMarketPreviousClose")
        change_pct = ((price - prev_close) / prev_close * 100) if price and prev_close else 0.0

        return {
            "ticker": ticker,
            "company_name": info.get("longName", ticker),
            "price": round(price, 4) if price else 0.0,
            "change_pct": round(change_pct, 4),
            "volume": info.get("volume", 0),
            "market_cap": info.get("marketCap", 0),
            "summary": info.get("longBusinessSummary", "")[:500],
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as e:
        print(f"⚠️  Error fetching {ticker}: {e}")
        return None


def fetch_all_tickers() -> list[dict]:
    """Fetcha datos para todos los tickers configurados."""
    results = []
    for ticker in TICKERS_TO_TRACK:
        data = fetch_ticker_data(ticker)
        if data:
            results.append(data)
    return results