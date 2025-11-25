# app/services/user_update_service.py
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
import logging

from app.models.user import User
from app.schemas.user_update_schemas import UpdateSelectedPathSchema, UpdateTestResultsSchema, GetUserDataSchema

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