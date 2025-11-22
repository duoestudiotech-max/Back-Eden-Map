# app/controllers/password_recovery_controller.py
from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from app.schemas.password_recovery_schemas import (
    RequestPasswordRecoverySchema,
    VerifyRecoveryCodeSchema,
    ResetPasswordSchema
)
from app.services.password_recovery_service import (
    request_password_recovery_service,
    verify_recovery_code_service,
    reset_password_service
)


def request_password_recovery_controller(data: RequestPasswordRecoverySchema, db: Session):
    """
    Controller para Etapa 1: Solicitar código de recuperação
    
    Args:
        data: Schema com email
        db: Sessão do banco
    
    Returns:
        dict com mensagem de sucesso
    """
    result = request_password_recovery_service(data.email, db)
    
    # Sempre retornar sucesso para não revelar se email existe
    return {
        "message": result["message"],
        "email": data.email
    }


def verify_recovery_code_controller(data: VerifyRecoveryCodeSchema, db: Session):
    """
    Controller para Etapa 2: Verificar código de recuperação
    
    Args:
        data: Schema com email e código
        db: Sessão do banco
    
    Returns:
        dict com resultado da verificação
        
    Raises:
        HTTPException: Se código inválido ou expirado
    """
    result = verify_recovery_code_service(data.email, data.code, db)
    
    if not result["success"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=result["message"]
        )
    
    return {
        "message": result["message"],
        "email": data.email
    }


def reset_password_controller(data: ResetPasswordSchema, db: Session):
    """
    Controller para Etapa 3: Redefinir senha
    
    Args:
        data: Schema com email, código e nova senha
        db: Sessão do banco
    
    Returns:
        dict com mensagem de sucesso
        
    Raises:
        HTTPException: Se código inválido ou expirado
    """
    result = reset_password_service(data.email, data.code, data.new_password, db)
    
    if not result["success"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=result["message"]
        )
    
    return {
        "message": result["message"],
        "email": data.email
    }