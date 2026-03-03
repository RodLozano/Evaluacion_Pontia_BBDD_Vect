from openai import OpenAI
from config import OPENAI_API_KEY, EMBEDDING_MODEL

client = OpenAI(api_key=OPENAI_API_KEY)


def generate_embedding(text: str) -> list[float]:
    """Genera el embedding de un único texto."""
    text = text.replace("\n", " ").strip()
    response = client.embeddings.create(
        input=[text],
        model=EMBEDDING_MODEL,
    )
    return response.data[0].embedding


def generate_embeddings_batch(texts: list[str]) -> list[list[float]]:
    """
    Genera embeddings para una lista de textos en una sola llamada a la API.
    Más eficiente que llamar generate_embedding() en bucle.
    """
    texts = [t.replace("\n", " ").strip() for t in texts]
    response = client.embeddings.create(
        input=texts,
        model=EMBEDDING_MODEL,
    )
    # Devolver en el mismo orden que la entrada
    return [item.embedding for item in sorted(response.data, key=lambda x: x.index)]


def text_for_news(article: dict) -> str:
    """
    Construye el texto que se va a embeddear para una noticia.
    Combinar título + contenido da mejores embeddings que solo el título.
    """
    return f"{article.get('title', '')}. {article.get('content', '')}"


def text_for_market_data(data: dict) -> str:
    """
    Construye el texto que se va a embeddear para un dato de mercado.
    """
    return (
        f"{data.get('ticker')} {data.get('company_name')}. "
        f"Precio actual: {data.get('price')} USD. "
        f"Variación: {data.get('change_pct')}%. "
        f"{data.get('summary', '')}"
    )