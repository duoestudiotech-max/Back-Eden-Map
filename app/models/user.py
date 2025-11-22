from sqlalchemy import Column, Integer, String, DateTime, JSON
from sqlalchemy.sql import func
from app.core.database import Base


class User(Base):
    __tablename__ = "users"

    # -----------------------------------------
    # Identificação
    # -----------------------------------------
    id = Column(Integer, primary_key=True, index=True)
    login = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)

    # -----------------------------------------
    # Credenciais
    # -----------------------------------------
    password = Column(String, nullable=False)

    # -----------------------------------------
    # Assinatura / Plano
    # -----------------------------------------
    tag = Column(String, nullable=False, default="client")
    plan = Column(String, nullable=False, default="trial")
    plan_date = Column(DateTime, nullable=False, default=func.now())

    # -----------------------------------------
    # Senha temporária
    # -----------------------------------------
    temp_password = Column(String, nullable=True, default=None)
    temp_password_expires = Column(DateTime, nullable=True, default=None)

    # -----------------------------------------
    # Dados do usuário (emocionais / caminhos)
    # -----------------------------------------
    selected_feelings = Column(JSON, nullable=True, default=None)
    selected_path = Column(String, nullable=True, default=None)
    test_results = Column(JSON, nullable=True, default=None)

    # -----------------------------------------
    # Progresso
    # -----------------------------------------
    progress = Column(JSON, nullable=True, default=None)
    progress_updated_at = Column(DateTime, nullable=True, default=None)

    # -----------------------------------------
    # Datas de sistema
    # -----------------------------------------
    created_at = Column(DateTime, nullable=False, server_default=func.now())
    updated_at = Column(DateTime, nullable=True, onupdate=func.now())