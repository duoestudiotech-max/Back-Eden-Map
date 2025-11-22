from fastapi import APIRouter, Depends, status, Request
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas.user_schemas import UserCreate, UserResponse, CreateUserResponse
from app.controllers.user_controller import (
    create_user_controller,
    get_user_controller,
    list_users_controller
)
from app.auth.dependencies import rate_limit_register

router = APIRouter(prefix="/users", tags=["users"])


@router.post(
    "/", 
    response_model=CreateUserResponse, 
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(rate_limit_register)]
)
def create_user_route(
    user: UserCreate, 
    request: Request,
    db: Session = Depends(get_db)
):
    """
    Cria um novo usuário e retorna tokens de autenticação
    
    **Rate Limit: 2 requisições por hora por IP**
    
    O usuário é criado e automaticamente recebe:
    - Access token (válido por 30 dias)
    - Refresh token (válido por 30 dias, renovável)
    
    Example:
        POST /users/
        {
            "login": "novousuario",
            "password": "Senha123@",
            "email": "novo@email.com",
            "tag": "client",
            "plan": "trial"
        }
        
        Response:
        {
            "access_token": "eyJhbGc...",
            "refresh_token": "a8f3k2j9...",
            "token_type": "bearer",
            "user": {
                "id": 4,
                "login": "novousuario",
                "email": "novo@email.com",
                "tag": "client",
                "plan": "trial"
            }
        }
    
    Errors:
        429: Too many registration attempts (excedeu 2 requisições/hora)
    """
    return create_user_controller(user, db, request)


@router.get("/{user_id}", response_model=UserResponse)
def get_user_route(user_id: int, db: Session = Depends(get_db)):
    """Busca um usuário por ID"""
    return get_user_controller(user_id, db)


@router.get("/", response_model=list[UserResponse])
def list_users_route(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Lista todos os usuários"""
    return list_users_controller(skip, limit, db)