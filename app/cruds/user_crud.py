from sqlalchemy.orm import Session
from werkzeug.security import generate_password_hash
from app.models.user import User  # модель пользователя
from app.schemas.auth import SignUpRequest  # схема входящих данных при регистрации

def get_user_by_email(db: Session, email: str) -> User:
    """
    Возвращает пользователя по email, если он существует.
    """
    return db.query(User).filter(User.email == email).first()

def create_user(db: Session, user_in: SignUpRequest) -> User:
    """
    Создаёт нового пользователя. Пароль хешируется перед сохранением в БД.
    """
    hashed_password = generate_password_hash(user_in.password)
    user = User(email=user_in.email, hashed_password=hashed_password)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def user_exists(email: str) -> bool:
    return True if get_user_by_email(db, email) else False