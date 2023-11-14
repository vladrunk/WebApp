from sqlalchemy.ext.asyncio import AsyncSession
from db.models import User


# Класс UserDAL представляет собой Data Access Layer (DAL) для работы с информацией о пользователях
class UserDAL:
    """Data Access Layer for operating user info"""

    # Инициализация объекта UserDAL сессией базы данных
    def __init__(self, db_session: AsyncSession):
        self.db_session: AsyncSession = db_session

    # Асинхронный метод для создания нового пользователя в базе данных
    async def create_user(self, f_name: str, l_name: str, email: str) -> User:
        # Создание нового объекта пользователя с переданными данными
        new_user = User(
            f_name=f_name,
            l_name=l_name,
            email=email,
        )
        # Добавление нового пользователя в текущую сессию базы данных
        self.db_session.add(new_user)
        # Сохранение изменений в базе данных
        await self.db_session.flush()
        # Возврат созданного пользователя
        return new_user
