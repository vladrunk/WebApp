import re
import uuid
from typing import Optional

from fastapi import HTTPException
from pydantic import BaseModel, EmailStr, field_validator, constr

LETTER_MATCH_PATTERN = re.compile(r"^[а-яА-Яa-zA-Z\-]+$")


class TunnedModel(BaseModel):
    class Config:
        """Tells pydantic to convert even non dict obj to json"""

        from_attributes = True


class ShowUser(TunnedModel):
    user_id: uuid.UUID
    f_name: str
    l_name: str
    email: EmailStr
    is_active: bool


class UserCreate(BaseModel):
    f_name: str
    l_name: str
    email: EmailStr

    @field_validator("f_name")
    def validate_f_name(cls, value):
        if not LETTER_MATCH_PATTERN.match(value):
            raise HTTPException(
                status_code=422, detail="First name should contains only letters"
            )
        return value

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

    @field_validator("f_name")
    def validate_f_name(cls, value):
        if not LETTER_MATCH_PATTERN.match(value):
            raise HTTPException(
                status_code=422, detail="First name should contains only letters"
            )
        return value

    @field_validator("l_name")
    def validate_l_name(cls, value):
        if not LETTER_MATCH_PATTERN.match(value):
            raise HTTPException(
                status_code=422, detail="Last name should contains only letters"
            )
        return value
