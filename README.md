## y_lab menus

### установка 

1. создать виртуальное окружение ```python -m venv venv``` 
2. активировать виртуальное окружение ```source venv/bin/activate```
3. установка зависимостей ```pip install -r requirements.txt```

### запуск базы данных
1. создать в корне проекта файл database.env в котором необходимо указать 
(#смотреть файл config.py)
POSTGRES_USER=****
POSTGRES_PASSWORD=****
POSTGRES_DB=****
POSTGRES_HOST=****
POSTGRES_HOSTNAME=****
DATABASE_PORT=****
CLIENT_ORIGIN=****


### запуск проекта
1. создание папки миграции ```alembic init migrations```
2. инициалиция первый миграций ```alembic revision --autogenerate -m ""```
3. применений миграций в бд ```alembic upgrade head```
4. запуски приложения ```uvicorn app.main:app --reload```


