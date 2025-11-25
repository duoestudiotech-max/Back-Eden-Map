from pydantic import BaseModel
from typing import Optional, List, Dict
from datetime import datetime

class LoginRequest(BaseModel):
    """Schema para requisição de login"""
    login: str
    password: str

class RefreshTokenRequest(BaseModel):
    """Schema para requisição de refresh token"""
    refresh_token: str

class UserData(BaseModel):
    """Schema completo dos dados do usuário retornados no login/registro"""
    id: int
    login: str
    email: str
    tag: Optional[str]
    plan: Optional[str]
    plan_date: Optional[str]  # ISO format string
    selected_path: Optional[List[str]]
    selected_path: Optional[str]
    progress: Optional[Dict]

    class Config:
        from_attributes = True

class TokenResponse(BaseModel):
    """Schema para resposta de tokens"""
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    user: UserData

    class Config:
        from_attributes = True

class LoginResponse(TokenResponse):
    """Schema para resposta de login (herda de TokenResponse)"""
    pass