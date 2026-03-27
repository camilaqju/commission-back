from __future__ import annotations

from typing import Any

from pydantic import BaseModel


class HealthResponse(BaseModel):
    status: str
    version: str


class Product(BaseModel):
    id: int | None = None
    name: str
    price: float


class ProductCreate(BaseModel):
    # Your current code stores whatever JSON arrives; this keeps Swagger strict without
    # breaking clients that omit `id`.
    id: int | None = None
    name: str
    price: float


class AddProductResponse(BaseModel):
    message: str
    product: Product


class User(BaseModel):
    id: int | None = None
    username: str
    email: str


class UserCreate(BaseModel):
    id: int | None = None
    username: str
    email: str


class CreateUserResponse(BaseModel):
    message: str
    data: User


class UploadExcelPreviewRow(BaseModel):
    # Rows are dynamic because they depend on the uploaded Excel columns.
    # We keep it flexible for Swagger/OpenAPI consumers.
    model_config = {"extra": "allow"}  # allows arbitrary keys


class UploadExcelResult(BaseModel):
    filename: str
    rows: int
    columns: int
    preview: list[dict[str, Any]]


class UploadResponse(BaseModel):
    nome: str
    cpf: str
    taxa_comissao: float
    resultado: UploadExcelResult


class ErrorResponse(BaseModel):
    detail: str

