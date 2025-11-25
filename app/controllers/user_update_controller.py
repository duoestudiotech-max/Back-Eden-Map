# app/controllers/user_update_controller.py
from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from app.schemas.user_update_schemas import (
    UpdateSelectedPathSchema, 
    UpdateTestResultsSchema, 
    UpdateProgressSchema,
    GetUserDataSchema
)
from app.services.user_update_service import (
    update_selected_path_service,
    update_test_results_service,
    update_progress_service,
    get_user_data_service
)


def update_selected_path_controller(data: UpdateSelectedPathSchema, db: Session):
    """
    Controller para atualizar selected_path usando email
    
    Args:
        data: Dados do caminho selecionado + email
        db: Sessão do banco
    
    Returns:
        dict com resultado da atualização
    """
    return update_selected_path_service(data, db)


def update_test_results_controller(data: UpdateTestResultsSchema, db: Session):
    """
    Controller para atualizar test_results usando email
    
    Args:
        data: Resultados dos testes + email
        db: Sessão do banco
    
    Returns:
        dict com resultado da atualização
    """
    return update_test_results_service(data, db)


def update_progress_controller(data: UpdateProgressSchema, db: Session):
    """
    Controller para atualizar progresso do usuário
    
    Args:
        data: Dados do progresso (email, semana, dia)
        db: Sessão do banco
    
    Returns:
        dict com resultado da atualização
    """
    return update_progress_service(data, db)


def get_user_data_controller(data: GetUserDataSchema, db: Session):
    """
    Controller para buscar dados do usuário usando email
    
    Args:
        data: Schema com email
        db: Sessão do banco
    
    Returns:
        dict com dados do usuário
    """
    return get_user_data_service(data, db)