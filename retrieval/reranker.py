from sentence_transformers import CrossEncoder
from config import RERANKER_MODEL, RERANKER_TOP_K

# Cargamos el modelo una sola vez al importar el módulo
_reranker = None


def get_reranker() -> CrossEncoder:
    global _reranker
    if _reranker is None:
        _reranker = CrossEncoder(RERANKER_MODEL)
    return _reranker


def rerank(query: str, documents: list[dict]) -> list[dict]:
    """
    Reordena los documentos por relevancia real query-documento
    usando un CrossEncoder.
    """
    if not documents:
        return []

    reranker = get_reranker()

    # Pares (query, texto_documento) para el CrossEncoder
    pairs = [(query, f"{d.get('title', '')}. {d.get('content', '')}") for d in documents]
    scores = reranker.predict(pairs)

    # Añadir score a cada documento y ordenar
    scored = sorted(
        zip(scores, documents),
        key=lambda x: x[0],
        reverse=True,
    )

    return [doc for _, doc in scored[:RERANKER_TOP_K]]


def apply_mmr(
    documents: list[dict],
    top_k: int = RERANKER_TOP_K,
    diversity: float = 0.3,
) -> list[dict]:
    """
    Maximal Marginal Relevance: selecciona documentos
    balanceando relevancia y diversidad para evitar redundancia.
    diversity=0.0 → máxima relevancia
    diversity=1.0 → máxima diversidad
    """
    if len(documents) <= top_k:
        return documents

    selected = [documents[0]]
    remaining = documents[1:]

    while len(selected) < top_k and remaining:
        best_score = -1
        best_doc = None

        for doc in remaining:
            # Relevancia: posición inversa en la lista (ya ordenada por reranker)
            relevance = 1.0 / (remaining.index(doc) + 1)

            # Diversidad: penalizar si el sector ya está cubierto
            sectors_selected = {d.get("sector") for d in selected}
            redundancy = 1.0 if doc.get("sector") in sectors_selected else 0.0

            score = (1 - diversity) * relevance - diversity * redundancy

            if score > best_score:
                best_score = score
                best_doc = doc

        if best_doc:
            selected.append(best_doc)
            remaining.remove(best_doc)

    return selected