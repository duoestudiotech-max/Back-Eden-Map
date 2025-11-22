from pydantic import BaseModel
from typing import Optional

class LoginRequest(BaseModel):
    """Schema para requisição de login"""
    login: str
    password: str

class RefreshTokenRequest(BaseModel):
    """Schema para requisição de refresh token"""
    refresh_token: str

class TokenResponse(BaseModel):
    """Schema para resposta de tokens"""
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    user: dict

    class Config:
        from_attributes = True

class LoginResponse(TokenResponse):
    """Schema para resposta de login (herda de TokenResponse)"""
    pass
