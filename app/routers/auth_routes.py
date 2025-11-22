from fastapi import APIRouter, Depends, status, Request
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas.auth_schemas import LoginRequest, LoginResponse, RefreshTokenRequest, TokenResponse
from app.controllers.auth_controller import login_controller, refresh_token_controller
from app.auth.dependencies import rate_limit_login, rate_limit_refresh

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post(
    "/login", 
    response_model=LoginResponse, 
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(rate_limit_login)]
)
def login_route(
    credentials: LoginRequest, 
    request: Request,
    db: Session = Depends(get_db)
):
    """
    Rota de autenticação com usuário e senha
    
    **Rate Limit: 6 requisições por hora por IP**
    
    Recebe login e senha, retorna access token, refresh token e dados do usuário
    
    Args:
        credentials: Objeto com login e password
        request: Request object (automático)
        db: Sessão do banco de dados (injetada automaticamente)
    
    Returns:
        LoginResponse com access_token, refresh_token e dados do usuário
    
    Example:
        POST /auth/login
        {
            "login": "dieghonm",
            "password": "Admin123@"
        }
        
        Response:
        {
            "access_token": "eyJhbGc...",
            "refresh_token": "a8f3k2j9...",
            "token_type": "bearer",
            "user": {
                "id": 1,
                "login": "dieghonm",
                "email": "dieghonm@gmail.com",
                "tag": "admin",
                "plan": "admin"
            }
        }
    
    Errors:
        401: Invalid credentials
        429: Too many login attempts (excedeu 6 requisições/hora)
    """
    return login_controller(credentials, db, request)


@router.post(
    "/refresh", 
    response_model=TokenResponse, 
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(rate_limit_refresh)]
)
def refresh_token_route(
    refresh_request: RefreshTokenRequest,
    request: Request,
    db: Session = Depends(get_db)
):
    """
    Rota para renovar access token usando refresh token
    
    **Rate Limit: 4 requisições por hora por IP**
    
    Recebe um refresh token válido e retorna novos tokens
    O refresh token é automaticamente renovado por mais 30 dias
    
    Args:
        refresh_request: Objeto com refresh_token
        request: Request object (automático)
        db: Sessão do banco de dados (injetada automaticamente)
    
    Returns:
        TokenResponse com novos access_token e refresh_token
    
    Example:
        POST /auth/refresh
        {
            "refresh_token": "a8f3k2j9..."
        }
        
        Response:
        {
            "access_token": "eyJhbGc...",
            "refresh_token": "b9g4l3k0...",
            "token_type": "bearer",
            "user": {
                "id": 1,
                "login": "dieghonm",
                "email": "dieghonm@gmail.com",
                "tag": "admin",
                "plan": "admin"
            }
        }
    
    Errors:
        401: Invalid or expired refresh token
        429: Too many refresh attempts (excedeu 4 requisições/hora)
    """
    return refresh_token_controller(refresh_request, db, request)
