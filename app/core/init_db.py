from sqlalchemy.orm import Session
from app.models.user import User
from app.core.database import SessionLocal, engine, Base
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# -------------------------------
# 🔹 Funções utilitárias
# -------------------------------

def get_db() -> Session:
    """Retorna uma sessão do banco."""
    return SessionLocal()


def hash_password(password: str) -> str:
    """Gera o hash seguro da senha."""
    return pwd_context.hash(password)


def create_user(db: Session, login: str, email: str, tag: str,plan: str,password: str):
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


def create_initial_users(db: Session):
    """Cria apenas os usuários iniciais, se o banco estiver vazio."""
    initial_users = [
        {"login": "dieghonm", "email": "dieghonm@gmail.com", "tag": "admin", "password": "Admin123@"},
        {"login": "cavamaga", "email": "cava.maga@gmail.com", "tag": "admin", "password": "Admin123@"},
        {"login": "tiaguetevital", "email": "tiagovital999@gmail.com", "tag": "admin", "password": "Admin123@"},
    ]

    for u in initial_users:
        create_user(
            db=db,
            login=u["login"],
            email=u["email"],
            tag=u["tag"],
            plan=u["tag"],
            password=u["password"],
        )

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
            print("✔ Banco já possui usuários. Nada a fazer.")
            return

        print("📌 Banco vazio. Criando usuários iniciais...")
        create_initial_users(db)
        db.commit()

        print("✔ Usuários iniciais criados com sucesso!")

    except Exception as e:
        db.rollback()
        print(f"❌ Erro ao inicializar banco: {e}")

    finally:
        db.close()


# Execução direta
if __name__ == "__main__":
    init_db()
    