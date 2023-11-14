from typing import Generator, Any
import pytest

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from starlette.testclient import TestClient

# Импорт настроек и FastAPI-приложения из соответствующих модулей
import settings
from main import app

import os
import asyncio
from db.session import get_db
import asyncpg

# Создание асинхронного движка SQLAlchemy для тестов с использованием настроек из settings.py
test_engine = create_async_engine(settings.TEST_DATABASE_URL, future=True, echo=True)
test_async_session = sessionmaker(test_engine, expire_on_commit=False, class_=AsyncSession)

# Таблицы, которые будут очищены перед выполнением тестов
CLEAN_TABLES = [
    "users",
]


# Фикстура для настройки асинхронного цикла событий в pytest
@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


# Фикстура для выполнения миграций перед запуском тестов
@pytest.fixture(scope="session", autouse=True)
async def run_migrations():
    os.system("alembic init migrations")
    os.system('alembic revision --autogenerate -m "test running migrations"')
    os.system("alembic upgrade heads")


# Фикстура для асинхронной сессии тестовой базы данных
@pytest.fixture(scope="session")
async def async_session_test():
    engine = create_async_engine(settings.TEST_DATABASE_URL, future=True, echo=True)
    async_session = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)
    yield async_session


# Фикстура для очистки таблиц перед выполнением каждого тестового случая
@pytest.fixture(scope="function", autouse=True)
async def clean_tables(async_session_test):
    """Clean data in all tables before running test function"""
    async with async_session_test() as session:
        async with session.begin():
            for table_for_cleaning in CLEAN_TABLES:
                await session.execute(f"""TRUNCATE TABLE {table_for_cleaning}""")


# Фикстура для создания тестового клиента FastAPI
@pytest.fixture(scope="function")
async def client() -> Generator[TestClient, Any, None]:
    """
    Create a new FastAPI TestClient that uses the `db_session` fixture to override
    the `get_db` dependency that is injected into rules
    """

    async def _get_test_db():
        try:
            yield test_async_session()
        finally:
            pass

    app.dependency_overrides[get_db] = _get_test_db
    with TestClient(app) as client:
        yield client


# Фикстура для создания пула соединений к тестовой базе данных с использованием asyncpg
@pytest.fixture(scope="session")
async def asyncpg_pool():
    pool = await asyncpg.create_pool("".join(settings.TEST_DATABASE_URL.split("+asyncpg")))
    yield pool
    pool.close()


# Фикстура для получения пользователя из тестовой базы данных по UUID
@pytest.fixture
async def get_user_from_database(asyncpg_pool):

    async def get_user_from_database_by_uuid(user_id: str):
        async with asyncpg_pool.acquire() as connection:
            return await connection.fetch("""SELECT * FROM users WHERE user_id = $1""", user_id)

    return get_user_from_database_by_uuid
