from sqlalchemy.ext.asyncio import AsyncSession
from db.models import User


class UserDAL:
    """Data Access Layer for operating user info"""

    def __init__(self, db_session: AsyncSession):
        self.db_session: AsyncSession = db_session

    async def create_user(self, f_name: str, l_name: str, email: str) -> User:
        new_user = User(
            f_name=f_name,
            l_name=l_name,
            email=email,
        )
        self.db_session.add(new_user)
        await self.db_session.flush()
        return new_user
