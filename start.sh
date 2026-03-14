#!/bin/bash

# 1. Verifica se o ambiente virtual existe, se não, cria
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python -m venv venv
fi

# 2. Ativa o ambiente virtual
.\venv\Scripts\Activate

# 3. Garante que as dependências estão instaladas
echo "Checking dependencies..."
pip install -r requirements.txt

# 4. Inicia o servidor FastAPI com porta customizada e auto-reload
# Busca a porta do .env ou usa 8000 como padrão
PORT_SERVER=$(grep PORT .env | cut -d '=' -f2 || echo 8000)

echo "Starting FastAPI server on port $PORT_SERVER..."
uvicorn app.main:app --host 0.0.0.0 --port $PORT_SERVER --reload --reload-dir app