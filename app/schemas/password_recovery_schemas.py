# app/schemas/password_recovery_schemas.py
from pydantic import BaseModel, EmailStr

class RequestPasswordRecoverySchema(BaseModel):
    """Schema para solicitar código de recuperação"""
    email: EmailStr

class VerifyRecoveryCodeSchema(BaseModel):
    """Schema para verificar código de recuperação"""
    email: EmailStr
    code: str

class ResetPasswordSchema(BaseModel):
    """Schema para redefinir senha"""
    email: EmailStr
    code: str
    new_password: str

class PasswordRecoveryResponse(BaseModel):
    """Schema para resposta de recuperação de senha"""
    message: str
    email: str
    
    class Config:
        from_attributes = True