# app/schemas/user_update_schemas.py
from pydantic import BaseModel, EmailStr, field_validator
from typing import Optional, Dict
from datetime import datetime

class UpdateSelectedPathSchema(BaseModel):
    """Schema para atualizar o caminho selecionado"""
    email: EmailStr
    selected_path: str
    
    @field_validator('selected_path')
    @classmethod
    def validate_path(cls, v):
        valid_paths = ['Ansiedade', 'Atenção Plena', 'Autoimagem', 'Motivação', 'Relacionamentos']
        if v not in valid_paths:
            raise ValueError(f'selected_path deve ser um dos seguintes: {", ".join(valid_paths)}')
        return v


class TestResultsSchema(BaseModel):
    """Schema para os resultados dos testes"""
    Ansiedade: int
    Atenção_Plena: int  # Note o underscore (Python não aceita espaço em atributos)
    Autoimagem: int
    Motivação: int
    Relacionamentos: int
    
    @field_validator('Ansiedade', 'Atenção_Plena', 'Autoimagem', 'Motivação', 'Relacionamentos')
    @classmethod
    def validate_score(cls, v):
        if not 0 <= v <= 100:
            raise ValueError('Cada pontuação deve estar entre 0 e 100')
        return v
    
    def to_dict(self) -> Dict[str, int]:
        """Converte para dict com espaços nos nomes"""
        return {
            "Ansiedade": self.Ansiedade,
            "Atenção Plena": self.Atenção_Plena,
            "Autoimagem": self.Autoimagem,
            "Motivação": self.Motivação,
            "Relacionamentos": self.Relacionamentos
        }


class UpdateTestResultsSchema(BaseModel):
    """Schema para atualizar resultados dos testes"""
    email: EmailStr
    test_results: TestResultsSchema


class ProgressData(BaseModel):
    """Schema para dados de progresso"""
    semana: int
    dia: int
    
    @field_validator('semana')
    @classmethod
    def validate_semana(cls, v):
        if not 1 <= v <= 12:
            raise ValueError('semana deve estar entre 1 e 12')
        return v
    
    @field_validator('dia')
    @classmethod
    def validate_dia(cls, v):
        if not 1 <= v <= 7:
            raise ValueError('dia deve estar entre 1 e 7')
        return v


class UpdateProgressSchema(BaseModel):
    """Schema para atualizar progresso do usuário"""
    email: EmailStr
    progress: ProgressData


class GetUserDataSchema(BaseModel):
    """Schema para buscar dados do usuário"""
    email: EmailStr


class UserUpdateResponse(BaseModel):
    """Schema para resposta de atualização"""
    message: str
    updated_field: str
    user_id: int
    email: str
    
    class Config:
        from_attributes = True


class ProgressResponse(BaseModel):
    """Schema para resposta de atualização de progresso"""
    message: str
    user_id: int
    email: str
    progress: dict
    progress_updated_at: str  # ISO format string
    
    class Config:
        from_attributes = True