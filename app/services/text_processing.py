import re
from dataclasses import dataclass

from celery.worker.state import requests
from sqlalchemy.orm import Session

from models.corpus import Corpus


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

    def save_words_to_db(self, db):
        """
        Записывает каждое слово, полученное из split_text(), в базу данных.

        """
        for word in self._split_text():
            db.add_word(word)


def text_processing(db, text_id, corpus):
    text = TextProcessing(text_id, corpus)
    text.save_words_to_db(db)


def add_corpus(db: Session, request: Corpus):
    new_corpus = Corpus(corpus_name=request.corpus_name)
    db.add(new_corpus)
    db.commit()
    db.refresh(new_corpus)
    return new_corpus
