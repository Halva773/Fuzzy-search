from sqlalchemy.orm import Session
from models.word import Word


def compute_signature(word: str) -> int:
    """
    Вычисляет сигнатуру слова в виде битовой маски для букв a-z.
    Например, для слова "bad" будут установлены биты для букв b, a и d.
    """
    signature = 0
    for c in word.lower():
        if 'a' <= c <= 'z':  # учитываем только английские буквы
            pos = ord(c) - ord('a')
            signature |= (1 << pos)
    return signature


def hamming_distance(sig1: int, sig2: int) -> int:
    """
    Вычисляет расстояние Хэмминга между двумя целыми числами,
    то есть количество битов, в которых они различаются.
    """
    return bin(sig1 ^ sig2).count("1")


def count_signature_distances(query_word: str, corpus_id: int, db: Session):
    """
    Извлекает все слова из таблицы Word для заданного corpus_id, вычисляет их сигнатуры и
    расстояние Хэмминга между сигнатурой искомого слова и сигнатурой каждого слова корпуса.
    Возвращает список слов с расстоянием, отсортированный по возрастанию расстояния.
    """
    # Вычисляем сигнатуру искомого слова
    query_signature = compute_signature(query_word)

    # Получаем все слова для данного корпуса
    corpus_words = db.query(Word).filter(Word.corpus_id == corpus_id).all()

    results = []
    for corpus_word in corpus_words:
        # Вычисляем сигнатуру слова из корпуса
        word_signature = compute_signature(corpus_word.word)
        dist = hamming_distance(query_signature, word_signature)
        results.append({
            "word": corpus_word.word,
            "distance": dist
        })

    # Сортируем результаты по расстоянию (наименьшее расстояние в начале)
    results.sort(key=lambda x: x["distance"])
    return results