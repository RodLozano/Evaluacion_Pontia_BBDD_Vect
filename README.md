# Financial RAG — Sistema de Preguntas sobre Noticias Financieras y Precios de Acciones

Sistema de Retrieval-Augmented Generation (RAG) que permite hacer preguntas en lenguaje natural sobre noticias financieras y precios de acciones en tiempo real. El sistema combina una base de datos vectorial (Weaviate) con el modelo de lenguaje Claude de Anthropic para generar respuestas fundamentadas y con fuentes citadas.

---

## ¿Qué hace este sistema?

El sistema responde preguntas como:

- *"¿Por qué está cayendo Tesla hoy?"*
- *"¿Cuál es el sentimiento del mercado sobre Nvidia tras sus últimos resultados?"*
- *"¿Qué noticias han afectado al sector bancario esta semana?"*

Para ello, recupera en tiempo real las noticias más relevantes y el precio actualizado del activo mencionado, construye un contexto y genera una respuesta mediante Claude, citando siempre las fuentes utilizadas.

---

## Arquitectura resumida

```
Fuentes de datos (NewsAPI, Yahoo Finance)
        ↓
Ingesta y normalización (dos pipelines)
        ↓
Generación de embeddings (text-embedding-3-large)
        ↓
Base de datos vectorial (Weaviate)
        ↓
Retrieval híbrido + Reranking
        ↓
Claude claude-sonnet-4-20250514 → Respuesta con fuentes
        ↓
API REST (FastAPI)
```

La ingesta funciona en segundo plano de forma continua: las noticias se actualizan cada 15 minutos y los precios cada minuto.

---

## Requisitos previos

- Python 3.10 o superior
- Docker y Docker Compose (para levantar Weaviate localmente)
- Cuentas y API keys en: OpenAI, Anthropic, NewsAPI y Alpaca Markets

---

## Instalación

### 1. Clonar el repositorio

```bash
git clone https://github.com/tu-usuario/financial-rag.git
cd financial-rag
```

### 2. Crear el entorno virtual e instalar dependencias

```bash
python -m venv venv
source venv/bin/activate        # En Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Configurar las variables de entorno

```bash
cp .env.example .env
```

Edita el fichero `.env` y rellena tus credenciales:

```
OPENAI_API_KEY=sk-...
ANTHROPIC_API_KEY=sk-ant-...
WEAVIATE_URL=http://localhost:8080
NEWSAPI_KEY=...
ALPACA_API_KEY=...
ALPACA_SECRET_KEY=...
```

### 4. Levantar Weaviate con Docker

```bash
docker compose up -d
```

Weaviate estará disponible en `http://localhost:8080`. Puedes verificarlo en `http://localhost:8080/v1/.well-known/ready`.

### 5. Inicializar el esquema de la base de datos vectorial

```bash
python -m vectordb.schema
```

Esto crea las clases `FinancialNews` y `MarketData` en Weaviate.

---

## Ejecución

### Arrancar el pipeline de ingesta (en segundo plano)

```bash
python -m ingestion.scheduler
```

Este proceso lanza automáticamente los dos pipelines: noticias cada 15 minutos y precios cada minuto. Se recomienda dejarlo corriendo en una terminal separada o como servicio.

### Arrancar la API

```bash
uvicorn api.main:app --reload --port 8000
```

La API estará disponible en `http://localhost:8000`. La documentación interactiva en `http://localhost:8000/docs`.

---

## Uso de la API

### Endpoint principal

```
POST /query
```

**Request:**

```json
{
  "question": "¿Por qué está cayendo Tesla hoy?",
  "time_range_hours": 24
}
```

**Response:**

```json
{
  "answer": "Tesla ha caído un 4.2% hoy debido a...",
  "sources": [
    {
      "title": "Tesla misses delivery estimates for Q2",
      "source": "Reuters",
      "published_at": "2025-03-01T09:30:00Z",
      "url": "https://..."
    }
  ],
  "ticker": "TSLA",
  "current_price": 182.45
}
```

---

## Tests

```bash
pytest tests/
```

---

## Estructura del proyecto

```
financial-rag/
├── ingestion/        # Pipelines de noticias y precios
├── embeddings/       # Generación de embeddings
├── vectordb/         # Cliente y operaciones sobre Weaviate
├── retrieval/        # Búsqueda, reranking y construcción de contexto
├── llm/              # Integración con Claude vía LangChain
├── api/              # API REST con FastAPI
└── tests/            # Tests unitarios
```

---

## Notas

- El sistema solo ingiere noticias en inglés por defecto. Para añadir fuentes en español, configura los parámetros de idioma en `config/settings.py`.
- Las noticias con más de 30 días se archivan automáticamente y no aparecen en los resultados de búsqueda, pero no se eliminan físicamente.
- Los costes principales del sistema provienen de las llamadas a la API de OpenAI (embeddings) y Anthropic (generación). Se recomienda monitorizar el uso en entornos de producción.
