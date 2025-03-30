from fastapi import FastAPI, HTTPException, Depends, Response
from sqlalchemy.orm import Session

from db.database import init_db
from models.corpus import Corpus

from schemas.auth import SignUpRequest, UserResponse
from cruds.user_crud import user_exists, create_user, get_user_access
from schemas.corpus import NewCorpus, CorpusesResponse
from schemas.fuzzy_search import RequestModel
from services.auth import create_access_token, get_current_user
from db.__init__ import get_db
from services.fuzzy_search.run_search import run_search_algorithm
from services.text_processing import add_corpus, add_words

app = FastAPI(
    title="Fuzzy Search",
    docs_url="/api/docs",
    description="API app for Fuzzy Search",
    debug=True,
)

init_db()


@app.get("/ping",
         tags=["Check status"])
def is_alive():
    return "pong"


@app.post("/sign-up/",
          tags=["Accounts"],
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
          tags=['Accounts'],
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

    return {
        "id": user.user_id,
        "email": user.email,
        "token": token
    }


@app.get(
    "/users/me/",
    response_model=UserResponse,
    tags=["Accounts"],
    summary="Получение информации о текущем пользователе"
)
def read_current_user(current_user=Depends(get_current_user)):
    """Возвращает данные авторизованного пользователя.

    Для доступа требуется передать токен в заголовке Authorization.

    Пример ответа:
    {
      "id": 1,
      "email": "user@example.com"
    }
    """
    return current_user


@app.post("/upload_corpus",
          tags=["Corpuses"],
          summary="Загружает корпус текста для индексации и поиска")
def upload_corpus(request: NewCorpus, db: Session = Depends(get_db)):
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
    add_words(db, corpus.corpus_id, request.text)
    return {
        "corpus_id": corpus.corpus_id,
        "message": "Corpus uploaded successfully"
    }


@app.get("/corpuses",
         tags=["Corpuses"],
         summary="Получить список корпусов текста",
         response_model=CorpusesResponse)
def get_corpuses(db: Session = Depends(get_db)):
    """
    Возвращает список корпусов с идентификаторами и названиями.

    Пример ответа:
    {
      "corpuses": [
         {"id": 1, "name": "example_corpus"},
         {"id": 2, "name": "another_corpus"}
      ]
    }
    """
    corpuses = db.query(Corpus).all()
    return {"corpuses": corpuses}


@app.post("/search_algorithm",
          tags=['Fuzzy search'],
          summary="Алгоритмы 'Расстояние Левенштейна' и '' для нечёткого поиска")
def search_algorithm(request: RequestModel, db: Session = Depends(get_db)):
    """
    Позволяет указать слово (для поиска), тип алгоритма (которым можно искать), корпус (который можно использовать) и возвращает время работы алгоритма + результат поиска.

    Пример запроса:
    {
        "word": "example",
        "algorithm": "levenshtein",
        "corpus_id": 1
    }

    Пример ответа:
    {
        "execution_time": 0.0023,
            "results": [
            {"word": "example", "distance": 0},
            {"word": "sample", "distance": 2}
            ]
    }
    """
    words, time = run_search_algorithm(request, db)
    if words == False:
        return HTTPException(status_code=401, detail="Этот алгоритм не подключён к приложению")
    return {
        "execution_time": time,
        "results": words
    }