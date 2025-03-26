import uuid

from fastapi import FastAPI, HTTPException
from schemas.corpus import New_corpus
from db import redis_connection as red
from services.text_processing import text_processing
from cruds.user import User

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

        text_processing(corpus_id, new_corpus.text)

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


@app.post("/sign-up/",
          tags=["Аккаунт"],
          summary="Проверка и регистрация пользователя по email")
def sign_up(new_user: User):
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
    :return:
    """
    # Проверяем, существует ли уже пользователь
    if user_exists(request.email):
        raise HTTPException(status_code=400, detail="Пользователь уже зарегистрирован")
    # Создаем нового пользователя
    new_user = create_user(request.email, request.password)
    # Генерируем токен, например, включая идентификатор пользователя в payload
    token = create_access_token(data={"user_id": new_user.id})
    return {"id": new_user.id, "email": new_user.email, "token": token}

