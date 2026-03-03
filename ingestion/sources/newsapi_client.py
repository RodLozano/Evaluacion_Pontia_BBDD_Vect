import requests
from config import NEWSAPI_KEY

BASE_URL = "https://newsapi.org/v2/everything"

FINANCIAL_QUERIES = [
    "stock market",
    "earnings report",
    "federal reserve",
    "cryptocurrency",
    "nasdaq nyse",
]


def fetch_news(query: str, page_size: int = 20) -> list[dict]:
    """Fetcha artículos de NewsAPI para una query dada."""
    params = {
        "q": query,
        "language": "en",
        "sortBy": "publishedAt",
        "pageSize": page_size,
        "apiKey": NEWSAPI_KEY,
    }
    response = requests.get(BASE_URL, params=params, timeout=10)
    response.raise_for_status()
    return response.json().get("articles", [])


def fetch_all_financial_news() -> list[dict]:
    """Fetcha noticias para todas las queries financieras definidas."""
    all_articles = []
    for query in FINANCIAL_QUERIES:
        try:
            articles = fetch_news(query)
            all_articles.extend(articles)
        except Exception as e:
            print(f"⚠️  Error fetching '{query}': {e}")
    return all_articles