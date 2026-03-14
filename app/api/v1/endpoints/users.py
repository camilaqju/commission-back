from fastapi import APIRouter, HTTPException, status

router = APIRouter()

# Simulação de banco de dados
users_db = [
    {"id": 1, "username": "admin", "email": "admin@email.com"},
    {"id": 2, "username": "dev_user", "email": "dev@email.com"}
]

@router.get("/")
async def get_all_users():
    return users_db

@router.get("/{user_id}")
async def get_user_by_id(user_id: int):
    user = next((u for u in users_db if u["id"] == user_id), None)
    if not user:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    return user

@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_user(new_user: dict):
    # Como não temos schemas, o 'new_user' aceitará qualquer JSON enviado
    users_db.append(new_user)
    return {"message": "Usuário criado com sucesso", "data": new_user}