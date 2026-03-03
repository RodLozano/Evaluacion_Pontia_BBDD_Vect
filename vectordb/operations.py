import hashlib
from datetime import datetime, timezone, timedelta
from typing import Optional
import weaviate

from config import (
    FINANCIAL_NEWS_CLASS,
    MARKET_DATA_CLASS,
    NEWS_ARCHIVE_DAYS,
)


# ── FinancialNews ──────────────────────────────────────────

def compute_hash(title: str, content: str) -> str:
    """Calcula el hash SHA-256 de un artículo."""
    return hashlib.sha256(f"{title}{content}".encode()).hexdigest()


def news_hash_exists(client: weaviate.Client, content_hash: str) -> bool:
    """Comprueba si un artículo con ese hash ya está en Weaviate."""
    result = (
        client.query
        .get(FINANCIAL_NEWS_CLASS, ["content_hash"])
        .with_where({
            "path": ["content_hash"],
            "operator": "Equal",
            "valueText": content_hash,
        })
        .with_limit(1)
        .do()
    )
    items = result.get("data", {}).get("Get", {}).get(FINANCIAL_NEWS_CLASS, [])
    return len(items) > 0


def insert_news(client: weaviate.Client, article: dict, embedding: list) -> None:
    """Inserta un artículo nuevo en Weaviate."""
    client.data_object.create(
        data_object=article,
        class_name=FINANCIAL_NEWS_CLASS,
        vector=embedding,
    )


def delete_news_by_url(client: weaviate.Client, url: str) -> None:
    """Elimina un artículo por URL (para actualizaciones)."""
    client.batch.delete_objects(
        class_name=FINANCIAL_NEWS_CLASS,
        where={
            "path": ["url"],
            "operator": "Equal",
            "valueText": url,
        },
    )


def archive_old_news(client: weaviate.Client) -> int:
    """Marca como archived=True las noticias con más de NEWS_ARCHIVE_DAYS días."""
    cutoff = datetime.now(timezone.utc) - timedelta(days=NEWS_ARCHIVE_DAYS)
    
    result = (
        client.query
        .get(FINANCIAL_NEWS_CLASS, ["_additional { id }"])
        .with_where({
            "path": ["published_at"],
            "operator": "LessThan",
            "valueDate": cutoff.isoformat(),
        })
        .do()
    )
    
    items = result.get("data", {}).get("Get", {}).get(FINANCIAL_NEWS_CLASS, [])
    
    for item in items:
        client.data_object.update(
            data_object={"archived": True},
            class_name=FINANCIAL_NEWS_CLASS,
            uuid=item["_additional"]["id"],
        )
    
    return len(items)


# ── MarketData ─────────────────────────────────────────────

def upsert_market_data(client: weaviate.Client, data: dict, embedding: list) -> None:
    """Inserta o actualiza el documento de precio de un ticker."""
    # Buscar si ya existe el ticker
    result = (
        client.query
        .get(MARKET_DATA_CLASS, ["_additional { id }"])
        .with_where({
            "path": ["ticker"],
            "operator": "Equal",
            "valueText": data["ticker"],
        })
        .with_limit(1)
        .do()
    )
    
    items = result.get("data", {}).get("Get", {}).get(MARKET_DATA_CLASS, [])
    
    if items:
        # Actualizar el documento existente
        uuid = items[0]["_additional"]["id"]
        client.data_object.update(
            data_object=data,
            class_name=MARKET_DATA_CLASS,
            uuid=uuid,
            vector=embedding,
        )
    else:
        # Insertar nuevo
        client.data_object.create(
            data_object=data,
            class_name=MARKET_DATA_CLASS,
            vector=embedding,
        )