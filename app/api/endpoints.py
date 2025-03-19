import uuid

from fastapi import FastAPI, HTTPException
from services.corpus import New_corpus
from db.redis_db import redis_connection as red

app = FastAPI(
    title="Fuzzy Search",
    docs_url="/api/docs",
    description="API app for Fuzzy Search",
    debug=True,
)

@app.get("/ping")
def is_alive():
    return "pong"



@app.post("/upload_corpus",
          tags=["Корпуса текстов"],
          summary="Загрузка корпуса текста")
def upload_corpus(new_corpus: New_corpus):
    try:
        corpus_id = str(uuid.uuid4())
        red.load_corpus({
            "id": corpus_id,
            "corpus_name": new_corpus.corpus_name,
            "text": new_corpus.text
        })
        return {
            "corpus_id": corpus_id,
            "message": "Corpus uploaded successfully"
        }
    except Exception as e:
        return HTTPException(status_code=400, detail=str(e))




@app.get("/corpuses",
         tags=['Корпуса текстов'],
         summary='Получить все корпуса текстов')
def get_corpuses():
    corpuses_list = red.get_all_corpuses()
    return {"corpuses": corpuses_list}

