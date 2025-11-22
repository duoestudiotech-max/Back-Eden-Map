from fastapi import HTTPException, status, Request
from sqlalchemy.orm import Session

from app.schemas.auth_schemas import LoginRequest, RefreshTokenRequest
from app.services.auth_service import login_service, refresh_access_token_service


def get_client_info(request: Request):
    """Extrai informações do cliente da requisição"""
    return {
        "ip_address": request.client.host if request.client else None,
        "user_agent": request.headers.get("user-agent")
    }


def login_controller(credentials: LoginRequest, db: Session, request: Request):
    """
    Controller para autenticação de usuário
    
    Args:
        credentials: Objeto com login e password
        db: Sessão do banco de dados
        request: Request object para capturar IP e user agent
    
    Returns:
        dict com tokens e dados do usuário
        
    Raises:
        HTTPException: Se credenciais inválidas
    """
    client_info = get_client_info(request)
    
    result = login_service(
        login=credentials.login,
        password=credentials.password,
        db=db,
        **client_info
    )
    
    if not result:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
            headers={"WWW-Authenticate": "Bearer"}
        )
    
    return result


def refresh_token_controller(refresh_request: RefreshTokenRequest, db: Session, request: Request):
    """
    Controller para renovar access token usando refresh token
    
    Args:
        refresh_request: Objeto com refresh_token
        db: Sessão do banco de dados
        request: Request object para capturar IP e user agent
    
    Returns:
        dict com novos tokens e dados do usuário
        
    Raises:
        HTTPException: Se refresh token inválido
    """
    client_info = get_client_info(request)
    
    result = refresh_access_token_service(
        refresh_token=refresh_request.refresh_token,
        db=db,
        **client_info
    )
    
    if not result:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired refresh token",
            headers={"WWW-Authenticate": "Bearer"}
        )
    
    return result