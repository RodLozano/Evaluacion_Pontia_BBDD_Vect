from fastapi import APIRouter, HTTPException
from api.schemas import QueryRequest, QueryResponse
from llm.openai_client import answer_question

router = APIRouter()


@router.post(
    "/query",
    response_model=QueryResponse,
    summary="Hacer una pregunta sobre noticias financieras",
    description="Recibe una pregunta en lenguaje natural y devuelve una respuesta basada en noticias recientes y datos de mercado en tiempo real.",
)
async def query_endpoint(request: QueryRequest):
    try:
        result = answer_question(
            question=request.question,
            time_range_hours=request.time_range_hours,
        )
        return QueryResponse(**result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))