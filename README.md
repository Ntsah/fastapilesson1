FASTAPI ПРОЕКТ - ПОЛНАЯ ИНСТРУКЦИЯ УСТАНОВКИ
=============================================

1. УСТАНОВКА НЕОБХОДИМОГО ПО
----------------------------

1.1 Python 3.8+:
- Windows: скачайте с python.org
- Linux: sudo apt install python3 python3-pip python3-venv
- macOS: brew install python

1.2 Git:
- Скачайте с git-scm.com

1.3 PostgreSQL (опционально):
- Windows: установщик с postgresql.org
- Linux: sudo apt install postgresql
- macOS: brew install postgresql

2. НАСТРОЙКА ПРОЕКТА
-------------------

2.1 Клонирование репозитория:
git clone https://github.com/Ntsah/fastapilesson1.git
cd fastapilesson1

2.2 Виртуальное окружение:
- Windows:
  python -m venv venv
  venv\Scripts\activate
- Linux/macOS:
  python3 -m venv venv
  source venv/bin/activate

2.3 Зависимости:
pip install -r requirements.txt

3. БАЗА ДАННЫХ
-------------

3.1 SQLite (простой вариант):
Создайте файл .env с содержимым:
DATABASE_URL=sqlite:///./database.db

3.2 PostgreSQL:
1. Создайте БД и пользователя:
   sudo -u postgres psql
   CREATE DATABASE fastapi_db;
   CREATE USER fastapi_user WITH PASSWORD 'password';
   GRANT ALL PRIVILEGES ON DATABASE fastapi_db TO fastapi_user;
   \q

2. Добавьте в .env:
DATABASE_URL=postgresql://fastapi_user:password@localhost:5432/fastapi_db

4. Измените в backend/db.py
POSTGRES_USER = 'user'
POSTGRES_PASSWORD = 'password'
POSTGRES_HOST = 'localhost'
POSTGRES_PORT = 5432
POSTGRES_DB_NAME = 'db_name' 

5. МИГРАЦИИ
----------

4.1 Инициализация (если не было):
alembic init migrations

4.2 Настройка alembic.ini:
sqlalchemy.url = ${DATABASE_URL}

4.3 Первая миграция:
alembic revision --autogenerate -m "Initial"
alembic upgrade head

5. ЗАПУСК ПРИЛОЖЕНИЯ
-------------------

5.1 Разработка:
uvicorn main:app --reload

5.2 Продакшен:
uvicorn main:app --host 0.0.0.0 --port 8000

Доступные адреса:
- http://localhost:8000
- http://localhost:8000/docs
- http://localhost:8000/redoc

6. DOCKER
--------

6.1 Установите Docker Desktop

6.2 Сборка и запуск:
docker build -t fastapi-app .
docker run -d -p 8000:8000 fastapi-app

6.3 С PostgreSQL:
docker-compose up -d

7. ТЕХНОЛОГИИ
------------
- FastAPI
- SQLAlchemy
- Alembic
- Uvicorn
- PostgreSQL/SQLite

