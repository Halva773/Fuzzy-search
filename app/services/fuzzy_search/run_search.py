from time import time

from sqlalchemy.orm import Session

from schemas.fuzzy_search import RequestModel
from services.fuzzy_search.levenshtein_distance import count_levenshtein_distances
from services.fuzzy_search.signature_hash import count_signature_distances


def run_search_algorithm(request: RequestModel, db: Session):
    """
    Измеряет время выполнения алгоритма поиска и возвращает результаты поиска.
    В зависимости от параметра request.algorithm выбирается алгоритм:
      - "levenshtein" для расстояния Левенштейна,
      - "signature" для хеширования по сигнатуре.
    Если указан неизвестный алгоритм, возвращает False.
    """
    start = time()
    if request.algorithm == "levenshtein":
        result = count_levenshtein_distances(request.word, request.corpus_id, db)
    elif request.algorithm == "signature":
        result = count_signature_distances(request.word, request.corpus_id, db)
    else:
        result = False
    end = time()
    return result, end - start