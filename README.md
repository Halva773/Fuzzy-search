# Нечеткий поиск

![Alt](https://repobeats.axiom.co/api/embed/d548e6048342d76888356f912d6991d3a418b5ae.svg "Repobeats analytics image")

## Этапы реализации

1. Базовая реализация с использованием HTTP-протоколов (GET, POST)
2. Интеграция веб-сокетов для real-time взаимодействия
3. Внедрение Redis и Celery для асинхронного выполнения задач

## Общие требования к проектам

- Использование FastAPI в качестве веб-фреймворка
- SQLite как база данных
- SQLAlchemy для ORM (Object-Relational Mapping)
- Реализация авторизации по email и паролю
- Аутентификация с использованием JWT (JSON Web Tokens)

## Структура проекта

project/<br>
├── app/<br>
│   ├── api/           # эндпоинты<br>
│   ├── core/          # config <br>
│   ├── db/            # файл базы данных и сессия подключения <br>
│   ├── models/        # модели для базы данных<br>
│   ├── cruds/         # ORM CRUD операции<br>
│   ├── schemas/       # схемы запросов <br>
│   ├── services/      # доп. сервисы, в нашем случае тут будет лежать логика под лабы <br>
│   └── main.py<br>
├── alembic/<br>
└── .env<br>

## эндпоинты

### Регистрация нового пользователя
@router.post("/sign-up/")
Проверяет, не зарегистрирован ли уже пользователь с таким email.
Если нет, создает нового пользователя и генерирует для него токен.
Возвращает данные созданного пользователя.

### Вход в систему
@router.post("/login/")
Проверяет существование пользователя с указанным email.
Проверяет правильность введенного пароля.
Если все верно, генерирует новый токен для пользователя.
Возвращает данные пользователя с новым токеном.

### Получение информации о текущем пользователе
@router.get("/users/me/")
Возвращает данные авторизованного пользователя.

Данные о пользователе должны сохраняться в базу данных для чего вам надо написать круды.
Необходимо пользоваться alembic для миграции базы данных.

### Другие

@app.post("/upload_corpus")<br>
Загружает корпус текста для индексации и поиска.

@app.get("/corpuses")<br>
Возвращает список корпусов c идентификаторами.

@app.post("/search_algorithm")<br>
Позволяет указать слово (для поиска), тип алгоритма (которым можно искать), корпус (который можно использовать) и возвращает время работы алгоритма + результат поиска.


## Тема работы
Алгоритмы нечеткого поиска (также известного как поиск по сходству или fuzzy string search) являются основой систем проверки орфографии и полноценных поисковых систем вроде Google или Yandex. Например, такие алгоритмы используются для функций наподобие «Возможно вы имели в виду …» в тех же поисковых системах.
[К ознакомлению](https://habr.com/ru/articles/114997/)

Будет реализовано 2 алгоритма из списка:
- Расстояние Левенштейна
- Расстояние Дамерау-Левенштейна
- Алгоритм Bitap с модификациями от Wu и Manber
- Алгоритм расширения выборки
- Метод N-грамм
- Хеширование по сигнатуре
- BK-деревья


## Курсы по fast api
[Артем Шумейко](https://youtube.com/playlist?list=PLuW7Z72R04bi313KhHamabibc8JW2HDU3&si=pw4q-OImqdknAo7c)  <br>
[Программирование и иже с ним(смотреть на свой страх и риск, но чувак сильный)](https://youtube.com/playlist?list=PLeLN0qH0-mCVQKZ8-W1LhxDcVlWtTALCS&si=swC88v6orGsczS0S)
