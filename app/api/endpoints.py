import uuid

from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session

from db.database import init_db
# from schemas.corpus import New_corpus
# from db import redis_connection as red
# from services.text_processing import text_processing

from schemas.auth import SignUpRequest
from cruds.user_crud import user_exists, create_user
from services.auth import create_access_token
from db.__init__ import get_db

app = FastAPI(
    title="Fuzzy Search",
    docs_url="/api/docs",
    description="API app for Fuzzy Search",
    debug=True,
)

init_db()

@app.get("/ping")
def is_alive():
    return "pong"



# @app.post("/upload_corpus",
#           tags=["Корпуса текстов"],
#           summary="Загрузка корпуса текста")
# def upload_corpus(new_corpus: New_corpus, db: Session = Depends(get_db)):
#     try:
#         corpus_id = str(uuid.uuid4())
#         red.load_corpus({
#             "id": corpus_id,
#             "corpus_name": new_corpus.corpus_name,
#             "text": new_corpus.text
#         })
#
#         text_processing(db, corpus_id, new_corpus.text)
#
#         return {
#             "corpus_id": corpus_id,
#             "message": "Corpus uploaded successfully"
#         }
#     except Exception as e:
#         return HTTPException(status_code=400, detail=str(e))
#
#
#
#
# @app.get("/corpuses",
#          tags=['Корпуса текстов'],
#          summary='Получить все корпуса текстов')
# def get_corpuses():
#     corpuses_list = red.get_all_corpuses()
#     return {"corpuses": corpuses_list}


@app.post("/sign-up/",
          tags=["Аккаунт"],
          summary="Проверка и регистрация пользователя по email")
def sign_up(request: SignUpRequest, db: Session = Depends(get_db)):
    """
    Проверяет, не зарегистрирован ли уже пользователь с таким email. Если нет, создает нового пользователя и генерирует
    для него токен. Возвращает данные созданного пользователя.

    Пример запроса:
    {
        "email": "user@example.com",
        "password": "securepassword123"
    }

    Пример ответа:
    {
        "id": 1,
        "email": "user@example.com",
        "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
    }
    """
    # Проверяем, существует ли уже пользователь
    if user_exists(db, request.email):
        return HTTPException(status_code=400, detail="Пользователь уже зарегистрирован")
    print("User not exists")
    # Создаем нового пользователя
    new_user = create_user(db, request)
    # Генерируем токен, например, включая идентификатор пользователя в payload
    token = create_access_token(data={"user_id": new_user.user_id})
    return {"id": new_user.user_id, "email": new_user.email, "token": token}