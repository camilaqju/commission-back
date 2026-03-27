from fastapi import APIRouter, status

from app.api.v1.schemas.models import (
    AddProductResponse,
    Product,
    ProductCreate,
)

router = APIRouter()

# Simulação de banco de dados
products_db = [
    {"id": 101, "name": "Notebook", "price": 4500.0},
    {"id": 102, "name": "Mouse Gamer", "price": 150.0}
]

@router.get("/", response_model=list[Product])
async def list_products() -> list[Product]:
    return products_db

@router.post("/", response_model=AddProductResponse, status_code=status.HTTP_201_CREATED)
async def add_product(product: ProductCreate) -> AddProductResponse:
    product_data = product.model_dump(exclude_none=True)
    products_db.append(product_data)
    return AddProductResponse(message="Produto adicionado", product=product_data)