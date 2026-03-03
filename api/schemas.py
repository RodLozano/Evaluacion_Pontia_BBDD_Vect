from pydantic import BaseModel, Field


class QueryRequest(BaseModel):
    question: str = Field(
        ...,
        min_length=5,
        max_length=500,
        example="Why is Tesla stock dropping today?",
    )
    time_range_hours: int = Field(
        default=24,
        ge=1,
        le=168,  # Máximo 7 días
        description="Ventana temporal en horas para buscar noticias",
    )


class SourceItem(BaseModel):
    title:        str
    source:       str
    published_at: str
    url:          str


class MarketDataItem(BaseModel):
    ticker:       str
    company_name: str
    price:        float
    change_pct:   float
    volume:       int
    summary:      str
    timestamp:    str


class QueryResponse(BaseModel):
    answer:      str
    sources:     list[SourceItem]
    tickers:     list[str]
    market_data: list[dict]
    docs_used:   int