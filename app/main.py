# # app/main.py
# from fastapi import FastAPI
# from fastapi.middleware.cors import CORSMiddleware
# from app.core.init_db import init_db
# from app.routers.user_routes import router as user_router
# from app.routers.auth_routes import router as auth_router
# from app.routers.password_recovery_routes import router as password_recovery_router
# from app.routers.user_update_routes import router as user_update_router

# # Inicializar banco de dados
# init_db()

# # Criar aplicação
# app = FastAPI(
#     title="Back-Eden-Map API",
#     description="API para gerenciamento de usuários do Eden Map",
#     version="1.0.0"
# )

# # CORS
# origins = [
#     "http://localhost:8081",
#     "http://localhost:19006",
#     "http://localhost:3000",
#     "http://127.0.0.1:8081",
#     "http://192.168.1.*",
#     "*",
# ]

# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=origins,
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# # Incluir rotas
# app.include_router(user_router)
# app.include_router(auth_router)
# app.include_router(password_recovery_router)
# app.include_router(user_update_router)

# @app.get("/")
# def root():
#     return {
#         "message": "Welcome to Back-Eden-Map API",
#         "docs": "/docs"
#     }

# @app.get("/health")
# def health_check():
#     return {"status": "healthy"}

#local ou render


# app/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.init_db import init_db
from app.core.config import settings
from app.routers.user_routes import router as user_router
from app.routers.auth_routes import router as auth_router
from app.routers.password_recovery_routes import router as password_recovery_router
from app.routers.user_update_routes import router as user_update_router
import logging

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Inicializar banco de dados
logger.info("Inicializando banco de dados...")
init_db()
logger.info("Banco de dados inicializado!")

# Criar aplicação
app = FastAPI(
    title="Back-Eden-Map API",
    description="API para gerenciamento de usuários do Eden Map",
    version="1.0.0"
)

# CORS - configuração para produção e desenvolvimento
if settings.ENVIRONMENT == "production":
    origins = [
        "https://seu-frontend.com",        # front web (se houver)
        "https://www.seu-frontend.com",
        "null",                             # apps nativos (React Native, iOS, Android)
    ]
else:
    origins = [
        "http://localhost:8081",  # Expo web
        "http://localhost:19006", # Expo
        "http://localhost:3000",  # React
        "http://127.0.0.1:8081",
        "*",                      # dev facilitado
        "null",                   # mobile no emulador
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
        "docs": "/docs",
        "environment": settings.ENVIRONMENT
    }

@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "environment": settings.ENVIRONMENT
    }