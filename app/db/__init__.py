from db.database import SessionLocal

def get_db():
    """
    Зависимость для получения сессии базы данных.
    Сессия создается, используется, а затем закрывается.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()