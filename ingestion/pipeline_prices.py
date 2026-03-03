from ingestion.sources.yahoo_finance_client import fetch_all_tickers
from vectordb.weaviate_client import get_client
from vectordb.operations import upsert_market_data
from embeddings.embedding_generator import (
    generate_embeddings_batch,
    text_for_market_data,
)


def run_prices_pipeline() -> None:
    """
    Pipeline B: fetcha precios actuales de todos
    los tickers y hace upsert en Weaviate.
    """
    print("🔄 Iniciando pipeline de precios...")
    client = get_client()

    tickers_data = fetch_all_tickers()
    print(f"   {len(tickers_data)} tickers fetchados")

    if not tickers_data:
        print("   ⚠️  Sin datos de mercado")
        return

    # Generar embeddings en batch
    texts = [text_for_market_data(d) for d in tickers_data]
    embeddings = generate_embeddings_batch(texts)

    # Upsert en Weaviate
    for data, embedding in zip(tickers_data, embeddings):
        upsert_market_data(client, data, embedding)

    print(f"   ✅ {len(tickers_data)} tickers actualizados")