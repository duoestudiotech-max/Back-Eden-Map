from sqlalchemy.orm import Session
from app.models.user import User
from app.core.database import SessionLocal, engine, Base
from passlib.context import CryptContext
from app.services.email_service import get_email_service
import logging

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
logger = logging.getLogger('app.core.init_db')


# -------------------------------
# 🔹 Funções utilitárias
# -------------------------------

def get_db() -> Session:
    """Retorna uma sessão do banco."""
    return SessionLocal()


def hash_password(password: str) -> str:
    """Gera o hash seguro da senha."""
    return pwd_context.hash(password)


def create_user(db: Session, login: str, email: str, tag: str, plan: str, password: str):
    """Cria um usuário no banco."""
    hashed_password = hash_password(password)

    user = User(
        login=login,
        email=email,
        tag=tag,
        plan=plan,
        password=hashed_password
    )

    db.add(user)
    return user


def send_welcome_email(email: str, login: str, plan: str) -> bool:
    """
    Envia email de boas-vindas para o usuário
    
    Args:
        email: Email do usuário
        login: Login do usuário
        plan: Plano do usuário
    
    Returns:
        True se enviado com sucesso, False caso contrário
    """
    try:
        email_service = get_email_service()
        
        if not email_service:
            logger.warning(f"⚠️  Serviço de email não configurado. Email para {email} não enviado.")
            return False
        
        email_enviado = email_service.enviar_boas_vindas(
            email=email,
            login=login,
            plan=plan
        )
        
        if email_enviado:
            logger.info(f"✅ Email de boas-vindas enviado para {email} (usuário inicial)")
            return True
        else:
            logger.warning(f"⚠️  Falha ao enviar email de boas-vindas para {email}")
            return False
            
    except Exception as e:
        logger.error(f"❌ Erro ao enviar email de boas-vindas para {email}: {str(e)}")
        return False


def create_initial_users(db: Session):
    """
    Cria apenas os usuários iniciais, se o banco estiver vazio.
    Também envia emails de boas-vindas para cada um.
    """
    initial_users = [
        {"login": "dieghonm", "email": "dieghonm@gmail.com", "tag": "admin", "password": "Admin123@"},
        {"login": "cavamaga", "email": "cava.maga@gmail.com", "tag": "admin", "password": "Admin123@"},
        {"login": "tiaguetevital", "email": "tiagovital999@gmail.com", "tag": "admin", "password": "Admin123@"},
    ]

    logger.info(f"📌 Criando {len(initial_users)} usuários iniciais...")
    
    emails_enviados = 0
    emails_falhados = 0
    
    for u in initial_users:
        # Criar usuário
        user = create_user(
            db=db,
            login=u["login"],
            email=u["email"],
            tag=u["tag"],
            plan=u["tag"],  # Plan = tag para admins
            password=u["password"],
        )
        
        logger.info(f"✔ Usuário criado: {u['login']} ({u['email']})")
        
        # Commit para garantir que o usuário foi criado
        db.commit()
        
        # Enviar email de boas-vindas
        email_enviado = send_welcome_email(
            email=u["email"],
            login=u["login"],
            plan=u["tag"]
        )
        
        if email_enviado:
            emails_enviados += 1
        else:
            emails_falhados += 1
    
    # Resumo do envio de emails
    logger.info("=" * 60)
    logger.info("📊 RESUMO DE ENVIO DE EMAILS:")
    logger.info(f"   ✅ Enviados com sucesso: {emails_enviados}")
    if emails_falhados > 0:
        logger.info(f"   ⚠️  Falharam: {emails_falhados}")
    logger.info("=" * 60)


def is_db_empty(db: Session) -> bool:
    """Retorna True se não houver usuários no banco."""
    return db.query(User).count() == 0


# -------------------------------
# 🔹 Função principal de inicialização
# -------------------------------

def init_db():
    """Inicializa banco, tabelas e cria usuários iniciais se necessário."""
    Base.metadata.create_all(bind=engine)
    db = get_db()

    try:
        if not is_db_empty(db):
            logger.info("✔ Banco já possui usuários. Nada a fazer.")
            return

        logger.info("📌 Banco vazio. Criando usuários iniciais...")
        create_initial_users(db)
        
        logger.info("✔ Usuários iniciais criados com sucesso!")

    except Exception as e:
        db.rollback()
        logger.error(f"❌ Erro ao inicializar banco: {e}")

    finally:
        db.close()


# Execução direta
if __name__ == "__main__":
    init_db()
    