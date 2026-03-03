from datetime import datetime


def build_context(
    news_docs: list[dict],
    market_data: list[dict],
) -> str:
    """
    Construye el bloque de contexto que se enviará al LLM,
    combinando noticias relevantes y datos de mercado actuales.
    """
    sections = []

    # ── Datos de mercado ──────────────────────────────────
    if market_data:
        sections.append("## Market Data (current prices)\n")
        for item in market_data:
            change_sign = "+" if item.get("change_pct", 0) >= 0 else ""
            sections.append(
                f"**{item['ticker']} — {item.get('company_name', '')}**\n"
                f"Price: ${item.get('price', 'N/A')} "
                f"({change_sign}{item.get('change_pct', 0):.2f}%)\n"
                f"Volume: {item.get('volume', 'N/A'):,}\n"
            )

    # ── Noticias relevantes ───────────────────────────────
    if news_docs:
        sections.append("\n## Relevant News\n")
        for i, doc in enumerate(news_docs, 1):
            published = doc.get("published_at", "")[:10]
            sections.append(
                f"[{i}] **{doc.get('title', 'No title')}**\n"
                f"Source: {doc.get('source', 'unknown')} | Date: {published}\n"
                f"URL: {doc.get('url', '')}\n"
                f"{doc.get('content', '')[:400]}...\n"
            )

    if not sections:
        return "No relevant information found for this query."

    return "\n".join(sections)


def build_sources(news_docs: list[dict]) -> list[dict]:
    """
    Construye la lista de fuentes para incluir en la respuesta final.
    """
    return [
        {
            "title":        doc.get("title", ""),
            "source":       doc.get("source", ""),
            "published_at": doc.get("published_at", ""),
            "url":          doc.get("url", ""),
        }
        for doc in news_docs
    ]