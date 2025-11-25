# app/routers/user_update_routes.py
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas.user_update_schemas import (
    UpdateSelectedPathSchema,
    UpdateTestResultsSchema,
    UpdateProgressSchema,
    GetUserDataSchema,
    UserUpdateResponse,
    ProgressResponse
)
from app.controllers.user_update_controller import (
    update_selected_path_controller,
    update_test_results_controller,
    update_progress_controller,
    get_user_data_controller
)

router = APIRouter(prefix="/users", tags=["user-updates"])


@router.post("/data")
def get_user_data_route(
    data: GetUserDataSchema,
    db: Session = Depends(get_db)
):
    """
    Busca dados completos do usuário usando email (selected_path, test_results, progress)
    
    Args:
        data: Objeto contendo email do usuário
    
    Returns:
        Dados completos do usuário
    
    Example:
        ```
        POST /users/data
        {
            "email": "usuario@email.com"
        }
        
        Response:
        {
            "user_id": 1,
            "login": "usuario",
            "email": "usuario@email.com",
            "selected_path": "Ansiedade",
            "test_results": {
                "Ansiedade": 20,
                "Atenção Plena": 20,
                "Autoimagem": 20,
                "Motivação": 20,
                "Relacionamentos": 20
            },
            "progress": {
                "semana": 3,
                "dia": 5
            }
        }
        ```
    
    Errors:
        404: User not found with this email
    """
    return get_user_data_controller(data, db)


@router.put(
    "/selected-path",
    response_model=UserUpdateResponse,
    status_code=status.HTTP_200_OK
)
def update_selected_path_route(
    data: UpdateSelectedPathSchema,
    db: Session = Depends(get_db)
):
    """
    Atualiza o caminho selecionado pelo usuário usando email
    
    **Valores válidos para selected_path:**
    - Ansiedade
    - Atenção Plena
    - Autoimagem
    - Motivação
    - Relacionamentos
    
    Args:
        data: Objeto com email e selected_path
    
    Returns:
        Confirmação da atualização
    
    Example:
        ```
        PUT /users/selected-path
        {
            "email": "usuario@email.com",
            "selected_path": "Ansiedade"
        }
        
        Response:
        {
            "message": "Selected path updated successfully",
            "updated_field": "selected_path",
            "user_id": 1,
            "email": "usuario@email.com",
            "selected_path": "Ansiedade"
        }
        ```
    
    Errors:
        400: Invalid selected_path value
        404: User not found with this email
    """
    return update_selected_path_controller(data, db)


@router.put(
    "/test-results",
    response_model=UserUpdateResponse,
    status_code=status.HTTP_200_OK
)
def update_test_results_route(
    data: UpdateTestResultsSchema,
    db: Session = Depends(get_db)
):
    """
    Atualiza os resultados dos testes do usuário usando email
    
    **Cada pontuação deve estar entre 0 e 100**
    
    Args:
        data: Objeto com email e test_results contendo 5 pontuações
    
    Returns:
        Confirmação da atualização
    
    Example:
        ```
        PUT /users/test-results
        {
            "email": "usuario@email.com",
            "test_results": {
                "Ansiedade": 20,
                "Atenção_Plena": 20,
                "Autoimagem": 20,
                "Motivação": 20,
                "Relacionamentos": 20
            }
        }
        
        Response:
        {
            "message": "Test results updated successfully",
            "updated_field": "test_results",
            "user_id": 1,
            "email": "usuario@email.com",
            "test_results": {
                "Ansiedade": 20,
                "Atenção Plena": 20,
                "Autoimagem": 20,
                "Motivação": 20,
                "Relacionamentos": 20
            }
        }
        ```
    
    **Nota:** No corpo da requisição use `Atenção_Plena` (com underscore),
    mas o banco salvará como `Atenção Plena` (com espaço).
    
    Errors:
        400: Invalid score values (must be 0-100)
        404: User not found with this email
    """
    return update_test_results_controller(data, db)


@router.put(
    "/progress",
    response_model=ProgressResponse,
    status_code=status.HTTP_200_OK
)
def update_progress_route(
    data: UpdateProgressSchema,
    db: Session = Depends(get_db)
):
    """
    Atualiza o progresso do usuário (semana e dia) usando email
    
    **Valores válidos:**
    - semana: 1 a 12
    - dia: 1 a 7
    
    Atualiza automaticamente o campo `progress_updated_at` com a data/hora atual.
    
    Args:
        data: Objeto com email e progress (contendo semana e dia)
    
    Returns:
        Confirmação da atualização com progresso e timestamp
    
    Example:
        ```
        PUT /users/progress
        {
            "email": "usuario@email.com",
            "progress": {
                "semana": 3,
                "dia": 5
            }
        }
        
        Response:
        {
            "message": "Progress updated successfully",
            "user_id": 1,
            "email": "usuario@email.com",
            "progress": {
                "semana": 3,
                "dia": 5
            },
            "progress_updated_at": "2025-11-25T14:30:00.123456"
        }
        ```
    
    Errors:
        400: Invalid semana (must be 1-12) or dia (must be 1-7)
        404: User not found with this email
    """
    return update_progress_controller(data, db)