import os
from dotenv import load_dotenv

load_dotenv()

# ── API Keys ──────────────────────────────────────────────
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
NEWSAPI_KEY = os.getenv("NEWSAPI_KEY")
ALPACA_API_KEY = os.getenv("ALPACA_API_KEY")
ALPACA_SECRET_KEY = os.getenv("ALPACA_SECRET_KEY")

# ── Weaviate ───────────────────────────────────────────────
WEAVIATE_URL = os.getenv("WEAVIATE_URL", "http://localhost:8080")

# ── Embedding Model ────────────────────────────────────────
EMBEDDING_MODEL = "text-embedding-3-large"
EMBEDDING_DIMENSIONS = 1536

# ── LLM ───────────────────────────────────────────────────
LLM_MODEL = "claude-sonnet-4-20250514"
LLM_TEMPERATURE = 0.2
LLM_MAX_TOKENS = 1024

# ── Retrieval ─────────────────────────────────────────────
RETRIEVAL_TOP_K = 8           # Candidatos iniciales
RERANKER_TOP_K = 4            # Documentos finales tras reranking
RERANKER_MODEL = "cross-encoder/ms-marco-MiniLM-L-6-v2"
NEWS_TIME_RANGE_HOURS = 24    # Ventana temporal por defecto

# ── Ingesta ───────────────────────────────────────────────
NEWS_FETCH_INTERVAL_MINUTES = 15
PRICE_FETCH_INTERVAL_SECONDS = 60
NEWS_ARCHIVE_DAYS = 30        # Días antes de archivar una noticia

# ── Weaviate Classes ───────────────────────────────────────
FINANCIAL_NEWS_CLASS = "FinancialNews"
MARKET_DATA_CLASS = "MarketData"