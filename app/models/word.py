from sqlalchemy import insert
from db.sqlalchemy_config import SingletonWordTable
from db.sqlalchemy_config import engine, word_table

class WordService:
    def __init__(self, engine, word_table: SingletonWordTable):
        """
        При инициализации WordService создается экземпляр класса SingletonWordTable,
        который отвечает за проверку существования таблицы и её инициализацию.
        """
        # Инициализируем класс для работы с таблицей (создает или отражает таблицу 'words')
        self.word_table_manager = word_table
        self.engine = engine

    def add_word(self, word: str) -> None:
        """
        Добавляет слово в таблицу.
        Функция принимает строку, формирует SQL-запрос для вставки и выполняет его.
        """
        stmt = insert(self.word_table_manager.table).values(text=word)
        with self.engine.begin() as connection:
            connection.execute(stmt)


if __name__ == '__main__':
    db = WordService(engine, word_table)
    db.add_word("слоны")
