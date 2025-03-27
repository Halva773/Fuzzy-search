from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from core.config import settings  # settings.DATABASE_URL должен содержать адрес вашей БД

SQLALCHEMY_DATABASE_URL = settings.DATABASE_URL

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False}  # Этот аргумент необходим для SQLite
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def init_db():
    """
    Импортируем все модели, чтобы они зарегистрировались в Base.metadata,
    и создаём таблицы, если их еще нет.
    """
    # Импорт моделей (необходимо, чтобы они появились в metadata)
    from models import user, word, corpus
    Base.metadata.create_all(bind=engine)
