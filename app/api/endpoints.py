import uuid

from fastapi import FastAPI

app = FastAPI(
    title="Fuzzy Search",
    docs_url="/api/docs",
    description="API app for Fuzzy Search",
    debug=True,
)

@app.get("/ping")
def is_alive():
    return "pong"


@app.get("/upload_corpus")
def upload_corpus():
    try:
        corpus_id = str(uuid.uuid4())
        return {
            "corpus_id": corpus_id,
            "message": "Corpus uploaded successfully"
        }
    except Exception as e:
        return {"message": str(e)}




@app.get("/corpuses")
def get_corpuses():
    corpuses_list = [
        {"id": 1, "name": "example_corpus"},
        {"id": 2, "name": "another_corpus"}
    ]
    return {"corpuses": corpuses_list}

