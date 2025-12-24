# app/schemas/user_schemas.py - CORRIGIDO
from pydantic import BaseModel, EmailStr
from typing import Optional, List, Dict
from datetime import datetime

class UserCreate(BaseModel):
    login: str
    password: str
    email: EmailStr
    tag: Optional[str] = "client"
    plan: Optional[str] = "trial"

class UserResponse(BaseModel):
    id: int
    login: str
    email: str
    tag: Optional[str]
    plan: Optional[str]
    plan_date: Optional[datetime]
    selected_feelings: Optional[List[str]] 
    selected_path: Optional[str] 
    test_results: Optional[Dict]
    progress: Optional[Dict]
    created_at: datetime

    class Config:
        from_attributes = True

class UserData(BaseModel):
    """Schema completo dos dados do usuário retornados no login/registro"""
    id: int
    login: str
    email: str
    tag: Optional[str]
    plan: Optional[str]
    plan_date: Optional[str]
    selected_feelings: Optional[List[str]] = None 
    selected_path: Optional[str]
    progress: Optional[Dict]

    class Config:
        from_attributes = True

class CreateUserResponse(BaseModel):
    """Schema para resposta de criação de usuário (com tokens)"""
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    user: UserData

    class Config:
        from_attributes = True