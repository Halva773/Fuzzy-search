import uuid

from fastapi import FastAPI, HTTPException, Depends, Response
from sqlalchemy.orm import Session

from db.database import init_db
# from schemas.corpus import New_corpus
# from db import redis_connection as red
# from services.text_processing import text_processing

from schemas.auth import SignUpRequest, UserResponse
from cruds.user_crud import user_exists, create_user, get_user_access
from schemas.corpus import New_corpus
from services.auth import create_access_token, get_current_user
from db.__init__ import get_db
from services.text_processing import TextProcessing, add_corpus

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
def sign_up(request: SignUpRequest, response: Response, db: Session = Depends(get_db)):
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
    if user_exists(db, request.email):
        return HTTPException(status_code=400, detail="Пользователь уже зарегистрирован")
    new_user = create_user(db, request)
    token = create_access_token(data={"user_id": new_user.user_id})
    response.set_cookie(key="access_token", value=token, httponly=True)
    return {"id": new_user.user_id, "email": new_user.email, "token": token}


@app.post("/login/",
          tags=['Аккаунт'],
          summary="Вход в аккаунт")
def login(request: SignUpRequest, response: Response, db: Session = Depends(get_db)):
    """
    Проверяет существование пользователя с указанным email. Проверяет правильность введенного пароля. Если все верно, генерирует новый токен для пользователя. Возвращает данные пользователя с новым токеном.

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
    user = get_user_access(db, request)
    if not bool(user):
        return HTTPException(status_code=401, detail="Неправильные данные для входа")
    token = create_access_token(data={"user_id": user.user_id})
    response.set_cookie(key="access_token", value=token, httponly=True)

    return{
        "id": user.user_id,
        "email": user.email,
        "token": token
    }


@app.get(
    "/users/me/",
    response_model=UserResponse,
    tags=["Аккаунт"],
    summary="Получение информации о текущем пользователе"
)
def read_current_user(current_user=Depends(get_current_user)):
    """
    Возвращает данные авторизованного пользователя.
    Для доступа требуется передать токен в заголовке Authorization.

    Пример ответа:
    {
      "id": 1,
      "email": "user@example.com"
    }
    """
    return current_user


@app.post("/upload_corpus")
def upload_corpus(request: New_corpus, db: Session = Depends(get_db)):
    """
    Загружает корпус текста для индексации и поиска.

    Пример запроса:
    {
        "corpus_name": "example_corpus",
        "text": "This is a sample text for the corpus."
    }
    Пример ответа:
    {
        "corpus_id": 1,
        "message": "Corpus uploaded successfully"
    }
    """
    corpus = add_corpus(db, request)
    return {
        "corpus_id": corpus.corpus_id,
        "message": "Corpus uploaded successfully"
    }
