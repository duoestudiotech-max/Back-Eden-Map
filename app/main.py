# app/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware  # ← IMPORTAR CORS
from app.core.init_db import init_db
from app.routers.user_routes import router as user_router
from app.routers.auth_routes import router as auth_router
from app.routers.password_recovery_routes import router as password_recovery_router

# Inicializar banco de dados
init_db()

# Criar aplicação
app = FastAPI(
    title="Back-Eden-Map API",
    description="API para gerenciamento de usuários do Eden Map",
    version="1.0.0"
)

# ============================================================================
# 🔥 CONFIGURAÇÃO DE CORS (ADICIONAR ISSO)
# ============================================================================

# Lista de origens permitidas
origins = [
    "http://localhost:8081",      # Expo Web
    "http://localhost:19006",     # Expo Web alternativo
    "http://localhost:3000",      # React Web
    "http://127.0.0.1:8081",      # Alternativo
    "http://192.168.1.*",         # Sua rede local (ajuste conforme necessário)
    "*",                          # ⚠️ Para desenvolvimento, aceita tudo
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,              # Permite essas origens
    allow_credentials=True,             # Permite cookies/autenticação
    allow_methods=["*"],                # Permite todos os métodos (GET, POST, etc)
    allow_headers=["*"],                # Permite todos os headers
)

# ============================================================================
# FIM DA CONFIGURAÇÃO DE CORS
# ============================================================================

# Incluir rotas
app.include_router(user_router)
app.include_router(auth_router)
app.include_router(password_recovery_router)

@app.get("/")
def root():
    return {
        "message": "Welcome to Back-Eden-Map API",
        "docs": "/docs"
    }

@app.get("/health")
def health_check():
    return {"status": "healthy"}
