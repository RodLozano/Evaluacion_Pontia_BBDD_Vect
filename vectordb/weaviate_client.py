import weaviate
from config import WEAVIATE_URL
from vectordb.schema import ALL_SCHEMAS


def get_client() -> weaviate.Client:
    """Devuelve un cliente conectado a Weaviate."""
    client = weaviate.Client(url=WEAVIATE_URL)
    if not client.is_ready():
        raise ConnectionError(f"Weaviate no está disponible en {WEAVIATE_URL}")
    return client


def init_schema(client: weaviate.Client) -> None:
    """Crea las clases en Weaviate si no existen."""
    existing = [c["class"] for c in client.schema.get()["classes"]]
    
    for schema in ALL_SCHEMAS:
        if schema["class"] not in existing:
            client.schema.create_class(schema)
            print(f"✅ Clase '{schema['class']}' creada")
        else:
            print(f"ℹ️  Clase '{schema['class']}' ya existe")


if __name__ == "__main__":
    client = get_client()
    init_schema(client)