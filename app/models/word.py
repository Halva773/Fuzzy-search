from sqlalchemy import insert

class WordService:

    def add_word(self, db, word: str) -> None:
        """
        Добавляет слово в таблицу.
        Функция принимает строку, формирует SQL-запрос для вставки и выполняет его.
        """
        stmt = insert(self.word_table_manager.table).values(text=word)
        with self.engine.begin() as connection:
            connection.execute(stmt)


if __name__ == '__main__':
    db = WordService()
    db.add_word("слоны")
