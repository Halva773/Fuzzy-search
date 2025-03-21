from sqlalchemy import create_engine, MetaData, Table, Column, Integer, Text, Index, inspect, insert

from app.services.config import DATABASE_URL


class SingletonWordTable:
    _instance = None

    def __new__(cls, engine):
        if cls._instance is None:
            cls._instance = super(SingletonWordTable, cls).__new__(cls)
            cls._instance.init_table(engine)
        return cls._instance

    def init_table(self, engine):
        self.engine = engine
        self.metadata = MetaData()
        inspector = inspect(engine)
        if inspector.has_table('words'):
            self.table = Table('words', self.metadata, autoload_with=engine)
            print("Таблица 'words' уже существует и будет использована.")
        else:
            self.table = Table(
                'words',
                self.metadata,
                Column('id', Integer, primary_key=True, autoincrement=True),
                Column('text', Text, nullable=False, unique=True),
                Index('ix_text', 'text')
            )
            # Создаём таблицу в базе данных
            self.metadata.create_all(engine)
            print("Таблица 'words' не существовала, поэтому создана новая таблица.")


engine = create_engine(DATABASE_URL)
word_table = SingletonWordTable(engine)

# Пример использования:
if __name__ == '__main__':
    word_table1 = SingletonWordTable(engine)
