FINANCIAL_NEWS_SCHEMA = {
    "class": "FinancialNews",
    "description": "Noticias financieras indexadas con embeddings",
    "vectorizer": "none",  # Embeddings generados externamente
    "properties": [
        {"name": "title",            "dataType": ["text"]},
        {"name": "content",          "dataType": ["text"]},
        {"name": "source",           "dataType": ["text"]},
        {"name": "url",              "dataType": ["text"]},
        {"name": "published_at",     "dataType": ["date"]},
        {"name": "ticker_mentions",  "dataType": ["text[]"]},
        {"name": "sector",           "dataType": ["text"]},
        {"name": "content_hash",     "dataType": ["text"]},
        {"name": "archived",         "dataType": ["boolean"]},
    ],
}

MARKET_DATA_SCHEMA = {
    "class": "MarketData",
    "description": "Precios y métricas de mercado por ticker",
    "vectorizer": "none",
    "properties": [
        {"name": "ticker",           "dataType": ["text"]},
        {"name": "company_name",     "dataType": ["text"]},
        {"name": "price",            "dataType": ["number"]},
        {"name": "change_pct",       "dataType": ["number"]},
        {"name": "volume",           "dataType": ["number"]},
        {"name": "market_cap",       "dataType": ["number"]},
        {"name": "summary",          "dataType": ["text"]},
        {"name": "timestamp",        "dataType": ["date"]},
    ],
}

ALL_SCHEMAS = [FINANCIAL_NEWS_SCHEMA, MARKET_DATA_SCHEMA]