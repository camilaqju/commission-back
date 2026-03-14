# app/api/v1/services/upload_service.py
import pandas as pd
from fastapi import UploadFile, HTTPException

def read_excel(file: UploadFile) -> dict:
    """Lê um arquivo Excel e retorna algumas informações"""
    if not file.filename.endswith((".xls", ".xlsx")):
        raise HTTPException(status_code=400, detail="Arquivo deve ser XLS ou XLSX")
    
    try:
        df = pd.read_excel(file.file)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao ler o arquivo: {e}")
    
    return {
        "filename": file.filename,
        "rows": df.shape[0],
        "columns": df.shape[1],
        "preview": df.head(5).to_dict(orient="records")
    }