from sqlalchemy.orm import Session

from models.word import Word


def levenshtein_distance(s1: str, s2: str) -> int:
    """
    Вычисляет расстояние Левенштейна между строками s1 и s2.
    """
    if len(s1) < len(s2):
        return levenshtein_distance(s2, s1)
    if len(s2) == 0:
        return len(s1)

    previous_row = list(range(len(s2) + 1))
    for i, c1 in enumerate(s1):
        current_row = [i + 1]
        for j, c2 in enumerate(s2):
            insertions = previous_row[j + 1] + 1
            deletions = current_row[j] + 1
            substitutions = previous_row[j] + (c1 != c2)
            current_row.append(min(insertions, deletions, substitutions))
        previous_row = current_row
    return previous_row[-1]


def count_levenshtein_distances(query_word: str, corpus_id: int, db: Session):
    """
    Извлекает все слова из таблицы Word для заданного corpus_id и
    вычисляет расстояние Левенштейна между query_word и каждым словом.

    Возвращает список слов с расстоянием, отсортированный по возрастанию расстояния.
    """
    # Получаем все слова для данного корпуса
    corpus_words = db.query(Word).filter(Word.corpus_id == corpus_id).all()

    results = []
    for corpus_word in corpus_words:
        dist = levenshtein_distance(query_word, corpus_word.word)
        results.append({
            "word": corpus_word.word,
            "distance": dist
        })

    # Сортируем результаты по расстоянию (от наименьшего к наибольшему)
    results.sort(key=lambda x: x["distance"])
    return results