from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from api.models import UserCreate, ShowUser, DeleteUserResponse, UpdateUserResponse, UpdateUserRequest
from db.dals import UserDAL
from db.session import get_db

# Создание экземпляра APIRouter для маршрутов, связанных с пользователями
user_routrer = APIRouter()


# Асинхронная функция для создания нового пользователя
async def _create_new_user(body: UserCreate, db: AsyncSession) -> ShowUser:
    async with db as session:
        async with session.begin():
            # Инициализация Data Access Layer для работы с пользователями
            user_dal = UserDAL(session)
            # Формирование объекта ShowUser для ответа
            user = await user_dal.create_user(
                f_name=body.f_name,
                l_name=body.l_name,
                email=body.email,
            )
            # Формирование объекта ShowUser для ответа
            return ShowUser(
                user_id=user.user_id,
                f_name=user.f_name,
                l_name=user.l_name,
                email=user.email,
                is_active=user.is_active
            )


async def _delete_user(user_id: UUID, db: AsyncSession) -> UUID | None:
    async with db as session:
        async with session.begin():
            user_dal = UserDAL(session)
            deleted_user_id = await user_dal.delete_user(user_id=user_id)
            return deleted_user_id


async def _get_user_by_id(user_id: UUID, db: AsyncSession) -> ShowUser | None:
    async with db as session:
        async with session.begin():
            user_dal = UserDAL(session)
            user = await user_dal.get_user_by_id(user_id=user_id)
            if user is not None:
                return ShowUser(
                    user_id=user.user_id,
                    f_name=user.f_name,
                    l_name=user.l_name,
                    email=user.email,
                    is_active=user.is_active,
                )


async def _update_user(updated_user_params: dict, user_id: UUID, db: AsyncSession) -> UUID | None:
    async with db as session:
        async with session.begin():
            user_dal = UserDAL(session)
            updated_user_id = await user_dal.update_user(
                user_id=user_id,
                **updated_user_params
            )
            return updated_user_id


@user_routrer.get("/", response_model=ShowUser)
async def get_user_by_id(user_id: UUID, db: AsyncSession = Depends(get_db)) -> ShowUser:
    user = await _get_user_by_id(user_id, db)
    if user is None:
        raise HTTPException(status_code=404, detail=f"User with id {user_id} not found")
    return user


# Объявление маршрута для создания пользователя
@user_routrer.post("/", response_model=ShowUser)
async def create_user(body: UserCreate, db: AsyncSession = Depends(get_db)) -> ShowUser:
    # Вызов функции для создания нового пользователя и возврат результата
    return await _create_new_user(body, db)


@user_routrer.delete("/", response_model=DeleteUserResponse)
async def delete_user(user_id: UUID, db: AsyncSession = Depends(get_db)) -> DeleteUserResponse:
    deleted_user_id = await _delete_user(user_id, db)
    if deleted_user_id is None:
        raise HTTPException(status_code=404, detail=f"User with id {user_id} not found")
    return DeleteUserResponse(deleted_user_id=deleted_user_id)


@user_routrer.patch("/", response_model=UpdateUserResponse)
async def update_user_by_id(
        user_id: UUID, body: UpdateUserRequest, db: AsyncSession = Depends(get_db)
) -> UpdateUserResponse:
    updated_user_params = body.model_dump(exclude_none=True)
    if updated_user_params == {}:
        raise HTTPException(status_code=422, detail="At least one parameter for user update info should be provided")
    user = await _get_user_by_id(user_id=user_id, db=db)
    if user is None:
        raise HTTPException(status_code=404, detail=f"User with {user_id} not found")
    updated_user_by_id = await _update_user(updated_user_params=updated_user_params, user_id=user_id, db=db)
    return UpdateUserResponse(updated_user_id=updated_user_by_id)
