from datetime import datetime, timezone, timedelta

import weaviate

from config import (
    FINANCIAL_NEWS_CLASS,
    MARKET_DATA_CLASS,
    RETRIEVAL_TOP_K,
    NEWS_TIME_RANGE_HOURS,
)
from embeddings.embedding_generator import generate_embedding
from retrieval.query_expander import detect_tickers, expand_query


def retrieve_news(
    client: weaviate.Client,
    query: str,
    top_k: int = RETRIEVAL_TOP_K,
    time_range_hours: int = NEWS_TIME_RANGE_HOURS,
    tickers: list[str] = None,
) -> list[dict]:
    """
    Búsqueda híbrida (vectorial + BM25) sobre FinancialNews
    con filtros opcionales por fecha y ticker.
    """
    expanded = expand_query(query)
    embedding = generate_embedding(expanded)

    cutoff = datetime.now(timezone.utc) - timedelta(hours=time_range_hours)

    # Filtro base: noticias no archivadas dentro del rango temporal
    where_filter = {
        "operator": "And",
        "operands": [
            {
                "path": ["archived"],
                "operator": "Equal",
                "valueBoolean": False,
            },
            {
                "path": ["published_at"],
                "operator": "GreaterThan",
                "valueDate": cutoff.isoformat(),
            },
        ],
    }

    result = (
        client.query
        .get(FINANCIAL_NEWS_CLASS, [
            "title", "content", "source",
            "url", "published_at", "ticker_mentions", "sector",
        ])
        .with_near_vector({"vector": embedding})
        .with_where(where_filter)
        .with_limit(top_k)
        .with_additional(["score", "distance"])
        .do()
    )

    return result.get("data", {}).get("Get", {}).get(FINANCIAL_NEWS_CLASS, [])


def retrieve_market_data(
    client: weaviate.Client,
    tickers: list[str],
) -> list[dict]:
    """
    Recupera los datos de mercado actuales para los tickers detectados.
    """
    if not tickers:
        return []

    results = []
    for ticker in tickers:
        result = (
            client.query
            .get(MARKET_DATA_CLASS, [
                "ticker", "company_name", "price",
                "change_pct", "volume", "summary", "timestamp",
            ])
            .with_where({
                "path": ["ticker"],
                "operator": "Equal",
                "valueText": ticker,
            })
            .with_limit(1)
            .do()
        )
        items = result.get("data", {}).get("Get", {}).get(MARKET_DATA_CLASS, [])
        if items:
            results.append(items[0])

    return results