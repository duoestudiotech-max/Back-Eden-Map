#!/usr/bin/env bash
# exit on error
set -o errexit

# Instalar dependências
pip install --upgrade pip
pip install -r requirements.txt

# Inicializar banco de dados
python -c "from app.core.init_db import init_db; init_db()"