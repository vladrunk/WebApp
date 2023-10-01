from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from api.models import UserCreate, ShowUser
from db.dals import UserDAL
from db.session import get_db


user_routrer = APIRouter()


async def _create_new_user(body: UserCreate, db) -> ShowUser:
    async with db as session:
        async with session.begin():
            user_dal = UserDAL(session)
            user = await user_dal.create_user(
                f_name=body.f_name,
                l_name=body.l_name,
                email=body.email,
            )
            return ShowUser(
                user_id=user.user_id,
                f_name=user.f_name,
                l_name=user.l_name,
                email=user.email,
                is_active=user.is_active
            )


@user_routrer.post("/", response_model=ShowUser)
async def create_user(body: UserCreate, db: AsyncSession = Depends(get_db)) -> ShowUser:
    return await _create_new_user(body, db)
