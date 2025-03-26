from sqlalchemy import create_engine, MetaData, Table, Column, Integer, Text, Index, inspect
from app.core.config import settings  # Предположим, что settings.DATABASE_URL содержит адрес БД

# Создаем engine один раз для всего модуля
engine = create_engine(settings.DATABASE_URL, connect_args={"check_same_thread": False})
metadata = MetaData()

def get_word_table():
    """
    Функция возвращает объект таблицы 'words'. Если таблицы еще нет в БД,
    она создается.
    """
    inspector = inspect(engine)
    if inspector.has_table('words'):
        word_table = Table('words', metadata, autoload_with=engine)
        print("Таблица 'words' уже существует и будет использована.")
    else:
        word_table = Table(
            'words',
            metadata,
            Column('id', Integer, primary_key=True, autoincrement=True),
            Column('text', Text, nullable=False, unique=True),
            Index('ix_text', 'text')
        )
        metadata.create_all(engine)
        print("Таблица 'words' не существовала, поэтому создана новая таблица.")
    return word_table

# Инициализация таблицы при импорте модуля (опционально)
word_table = get_word_table()
