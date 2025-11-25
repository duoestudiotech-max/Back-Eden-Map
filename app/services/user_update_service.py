# app/services/user_update_service.py
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from datetime import datetime
import logging

from app.models.user import User
from app.schemas.user_update_schemas import (
    UpdateSelectedPathSchema, 
    UpdateTestResultsSchema, 
    UpdateProgressSchema,
    GetUserDataSchema
)

logger = logging.getLogger('app.services.user_update_service')


def update_selected_path_service(data: UpdateSelectedPathSchema, db: Session):
    """
    Atualiza o caminho selecionado pelo usuário usando email
    
    Args:
        data: Schema com email e selected_path
        db: Sessão do banco
    
    Returns:
        dict com mensagem de sucesso
        
    Raises:
        HTTPException: Se usuário não encontrado
    """
    # Buscar usuário pelo email
    user = db.query(User).filter(User.email == data.email).first()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found with this email"
        )
    
    # Atualizar selected_path
    user.selected_path = data.selected_path
    
    db.commit()
    db.refresh(user)
    
    logger.info(f"✅ Caminho atualizado para usuário {user.login} ({data.email}): {data.selected_path}")
    
    return {
        "message": "Selected path updated successfully",
        "updated_field": "selected_path",
        "user_id": user.id,
        "email": user.email,
        "selected_path": user.selected_path
    }


def update_test_results_service(data: UpdateTestResultsSchema, db: Session):
    """
    Atualiza os resultados dos testes do usuário usando email
    
    Args:
        data: Schema com email e test_results
        db: Sessão do banco
    
    Returns:
        dict com mensagem de sucesso
        
    Raises:
        HTTPException: Se usuário não encontrado
    """
    # Buscar usuário pelo email
    user = db.query(User).filter(User.email == data.email).first()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found with this email"
        )
    
    # Converter TestResultsSchema para dict com espaços nos nomes
    test_results_dict = data.test_results.to_dict()
    
    # Atualizar test_results
    user.test_results = test_results_dict
    
    db.commit()
    db.refresh(user)
    
    logger.info(f"✅ Resultados dos testes atualizados para usuário {user.login} ({data.email})")
    logger.debug(f"Valores: {test_results_dict}")
    
    return {
        "message": "Test results updated successfully",
        "updated_field": "test_results",
        "user_id": user.id,
        "email": user.email,
        "test_results": user.test_results
    }


def update_progress_service(data: UpdateProgressSchema, db: Session):
    """
    Atualiza o progresso do usuário (semana e dia) usando email
    
    Args:
        data: Schema com email e progress (semana, dia)
        db: Sessão do banco
    
    Returns:
        dict com mensagem de sucesso e dados atualizados
        
    Raises:
        HTTPException: Se usuário não encontrado
    """
    # Buscar usuário pelo email
    user = db.query(User).filter(User.email == data.email).first()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found with this email"
        )
    
    # Preparar dados de progresso
    progress_dict = {
        "semana": data.progress.semana,
        "dia": data.progress.dia
    }
    
    # Atualizar progress e progress_updated_at
    user.progress = progress_dict
    user.progress_updated_at = datetime.utcnow()
    
    db.commit()
    db.refresh(user)
    
    logger.info(f"✅ Progresso atualizado para usuário {user.login} ({data.email}): Semana {data.progress.semana}, Dia {data.progress.dia}")
    
    return {
        "message": "Progress updated successfully",
        "user_id": user.id,
        "email": user.email,
        "progress": user.progress,
        "progress_updated_at": user.progress_updated_at.isoformat()
    }


def get_user_data_service(data: GetUserDataSchema, db: Session):
    """
    Busca dados completos do usuário usando email (selected_path e test_results)
    
    Args:
        data: Schema com email
        db: Sessão do banco
    
    Returns:
        dict com dados do usuário
        
    Raises:
        HTTPException: Se usuário não encontrado
    """
    user = db.query(User).filter(User.email == data.email).first()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found with this email"
        )
    
    return {
        "user_id": user.id,
        "login": user.login,
        "email": user.email,
        "selected_path": user.selected_path,
        "test_results": user.test_results,
        "progress": user.progress
    }