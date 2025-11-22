# app/routers/password_recovery_routes.py
from fastapi import APIRouter, Depends, status, Request
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas.password_recovery_schemas import (
    RequestPasswordRecoverySchema,
    VerifyRecoveryCodeSchema,
    ResetPasswordSchema,
    PasswordRecoveryResponse
)
from app.controllers.password_recovery_controller import (
    request_password_recovery_controller,
    verify_recovery_code_controller,
    reset_password_controller
)
from app.auth.dependencies import rate_limit_password_recovery

router = APIRouter(prefix="/auth/password-recovery", tags=["password-recovery"])


@router.post(
    "/request",
    response_model=PasswordRecoveryResponse,
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(rate_limit_password_recovery)]
)
def request_password_recovery_route(
    data: RequestPasswordRecoverySchema,
    request: Request,
    db: Session = Depends(get_db)
):
    """
    **ETAPA 1: Solicitar código de recuperação de senha**
    
    **Rate Limit: 3 requisições por hora por IP**
    
    Envia um código de 4 dígitos para o email do usuário.
    O código expira em 15 minutos.
    
    **Segurança:** Por razões de segurança, sempre retorna sucesso,
    mesmo se o email não existir no banco de dados.
    
    Args:
        data: Objeto com email do usuário
    
    Returns:
        Mensagem de confirmação
    
    Example:
        ```json
        POST /auth/password-recovery/request
        {
            "email": "usuario@email.com"
        }
        
        Response:
        {
            "message": "If this email exists, a recovery code has been sent",
            "email": "usuario@email.com"
        }
        ```
    
    Errors:
        429: Too many requests (excedeu 3 requisições/hora)
    """
    return request_password_recovery_controller(data, db)


@router.post(
    "/verify",
    response_model=PasswordRecoveryResponse,
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(rate_limit_password_recovery)]
)
def verify_recovery_code_route(
    data: VerifyRecoveryCodeSchema,
    request: Request,
    db: Session = Depends(get_db)
):
    """
    **ETAPA 2: Verificar código de recuperação**
    
    **Rate Limit: 3 requisições por hora por IP**
    
    Verifica se o código de 4 dígitos está correto e ainda não expirou.
    
    Args:
        data: Objeto com email e código de 4 dígitos
    
    Returns:
        Confirmação de código válido
    
    Example:
        ```json
        POST /auth/password-recovery/verify
        {
            "email": "usuario@email.com",
            "code": "1234"
        }
        
        Response:
        {
            "message": "Recovery code verified successfully",
            "email": "usuario@email.com"
        }
        ```
    
    Errors:
        400: Invalid or expired code
        429: Too many requests (excedeu 3 requisições/hora)
    """
    return verify_recovery_code_controller(data, db)


@router.post(
    "/reset",
    response_model=PasswordRecoveryResponse,
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(rate_limit_password_recovery)]
)
def reset_password_route(
    data: ResetPasswordSchema,
    request: Request,
    db: Session = Depends(get_db)
):
    """
    **ETAPA 3: Redefinir senha**
    
    **Rate Limit: 3 requisições por hora por IP**
    
    Verifica o código novamente e, se correto, altera a senha do usuário.
    Após redefinir a senha, o código de recuperação é invalidado.
    
    Args:
        data: Objeto com email, código e nova senha
    
    Returns:
        Confirmação de senha alterada
    
    Example:
        ```json
        POST /auth/password-recovery/reset
        {
            "email": "usuario@email.com",
            "code": "1234",
            "new_password": "NovaSenha123@"
        }
        
        Response:
        {
            "message": "Password reset successfully",
            "email": "usuario@email.com"
        }
        ```
    
    Errors:
        400: Invalid or expired code
        429: Too many requests (excedeu 3 requisições/hora)
    """
    return reset_password_controller(data, db)