# app/main.py
from fastapi import FastAPI
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
