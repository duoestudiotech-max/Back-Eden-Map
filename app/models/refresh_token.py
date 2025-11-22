# app/models/refresh_token.py
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.core.database import Base


class RefreshToken(Base):
    """Model para armazenar refresh tokens dos usuários"""
    __tablename__ = "refresh_tokens"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    token = Column(String, unique=True, nullable=False, index=True)
    
    # Controle de validade
    expires_at = Column(DateTime, nullable=False)
    is_revoked = Column(Boolean, default=False, nullable=False)
    
    # Metadados
    created_at = Column(DateTime, nullable=False, server_default=func.now())
    last_used_at = Column(DateTime, nullable=True)
    
    # Informações opcionais de segurança
    ip_address = Column(String, nullable=True)
    user_agent = Column(String, nullable=True)
    
    # Relacionamento com User
    user = relationship("User", backref="refresh_tokens")