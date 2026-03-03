import hashlib
import re
from datetime import datetime, timezone

TICKER_PATTERN = re.compile(r'\b([A-Z]{1,5})\b')

KNOWN_TICKERS = {
    "AAPL", "MSFT", "GOOGL", "AMZN", "NVDA",
    "TSLA", "META", "JPM", "V", "BRK",
}

SECTOR_KEYWORDS = {
    "technology": ["software", "chip", "semiconductor", "ai", "cloud", "tech"],
    "finance":    ["bank", "fed", "interest rate", "lending", "credit", "hedge fund"],
    "energy":     ["oil", "gas", "renewable", "solar", "energy"],
    "healthcare": ["pharma", "drug", "fda", "biotech", "clinical"],
    "crypto":     ["bitcoin", "ethereum", "crypto", "blockchain", "defi"],
}


def compute_hash(title: str, content: str) -> str:
    """SHA-256 del título + contenido."""
    return hashlib.sha256(f"{title}{content}".encode()).hexdigest()


def extract_tickers(text: str) -> list[str]:
    """Extrae tickers conocidos mencionados en el texto."""
    matches = TICKER_PATTERN.findall(text)
    return list({m for m in matches if m in KNOWN_TICKERS})


def classify_sector(text: str) -> str:
    """Clasifica el texto en un sector financiero."""
    text_lower = text.lower()
    for sector, keywords in SECTOR_KEYWORDS.items():
        if any(kw in text_lower for kw in keywords):
            return sector
    return "general"


def normalize_article(raw: dict) -> dict | None:
    """
    Transforma un artículo crudo de NewsAPI al formato
    que espera Weaviate (FinancialNews).
    """
    title = (raw.get("title") or "").strip()
    content = (raw.get("content") or raw.get("description") or "").strip()

    if not title or not content:
        return None

    full_text = f"{title} {content}"

    # Parsear fecha
    published_raw = raw.get("publishedAt", "")
    try:
        published_at = datetime.fromisoformat(
            published_raw.replace("Z", "+00:00")
        ).isoformat()
    except Exception:
        published_at = datetime.now(timezone.utc).isoformat()

    return {
        "title":           title,
        "content":         content,
        "source":          raw.get("source", {}).get("name", "unknown"),
        "url":             raw.get("url", ""),
        "published_at":    published_at,
        "ticker_mentions": extract_tickers(full_text),
        "sector":          classify_sector(full_text),
        "content_hash":    compute_hash(title, content),
        "archived":        False,
    }