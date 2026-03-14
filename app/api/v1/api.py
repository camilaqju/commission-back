from fastapi import APIRouter
from app.api.v1.endpoints import users, products, health, upload # Importe o novo arquivo

api_router = APIRouter()

# Rotas de negócio
api_router.include_router(users.router, prefix="/users", tags=["Users"])
api_router.include_router(products.router, prefix="/products", tags=["Products"])
api_router.include_router(upload.router, prefix="/upload", tags=["Files"])

# Rota de infraestrutura
api_router.include_router(health.router, prefix="/health-check", tags=["Health Check"])

