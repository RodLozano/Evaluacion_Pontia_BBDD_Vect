import re

TICKER_MAP = {
    "tesla": "TSLA",
    "apple": "AAPL",
    "microsoft": "MSFT",
    "google": "GOOGL",
    "alphabet": "GOOGL",
    "amazon": "AMZN",
    "nvidia": "NVDA",
    "meta": "META",
    "facebook": "META",
    "jpmorgan": "JPM",
    "visa": "V",
}

FINANCIAL_SYNONYMS = {
    "falling":  ["dropping", "declining", "down", "sell-off"],
    "rising":   ["gaining", "up", "rally", "surging"],
    "earnings": ["results", "revenue", "profit", "quarterly report"],
    "crash":    ["collapse", "plunge", "correction"],
}


def detect_tickers(text: str) -> list[str]:
    """
    Detecta tickers en el texto, tanto explícitos (TSLA)
    como implícitos por nombre de empresa (Tesla → TSLA).
    """
    tickers = []

    # Tickers explícitos en mayúsculas (ej: TSLA, NVDA)
    explicit = re.findall(r'\b[A-Z]{1,5}\b', text)
    tickers.extend(explicit)

    # Nombres de empresa → ticker
    text_lower = text.lower()
    for name, ticker in TICKER_MAP.items():
        if name in text_lower:
            tickers.append(ticker)

    return list(set(tickers))


def expand_query(query: str) -> str:
    """
    Expande la query original añadiendo sinónimos financieros
    y los tickers detectados para mejorar el retrieval.
    """
    expansions = []
    query_lower = query.lower()

    for term, synonyms in FINANCIAL_SYNONYMS.items():
        if term in query_lower:
            expansions.extend(synonyms)

    tickers = detect_tickers(query)

    expanded = query
    if tickers:
        expanded += " " + " ".join(tickers)
    if expansions:
        expanded += " " + " ".join(expansions[:3])  # Máximo 3 sinónimos

    return expanded