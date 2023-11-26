import uuid
import re
from typing import Optional

from fastapi import HTTPException
from pydantic import BaseModel, EmailStr, field_validator, constr

# Регулярное выражение для проверки наличия только букв в строке
LETTER_MATCH_PATTERN = re.compile(r"^[а-яА-Яa-zA-Z\-]+$")


# Базовый класс модели, настроенный для конвертации даже не словарных объектов в JSON
class TunnedModel(BaseModel):
    class Config:
        """Tells pydantic to convert even non dict obj to json"""

        from_attributes = True


# Модель для отображения пользователя
class ShowUser(TunnedModel):
    user_id: uuid.UUID
    f_name: str
    l_name: str
    email: EmailStr
    is_active: bool


# Модель для создания нового пользователя
class UserCreate(BaseModel):
    f_name: str
    l_name: str
    email: EmailStr

    # Валидатор для поля f_name, проверяющий, содержит ли строка только буквы
    @field_validator("f_name")
    def validate_f_name(cls, value):
        if not LETTER_MATCH_PATTERN.match(value):
            raise HTTPException(
                status_code=422, detail="First name should contains only letters"
            )
        return value

    # Валидатор для поля l_name, проверяющий, содержит ли строка только буквы
    @field_validator("l_name")
    def validate_l_name(cls, value):
        if not LETTER_MATCH_PATTERN.match(value):
            raise HTTPException(
                status_code=422, detail="Last name should contains only letters"
            )
        return value


class DeleteUserResponse(BaseModel):
    deleted_user_id: uuid.UUID


class UpdateUserResponse(BaseModel):
    updated_user_id: uuid.UUID


class UpdateUserRequest(BaseModel):
    f_name: Optional[constr(min_length=1)] = None
    l_name: Optional[constr(min_length=1)] = None
    email: Optional[EmailStr] = None

    # Валидатор для поля f_name, проверяющий, содержит ли строка только буквы
    @field_validator("f_name")
    def validate_f_name(cls, value):
        if not LETTER_MATCH_PATTERN.match(value):
            raise HTTPException(
                status_code=422, detail="First name should contains only letters"
            )
        return value

    # Валидатор для поля l_name, проверяющий, содержит ли строка только буквы
    @field_validator("l_name")
    def validate_l_name(cls, value):
        if not LETTER_MATCH_PATTERN.match(value):
            raise HTTPException(
                status_code=422, detail="Last name should contains only letters"
            )
        return value
