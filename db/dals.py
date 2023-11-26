from uuid import UUID

from sqlalchemy import update, and_, select
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

    async def delete_user(self, user_id: UUID) -> UUID | None:
        query = update(User). \
            where(and_(User.user_id == user_id, User.is_active == True)). \
            values(is_active=False).\
            returning(User.user_id)
        res = await self.db_session.execute(query)
        deleted_user_id_row = res.fetchone()
        if deleted_user_id_row is not None:
            return deleted_user_id_row[0]

    async def get_user_by_id(self, user_id: UUID) -> User | None:
        query = select(User).\
            where(User.user_id == user_id)
        res = await self.db_session.execute(query)
        user_row = res.fetchone()
        if user_row is not None:
            return user_row[0]

    async def update_user(self, user_id: UUID, **kwargs) -> UUID | None:
        query = update(User).\
            where(and_(User.user_id == user_id, User.is_active == True)). \
            values(kwargs).\
            returning(User.user_id)
        res = await self.db_session.execute(query)
        update_user_id_row = res.fetchone()
        if update_user_id_row is not None:
            return update_user_id_row[0]
