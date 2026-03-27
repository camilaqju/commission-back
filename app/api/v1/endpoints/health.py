from fastapi import APIRouter, status

from app.api.v1.schemas.models import HealthResponse

router = APIRouter()

@router.get("/", status_code=status.HTTP_200_OK, response_model=HealthResponse)
async def health_check() -> HealthResponse:
    return HealthResponse(status="healthy", version="2.0.0")