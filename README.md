## y_lab menus

### установка

1. создать виртуальное окружение ```python -m venv venv```
2. активировать виртуальное окружение ```source venv/bin/activate```
3. установка зависимостей ```pip install -r requirements.txt```

### запуск базы данных
1. использовать в корне проекта файл .env, в котором необходимо указать свои настройки для подключения к другим сервисам


### Запуск проекта
1. создание папки миграции ```alembic init migrations```
2. настроить файл /migrations/env.py
```from app.db.models import Base```
```target_metadata = Base.metadata```
3. настойка файла alembic.ini ```sqlalchemy.url = driver://user:pass@localhost/dbname```
4. инициалиция первых миграций ```alembic revision --autogenerate -m ""```
5. применение миграций в бд ```alembic upgrade head```
6. запуск приложения ```uvicorn app.main:app --reload```

### запуск docker
```shell
docker-compose up -d
```
### запуск тестов docker
```shell
docker-compose -f docker-compose-test.yaml up -d
```

## Дополнительные задания:
Обновление меню из google sheets раз в 15 сек. в папке app.celery.tasks.py
https://docs.google.com/spreadsheets/d/1CKvxZQWP8TwJUt0t-tFUFqKkhAsm9EkrHpxUk21JEKM/edit
в файле credentials.json специально убран ключ "client_secret", для его получения необходимо мне написать в личные сообщения на портале ylab
