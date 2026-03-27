from fastapi import APIRouter, HTTPException, status

from app.api.v1.schemas.models import CreateUserResponse, User, UserCreate

router = APIRouter()

# Simulação de banco de dados
users_db = [
    {"id": 1, "username": "admin", "email": "admin@email.com"},
    {"id": 2, "username": "dev_user", "email": "dev@email.com"}
]

@router.get("/", response_model=list[User])
async def get_all_users() -> list[User]:
    return users_db

@router.get("/{user_id}", response_model=User)
async def get_user_by_id(user_id: int) -> User:
    user = next((u for u in users_db if u["id"] == user_id), None)
    if not user:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    return user

@router.post("/", response_model=CreateUserResponse, status_code=status.HTTP_201_CREATED)
async def create_user(new_user: UserCreate) -> CreateUserResponse:
    user_data = new_user.model_dump(exclude_none=True)
    users_db.append(user_data)
    return CreateUserResponse(message="Usuário criado com sucesso", data=user_data)