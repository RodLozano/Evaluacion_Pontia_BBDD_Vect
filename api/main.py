from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.routes.query import router as query_router

app = FastAPI(
    title="Financial RAG API",
    description="Sistema RAG para preguntas sobre noticias financieras y precios de acciones en tiempo real.",
    version="1.0.0",
)

# CORS — permite peticiones desde el frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Rutas
app.include_router(query_router, prefix="/api/v1", tags=["RAG"])


@app.get("/health", tags=["Health"])
async def health_check():
    return {"status": "ok"}