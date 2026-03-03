from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage

from config import (
    OPENAI_API_KEY,
    LLM_MODEL,
    LLM_TEMPERATURE,
    LLM_MAX_TOKENS,
)
from llm.prompt_templates import SYSTEM_PROMPT, build_user_prompt
from retrieval.query_expander import detect_tickers, expand_query
from retrieval.retriever import retrieve_news, retrieve_market_data
from retrieval.reranker import rerank, apply_mmr
from retrieval.context_builder import build_context, build_sources
from vectordb.weaviate_client import get_client


llm = ChatOpenAI(
    model=LLM_MODEL,
    temperature=LLM_TEMPERATURE,
    max_tokens=LLM_MAX_TOKENS,
    openai_api_key=OPENAI_API_KEY,
)


def answer_question(
    question: str,
    time_range_hours: int = 24,
) -> dict:
    """
    Flujo completo del sistema RAG con GPT-4o.
    """

    # ── 1. Query expansion ────────────────────────────────
    tickers = detect_tickers(question)
    print(f"   🔍 Tickers detectados: {tickers}")

    # ── 2. Retrieval ──────────────────────────────────────
    client = get_client()

    news_candidates = retrieve_news(
        client=client,
        query=question,
        time_range_hours=time_range_hours,
        tickers=tickers,
    )
    print(f"   📰 {len(news_candidates)} noticias candidatas")

    market_data = retrieve_market_data(
        client=client,
        tickers=tickers,
    )
    print(f"   📈 {len(market_data)} tickers con datos de mercado")

    # ── 3. Reranking + MMR ────────────────────────────────
    reranked = rerank(question, news_candidates)
    final_docs = apply_mmr(reranked)
    print(f"   ✅ {len(final_docs)} documentos finales tras reranking")

    # ── 4. Construcción del contexto ──────────────────────
    context = build_context(final_docs, market_data)
    sources = build_sources(final_docs)

    # ── 5. Generación con GPT-4o ──────────────────────────
    user_prompt = build_user_prompt(question, context)

    messages = [
        SystemMessage(content=SYSTEM_PROMPT),
        HumanMessage(content=user_prompt),
    ]

    response = llm.invoke(messages)

    return {
        "answer":      response.content,
        "sources":     sources,
        "tickers":     tickers,
        "market_data": market_data,
        "docs_used":   len(final_docs),
    }