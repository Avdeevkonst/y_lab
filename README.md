## y_lab menus

### установка 

1. создать виртуальное окружение ```python -m venv venv``` 
2. активировать виртуальное окружение ```source venv/bin/activate```
3. установка зависимостей ```pip install -r requirements.txt```

### запуск базы данных
1. создать в корне проекта файл database.env в котором необходимо указать 
(#смотреть файл config.py)
```
POSTGRES_USER=****
POSTGRES_PASSWORD=****
POSTGRES_DB=****
POSTGRES_HOST=****
POSTGRES_HOSTNAME=****
DATABASE_PORT=****
CLIENT_ORIGIN=****
```

### запуск проекта
1. создание папки миграции ```alembic init migrations```
2. настроить файл /migrations/env.py 
```from app.db.models import Base```
```target_metadata = Base.metadata```
3. настойка файла alembic.ini ```sqlalchemy.url = driver://user:pass@localhost/dbname```
3. инициалиция первый миграций ```alembic revision --autogenerate -m ""```
4. применений миграций в бд ```alembic upgrade head```
5. запуски приложения ```uvicorn app.main:app --reload```


### запуск docker 
docker-compose up -d
### запуск тестов docker
```shell
docker-compose -f docker-compose-test.yaml up -d
docker start -a fastapi_test_app
```