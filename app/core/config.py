# # app/core/config.py
# from pydantic_settings import BaseSettings
# from typing import Optional

# class Settings(BaseSettings):
#     # Banco de dados
#     DATABASE_URL: str
    
#     # JWT
#     SECRET_KEY: str
#     ALGORITHM: str = "HS256"
#     ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
#     # Rate Limiting (requisições por hora)
#     RATE_LIMIT_REGISTER: int = 2
#     RATE_LIMIT_REFRESH: int = 4
#     RATE_LIMIT_LOGIN: int = 6
#     RATE_LIMIT_PASSWORD_RECOVERY: int = 12
    
#     # Brevo Email Service
#     BREVO_API_KEY: Optional[str] = None
#     BREVO_SENDER_EMAIL: str = "duo.estudio.tech@gmail.com"
#     BREVO_SENDER_NAME: str = "Eden Map"
#     EMAIL_ENABLED: bool = True

#     class Config:
#         env_file = ".env"

# settings = Settings()

#local ou render

# app/core/config.py
from pydantic_settings import BaseSettings
from typing import Optional
import os

class Settings(BaseSettings):
    # Banco de dados - usar DATABASE_URL do Render
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./banco.db")
    
    # JWT
    SECRET_KEY: str = os.getenv("SECRET_KEY", "LocalhostPassword")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # Rate Limiting (requisições por hora)
    RATE_LIMIT_REGISTER: int = 2
    RATE_LIMIT_REFRESH: int = 4
    RATE_LIMIT_LOGIN: int = 6
    RATE_LIMIT_PASSWORD_RECOVERY: int = 12
    
    # Brevo Email Service
    BREVO_API_KEY: Optional[str] = os.getenv("BREVO_API_KEY")
    BREVO_SENDER_EMAIL: str = "duo.estudio.tech@gmail.com"
    BREVO_SENDER_NAME: str = "Eden Map"
    EMAIL_ENABLED: bool = True
    
    # Ambiente
    ENVIRONMENT: str = os.getenv("ENVIRONMENT", "development")

    class Config:
        env_file = ".env"

settings = Settings()
