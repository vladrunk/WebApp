from typing import Generator

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

import settings

# Создание асинхронного движка SQLAlchemy с использованием настроек из settings.py
engine = create_async_engine(settings.REAL_DATABASE_URL, future=True, echo=True)
# Создание фабрики сессий SQLAlchemy для асинхронной работы с базой данных
async_session = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)


# Асинхронная функция для получения сессии базы данных в виде генератора
async def get_db() -> Generator:
    """Dependency for getting async session"""
    try:
        # Создание новой асинхронной сессии
        session: AsyncSession = async_session()
        # Предоставление сессии в качестве контекстного менеджера
        yield session
    finally:
        # Асинхронное закрытие сессии при завершении работы с ней
        # noinspection PyUnboundLocalVariable
        await session.close()
