# app/services/password_recovery_service.py
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from passlib.context import CryptContext
import random
import string

from app.models.user import User
from app.services.email_service import send_recovery_code_email

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Código expira em 15 minutos
CODE_EXPIRE_MINUTES = 15


def generate_recovery_code() -> str:
    """Gera código de 4 dígitos aleatórios"""
    return ''.join(random.choices(string.digits, k=4))


def hash_code(code: str) -> str:
    """Criptografa o código de recuperação"""
    return pwd_context.hash(code)


def verify_code(plain_code: str, hashed_code: str) -> bool:
    """Verifica se o código está correto"""
    return pwd_context.verify(plain_code, hashed_code)


def request_password_recovery_service(email: str, db: Session) -> dict:
    """
    Etapa 1: Gera código de recuperação e envia por email
    
    Args:
        email: Email do usuário
        db: Sessão do banco de dados
    
    Returns:
        dict com mensagem de sucesso ou erro
    """
    # Buscar usuário pelo email
    user = db.query(User).filter(User.email == email).first()
    
    if not user:
        # Por segurança, não revelar que o email não existe
        # Retornar sucesso mesmo assim
        return {
            "success": True,
            "message": "If this email exists, a recovery code has been sent",
            "email": email
        }
    
    # Gerar código de 4 dígitos
    recovery_code = generate_recovery_code()
    
    # Criptografar código
    hashed_code = hash_code(recovery_code)
    
    # Definir tempo de expiração (15 minutos)
    expires_at = datetime.utcnow() + timedelta(minutes=CODE_EXPIRE_MINUTES)
    
    # Salvar no banco
    user.temp_password = hashed_code
    user.temp_password_expires = expires_at
    
    db.commit()
    
    # Enviar email com código
    email_sent = send_recovery_code_email(
        to_email=email,
        user_login=user.login,
        recovery_code=recovery_code
    )
    
    if not email_sent:
        # Se falhar ao enviar email, reverter mudanças
        user.temp_password = None
        user.temp_password_expires = None
        db.commit()
        
        return {
            "success": False,
            "message": "Failed to send recovery email. Please try again later.",
            "email": email
        }
    
    return {
        "success": True,
        "message": "Recovery code sent to your email",
        "email": email
    }


def verify_recovery_code_service(email: str, code: str, db: Session) -> dict:
    """
    Etapa 2: Verifica se o código está correto
    
    Args:
        email: Email do usuário
        code: Código de 4 dígitos enviado pelo usuário
        db: Sessão do banco de dados
    
    Returns:
        dict com resultado da verificação
    """
    # Buscar usuário
    user = db.query(User).filter(User.email == email).first()
    
    if not user:
        return {
            "success": False,
            "message": "Invalid email or code",
            "email": email
        }
    
    # Verificar se existe código temporário
    if not user.temp_password or not user.temp_password_expires:
        return {
            "success": False,
            "message": "No recovery code requested for this email",
            "email": email
        }
    
    # Verificar se código expirou
    if datetime.utcnow() > user.temp_password_expires:
        # Limpar código expirado
        user.temp_password = None
        user.temp_password_expires = None
        db.commit()
        
        return {
            "success": False,
            "message": "Recovery code has expired. Please request a new one.",
            "email": email
        }
    
    # Verificar se código está correto
    if not verify_code(code, user.temp_password):
        return {
            "success": False,
            "message": "Invalid recovery code",
            "email": email
        }
    
    return {
        "success": True,
        "message": "Recovery code verified successfully",
        "email": email
    }


def reset_password_service(email: str, code: str, new_password: str, db: Session) -> dict:
    """
    Etapa 3: Verifica código e altera a senha
    
    Args:
        email: Email do usuário
        code: Código de 4 dígitos
        new_password: Nova senha
        db: Sessão do banco de dados
    
    Returns:
        dict com resultado da operação
    """
    # Primeiro verificar o código (reutilizando a lógica da etapa 2)
    verification = verify_recovery_code_service(email, code, db)
    
    if not verification["success"]:
        return verification
    
    # Buscar usuário novamente
    user = db.query(User).filter(User.email == email).first()
    
    if not user:
        return {
            "success": False,
            "message": "User not found",
            "email": email
        }
    
    # Atualizar senha
    user.password = pwd_context.hash(new_password)
    
    # Limpar código temporário
    user.temp_password = None
    user.temp_password_expires = None
    
    db.commit()
    
    return {
        "success": True,
        "message": "Password reset successfully",
        "email": email
    }