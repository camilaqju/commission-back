from fastapi import FastAPI
from app.api.v1.api import api_router
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(
    title="Minha API Modular",
    description="Exemplo de rotas divididas por domínio.",
    version="1.0.0"
)

# Todas as rotas agora começam com /api/v1
app.include_router(api_router, prefix="/api/v1")