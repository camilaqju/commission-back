from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.v1.api import api_router
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(
    title="Minha Comissão API",
    description="Exemplo de rotas divididas por domínio.",
    version="1.0.0"
)
origins = [
    "http://localhost:5173",  # seu frontend (Vite)
    "*"
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,        # quem pode acessar
    allow_credentials=True,
    allow_methods=["*"],          # GET, POST, etc
    allow_headers=["*"],          # headers liberados
)
# Todas as rotas agora começam com /api/v1
app.include_router(api_router, prefix="/api/v1")