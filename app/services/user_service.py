from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from passlib.context import CryptContext
import logging

from app.models.user import User
from app.schemas.user_schemas import UserCreate
from app.services.auth_service import generate_tokens_for_user
from app.services.email_service import get_email_service

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
logger = logging.getLogger('app.services.user_service')


def create_user_service(user: UserCreate, db: Session, ip_address: str = None, user_agent: str = None):
    """
    Cria um novo usuário e retorna tokens de autenticação
    Também envia email de boas-vindas
    
    Args:
        user: Dados do usuário a ser criado
        db: Sessão do banco de dados
        ip_address: IP do cliente (opcional)
        user_agent: User agent do cliente (opcional)
    
    Returns:
        dict com access_token, refresh_token e dados completos do usuário
    """
    hashed_password = pwd_context.hash(user.password)

    new_user = User(
        login=user.login,
        password=hashed_password,
        email=user.email,
        tag=user.tag or "client",
        plan=user.plan or "trial"
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    # Enviar email de boas-vindas
    try:
        email_service = get_email_service()
        if email_service:
            email_enviado = email_service.enviar_boas_vindas(
                email=new_user.email,
                login=new_user.login,
                plan=new_user.plan
            )
            
            if email_enviado:
                logger.info(f"✅ Email de boas-vindas enviado para {new_user.email}")
            else:
                logger.warning(f"⚠️  Falha ao enviar email de boas-vindas para {new_user.email}")
        else:
            logger.warning("⚠️  Serviço de email não configurado. Email de boas-vindas não enviado.")
    except Exception as e:
        # Não interromper criação do usuário se email falhar
        logger.error(f"❌ Erro ao enviar email de boas-vindas: {str(e)}")
    
    # Gerar tokens para o novo usuário (inclui todos os campos do usuário)
    tokens = generate_tokens_for_user(new_user, db, ip_address, user_agent)
    
    return tokens


def get_user_service(user_id: int, db: Session):
    """Busca um usuário por ID"""
    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    return user


def list_users_service(skip: int, limit: int, db: Session):
    """Lista usuários com paginação"""
    return db.query(User).offset(skip).limit(limit).all()