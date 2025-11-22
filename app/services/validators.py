from sqlalchemy.orm import Session
from app.models.user import User

def validate_user_exists(login: str, db: Session) -> bool:
    return db.query(User).filter(User.login == login).first() is not None

def validate_email_exists(email: str, db: Session) -> bool:
    return db.query(User).filter(User.email == email).first() is not None
