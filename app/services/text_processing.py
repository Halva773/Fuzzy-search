import re
from dataclasses import dataclass
from db.database import word_table, engine
from models.word import WordService


@dataclass(frozen=True)
class TextProcessing:
    text_name: str
    text: str
    """
    Класс для обработки корпуса текста: разбиение на слова, удаление знаков препинания
    и запись полученных слов в базу данных.

    Для экономии памяти используется генератор, который по одному возвращает слова.
    """

    def _split_text(self):
        """
        Разбивает текст на слова, удаляя знаки препинания.
        Возвращает генератор, который выдаёт слова в нижнем регистре.
        """
        pattern = re.compile(r'\b\w+\b', re.UNICODE)
        return (match.group().lower() for match in pattern.finditer(self.text))

    def save_words_to_db(self, word_table):
        """
        Записывает каждое слово, полученное из split_text(), в базу данных.

        :param word_table: экземпляр класса для работы с таблицей слов (например, SingletonWordTable)
        """
        db = WordService(engine, word_table)
        for word in self._split_text():
            db.add_word(word)


def text_processing(db, text_id, corpus):
    text = TextProcessing(text_id, corpus)
    text.save_words_to_db(word_table)

if __name__ == '__main__':
    text = TextProcessing(1, "текст? большой/маленький!")
    text.save_words_to_db(word_table)
