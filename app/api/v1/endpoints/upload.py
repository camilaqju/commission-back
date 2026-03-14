# app/api/v1/endpoints/upload.py
from fastapi import APIRouter, UploadFile, File
from app.api.v1.services.upload_service import read_excel

router = APIRouter()

@router.post("/file", tags=["Files"])
async def upload(file: UploadFile = File(...)):
    print("Recebi arquivo:", file.filename)  # <-- log simples

    result = read_excel(file)
    print("Resultado:", result)
    return result