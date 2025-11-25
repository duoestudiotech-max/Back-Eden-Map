# app/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.init_db import init_db
from app.routers.user_routes import router as user_router
from app.routers.auth_routes import router as auth_router
from app.routers.password_recovery_routes import router as password_recovery_router
from app.routers.user_update_routes import router as user_update_router

# Inicializar banco de dados
init_db()

# Criar aplicação
app = FastAPI(
    title="Back-Eden-Map API",
    description="API para gerenciamento de usuários do Eden Map",
    version="1.0.0"
)

# CORS
origins = [
    "http://localhost:8081",
    "http://localhost:19006",
    "http://localhost:3000",
    "http://127.0.0.1:8081",
    "http://192.168.1.*",
    "*",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Incluir rotas
app.include_router(user_router)
app.include_router(auth_router)
app.include_router(password_recovery_router)
app.include_router(user_update_router)

@app.get("/")
def root():
    return {
        "message": "Welcome to Back-Eden-Map API",
        "docs": "/docs"
    }

@app.get("/health")
def health_check():
    return {"status": "healthy"}