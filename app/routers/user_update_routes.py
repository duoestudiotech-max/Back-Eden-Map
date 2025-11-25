# app/routers/user_update_routes.py
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas.user_update_schemas import (
    UpdateSelectedPathSchema,
    UpdateTestResultsSchema,
    GetUserDataSchema,
    UserUpdateResponse
)
from app.controllers.user_update_controller import (
    update_selected_path_controller,
    update_test_results_controller,
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
            "progress": {...}
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