from time import time

from sqlalchemy.orm import Session

from schemas.fuzzy_search import RequestModel
from services.fuzzy_search.levenshtein_distance import count_levenshtein_distances


def run_search_algorithm(request: RequestModel, db: Session):
    start = time()
    if request.algorithm == "levenshtein":
        result = count_levenshtein_distances(request.word, request.corpus_id, db)
    else:
        result = False
    end = time()
    return result, end - start
