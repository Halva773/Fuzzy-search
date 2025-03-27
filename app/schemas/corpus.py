from pydantic import BaseModel


class New_corpus(BaseModel):
    corpus_name: str
    text: str