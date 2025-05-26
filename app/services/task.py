import time
from sqlalchemy.orm import Session
from celery_app import celery_app
from db import SessionLocal
from db.database import init_db
from services.fuzzy_search.run_search import (
    count_levenshtein_distances,
    count_signature_distances
)


@celery_app.task(bind=True)
def fuzzy_search_task(self, word: str, algorithm: str, corpus_id: int):
    self.update_state(
        state='STARTED',
        meta={'word': word, 'algorithm': algorithm}
    )
    start_time = time.time()
    init_db()

    db: Session = SessionLocal()

    if algorithm == "levenshtein":
        all_results = count_levenshtein_distances(word, corpus_id, db=db)
    elif algorithm == "signature":
        all_results = count_signature_distances(word, corpus_id, db=db)
    else:
        raise ValueError("Unknown algorithm")

    # total = len(all_results)

    # for idx, item in enumerate(all_results, start=1):
    #     if idx % max(1, total // 20) == 0:
    #         progress = int(idx / total * 100)
    #         self.update_state(
    #             state='PROGRESS',
    #             meta={
    #                 'progress': progress,
    #                 'current_word': f"processing word {idx}/{total}"
    #             }
    #         )

    execution_time = round(time.time() - start_time, 4)
    return {
        'execution_time': execution_time,
        'results': all_results
    }
