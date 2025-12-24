from sqlalchemy.orm import Session
from fastapi import HTTPException, status, Request
from app.schemas.user_schemas import UserCreate
from app.services.user_service import (
    create_user_service,
    get_user_service,
    list_users_service
)
from app.services.validators import (validate_user_exists, validate_email_exists)
import logging

logger = logging.getLogger('app.controllers.user_controller')


def get_client_info(request: Request):
    """Extrai informações do cliente da requisição"""
    return {
        "ip_address": request.client.host if request.client else None,
        "user_agent": request.headers.get("user-agent")
    }


def create_user_controller(user: UserCreate, db: Session, request: Request):
    """
    Controller para criar usuário e retornar tokens
    
    Args:
        user: Dados do usuário
        db: Sessão do banco
        request: Request object para capturar IP e user agent
    
    Returns:
        dict com tokens e dados do usuário
    """
    try:
        logger.info(f"📥 Tentando criar usuário: {user.login} ({user.email})")
        
        email_exists = validate_email_exists(user.email, db)
        if email_exists:
            logger.warning(f"❌ Email já cadastrado: {user.email}")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )
        
        login_exists = validate_user_exists(user.login, db)
        if login_exists:
            logger.warning(f"❌ Login já cadastrado: {user.login}")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Login already registered"
            )
        
        client_info = get_client_info(request)
        logger.info(f"📍 IP: {client_info['ip_address']}")
        
        response = create_user_service(user, db, **client_info)
        
        logger.info(f"✅ Usuário criado com sucesso: {user.login}")
        return response
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"❌ ERRO INESPERADO ao criar usuário: {str(e)}")
        logger.exception(e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Internal server error: {str(e)}"
        )


def get_user_controller(user_id: int, db: Session):
    """Controller para buscar usuário"""
    return get_user_service(user_id, db)


def list_users_controller(skip: int, limit: int, db: Session):
    """Controller para listar usuários"""
    return list_users_service(skip, limit, db)