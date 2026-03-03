from ingestion.sources.newsapi_client import fetch_all_financial_news
from ingestion.normalizer import normalize_article
from vectordb.weaviate_client import get_client
from vectordb.operations import (
    news_hash_exists,
    insert_news,
    delete_news_by_url,
)
from embeddings.embedding_generator import (
    generate_embeddings_batch,
    text_for_news,
)


def run_news_pipeline() -> None:
    """
    Pipeline A: fetcha noticias, deduplica,
    genera embeddings e inserta en Weaviate.
    """
    print("🔄 Iniciando pipeline de noticias...")
    client = get_client()

    raw_articles = fetch_all_financial_news()
    print(f"   {len(raw_articles)} artículos fetchados")

    # Normalizar y filtrar artículos sin contenido
    normalized = [normalize_article(a) for a in raw_articles]
    normalized = [a for a in normalized if a is not None]

    # Separar nuevos vs duplicados
    new_articles = []
    for article in normalized:
        if not news_hash_exists(client, article["content_hash"]):
            new_articles.append(article)

    print(f"   {len(new_articles)} artículos nuevos a indexar")

    if not new_articles:
        print("   ✅ Sin novedades")
        return

    # Generar embeddings en batch
    texts = [text_for_news(a) for a in new_articles]
    embeddings = generate_embeddings_batch(texts)

    # Insertar en Weaviate
    for article, embedding in zip(new_articles, embeddings):
        # Si la URL ya existe con distinto hash → actualizar
        delete_news_by_url(client, article["url"])
        insert_news(client, article, embedding)

    print(f"   ✅ {len(new_articles)} artículos indexados")