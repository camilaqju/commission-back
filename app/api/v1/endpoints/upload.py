# app/api/v1/endpoints/upload.py
from fastapi import APIRouter, UploadFile, File, Form, HTTPException
import re

from app.api.v1.services.upload_service import read_excel
from app.api.v1.schemas.models import UploadResponse

router = APIRouter()

@router.post("/file", response_model=UploadResponse, tags=["Files"])
async def upload(
    file: UploadFile = File(...),
    nome: str = Form(...),
    cpf: str = Form(...),
    taxa_comissao: str = Form(...)  # <- usar str pra validar melhor
):
    # =========================
    # VALIDAÇÕES
    # =========================

    # 1. Arquivo
    if not file or not file.filename:
        raise HTTPException(status_code=400, detail="Arquivo é obrigatório")

    if not file.filename.endswith((".xlsx", ".xls")):
        raise HTTPException(status_code=400, detail="Arquivo deve ser Excel (.xlsx ou .xls)")

    # 2. Nome (apenas letras e espaços)
    if not nome.strip():
        raise HTTPException(status_code=400, detail="Nome é obrigatório")

    if not re.fullmatch(r"[A-Za-zÀ-ÿ\s]+", nome):
        raise HTTPException(status_code=400, detail="Nome deve conter apenas letras")

    # 3. CPF (somente números e até 11 dígitos)
    if not cpf.isdigit():
        raise HTTPException(status_code=400, detail="CPF deve conter apenas números")

    if len(cpf) != 11:
        raise HTTPException(status_code=400, detail="CPF deve ter 11 dígitos")

    # 4. Taxa de comissão (número com ponto)
    if not re.fullmatch(r"\d+(\.\d+)?", taxa_comissao):
        raise HTTPException(
            status_code=400,
            detail="Taxa de comissão deve ser um número válido (ex: 10 ou 10.5)"
        )

    taxa_comissao = float(taxa_comissao)

    # =========================
    # LOG
    # =========================
    print("Recebi arquivo:", file.filename)
    print("Nome:", nome)
    print("CPF:", cpf)
    print("Taxa:", taxa_comissao)

    result = read_excel(file, taxa_comissao)

    return UploadResponse(
        nome=nome,
        cpf=cpf,
        taxa_comissao=taxa_comissao,
        resultado=result,
    )