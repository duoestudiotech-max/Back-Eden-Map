from datetime import datetime, timedelta
from jose import jwt, JWTError
from sqlalchemy.orm import Session
from passlib.context import CryptContext
import secrets

from app.models.user import User
from app.models.refresh_token import RefreshToken
from app.core.config import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Constantes
REFRESH_TOKEN_EXPIRE_DAYS = 30


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verifica se a senha está correta"""
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(data: dict) -> str:
    """Cria um token JWT de acesso"""
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire, "type": "access"})
    
    encoded_jwt = jwt.encode(
        to_encode, 
        settings.SECRET_KEY, 
        algorithm=settings.ALGORITHM
    )
    return encoded_jwt


def create_refresh_token(user_id: int, db: Session, ip_address: str = None, user_agent: str = None) -> str:
    """
    Cria um refresh token único e armazena no banco
    
    Args:
        user_id: ID do usuário
        db: Sessão do banco de dados
        ip_address: IP do cliente (opcional)
        user_agent: User agent do cliente (opcional)
    
    Returns:
        String do refresh token
    """
    # Gerar token único e seguro
    token = secrets.token_urlsafe(64)
    
    # Calcular data de expiração (30 dias)
    expires_at = datetime.utcnow() + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
    
    # Criar registro no banco
    refresh_token = RefreshToken(
        user_id=user_id,
        token=token,
        expires_at=expires_at,
        ip_address=ip_address,
        user_agent=user_agent
    )
    
    db.add(refresh_token)
    db.commit()
    db.refresh(refresh_token)
    
    return token


def revoke_user_tokens(user_id: int, db: Session, except_token: str = None):
    """
    Revoga todos os refresh tokens de um usuário
    
    Args:
        user_id: ID do usuário
        db: Sessão do banco
        except_token: Token a ser mantido ativo (opcional)
    """
    query = db.query(RefreshToken).filter(
        RefreshToken.user_id == user_id,
        RefreshToken.is_revoked == False
    )
    
    if except_token:
        query = query.filter(RefreshToken.token != except_token)
    
    query.update({"is_revoked": True})
    db.commit()


def validate_refresh_token(token: str, db: Session):
    """
    Valida um refresh token e retorna o usuário associado
    
    Args:
        token: String do refresh token
        db: Sessão do banco de dados
    
    Returns:
        User object se válido, None caso contrário
    """
    # Buscar token no banco
    refresh_token = db.query(RefreshToken).filter(
        RefreshToken.token == token,
        RefreshToken.is_revoked == False
    ).first()
    
    if not refresh_token:
        return None
    
    # Verificar se expirou
    if refresh_token.expires_at < datetime.utcnow():
        refresh_token.is_revoked = True
        db.commit()
        return None
    
    # Atualizar último uso
    refresh_token.last_used_at = datetime.utcnow()
    
    # Renovar data de expiração (adiciona mais 30 dias)
    refresh_token.expires_at = datetime.utcnow() + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
    
    db.commit()
    
    # Retornar usuário associado
    return refresh_token.user


def authenticate_user(login: str, password: str, db: Session):
    """
    Autentica o usuário verificando login e senha
    
    Returns:
        User object se autenticado, None caso contrário
    """
    user = db.query(User).filter(User.login == login).first()
    
    if not user:
        return None
    
    if not verify_password(password, user.password):
        return None
    
    return user


def serialize_user_data(user: User) -> dict:
    """
    Serializa os dados do usuário para resposta JSON
    Converte campos JSON e datetime para formatos adequados
    
    Args:
        user: Objeto User do SQLAlchemy
    
    Returns:
        dict com dados completos do usuário
    """
    return {
        "id": user.id,
        "login": user.login,
        "email": user.email,
        "tag": user.tag,
        "plan": user.plan,
        "plan_date": user.plan_date.isoformat() if user.plan_date else None,
        "selected_path": user.selected_path if user.selected_path else None,
        "selected_path": user.selected_path,
        "progress": user.progress if user.progress else None,
    }


def generate_tokens_for_user(user: User, db: Session, ip_address: str = None, user_agent: str = None):
    """
    Gera access token e refresh token para um usuário
    
    Returns:
        dict com access_token, refresh_token e dados do usuário
    """
    # Criar access token
    access_token = create_access_token(
        data={
            "sub": str(user.id),
            "login": user.login,
            "tag": user.tag
        }
    )
    
    # Criar refresh token
    refresh_token = create_refresh_token(
        user_id=user.id,
        db=db,
        ip_address=ip_address,
        user_agent=user_agent
    )
    
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
        "user": serialize_user_data(user)
    }


def login_service(login: str, password: str, db: Session, ip_address: str = None, user_agent: str = None):
    """
    Serviço de login que retorna tokens e dados do usuário
    
    Returns:
        dict com access_token, refresh_token e informações do usuário
    """
    user = authenticate_user(login, password, db)
    
    if not user:
        return None
    
    # Revogar tokens antigos do usuário (por segurança, manter apenas o novo)
    revoke_user_tokens(user.id, db)
    
    return generate_tokens_for_user(user, db, ip_address, user_agent)


def refresh_access_token_service(refresh_token: str, db: Session, ip_address: str = None, user_agent: str = None):
    """
    Serviço para renovar access token usando refresh token
    
    Args:
        refresh_token: String do refresh token
        db: Sessão do banco de dados
        ip_address: IP do cliente (opcional)
        user_agent: User agent do cliente (opcional)
    
    Returns:
        dict com novos tokens e dados do usuário, ou None se inválido
    """
    user = validate_refresh_token(refresh_token, db)
    
    if not user:
        return None
    
    # Gerar novos tokens
    return generate_tokens_for_user(user, db, ip_address, user_agent)