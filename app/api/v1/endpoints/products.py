from fastapi import APIRouter, status

router = APIRouter()

# Simulação de banco de dados
products_db = [
    {"id": 101, "name": "Notebook", "price": 4500.0},
    {"id": 102, "name": "Mouse Gamer", "price": 150.0}
]

@router.get("/")
async def list_products():
    return products_db

@router.post("/", status_code=status.HTTP_201_CREATED)
async def add_product(product: dict):
    products_db.append(product)
    return {"message": "Produto adicionado", "product": product}