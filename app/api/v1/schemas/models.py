from __future__ import annotations

from datetime import datetime
from typing import Any, Literal

from pydantic import AliasChoices, BaseModel, Field


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


class UploadExcelRow(BaseModel):
    """
    Typing for a single Excel row returned to the client.

    Some original Excel columns contain spaces (e.g. "EMISSAO NF"). We use
    field aliases so the API can keep the original keys while still being typed.
    Dynamic parcel columns like `valor_parcela_1` / `mes_parcela_1` are allowed via `extra`.
    """

    model_config = {
        "populate_by_name": True,
        "extra": "allow",
    }

    nf: int = Field(alias="NF")
    emissao_nf: datetime | str | None = Field(
        default=None,
        validation_alias=AliasChoices("EMISSAO_NF", "EMISSAO NF"),
        serialization_alias="EMISSAO_NF",
    )
    cliente: str | None = Field(default=None, alias="CLIENTE")
    cond_pgto: str | None = Field(
        default=None,
        validation_alias=AliasChoices("COND_PGTO", "COND PGTO"),
        serialization_alias="COND_PGTO",
    )
    total: float | int | None = Field(default=None, alias="Total")

    taxa_comissao: float | None = None
    comissao_calculada: float | None = None
    prazo_pagamento: list[int] | None = None
    numero_parcelas: int | Literal["Não encontrado"] | None = None
    comissao_parcela: float | Literal["Não encontrado"] | None = None


class UploadExcelResult(BaseModel):
    filename: str
    rows: int
    columns: int
    preview: list[UploadExcelRow]


class UploadResponse(BaseModel):
    nome: str
    cpf: str
    taxa_comissao: float
    resultado: UploadExcelResult


class ErrorResponse(BaseModel):
    detail: str

