# region:IMPORTS
import uuid
import re
import settings
from fastapi import (
    FastAPI,
    HTTPException,
)
from fastapi.routing import APIRouter
import uvicorn
from pydantic import (
    BaseModel,
    EmailStr,
    field_validator,
)
from sqlalchemy import (
    Column,
    Boolean,
    String,
)
from sqlalchemy.ext.asyncio import (
    create_async_engine,
    AsyncSession,
)
from sqlalchemy.orm import (
    sessionmaker,
    declarative_base,
)
from sqlalchemy.dialects.postgresql import UUID

# endregion

# region:BLOCK FOR COMMON INTERACTION WITH DATABASE
engine = create_async_engine(settings.REAL_DATABASE_URL, future=True, echo=True)
async_session = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)
# endregion


# region:BLOCK WITH DATABASE MODELS
Base = declarative_base()


class User(Base):
    __tablename__ = "users"

    user_id = Column(
        type_=UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )
    f_name = Column(
        type_=String,
        nullable=False,
    )
    l_name = Column(
        type_=String,
        nullable=False,
    )
    email = Column(
        type_=String,
        nullable=False,
        unique=True,
    )
    is_active = Column(
        type_=Boolean(),
        default=True,
    )


# endregion


# region:BLOCK FOR COMMON INTERACTION WITH DATABASE IN BUSINESS CONTEXT
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


# endregion


# region:BLOCK WITH API MODELS
LETTER_MATCH_PATTERN = re.compile(r"^[а-яА-Яa-zA-Z\-]+$")


class TunnedModel(BaseModel):
    class Config:
        """tells pydantic to convert even non dict obj to json"""

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


# endregion

# region:BLOCK WITH API ROUTES

app = FastAPI(title="vladrunk WebApp")

user_routrer = APIRouter()


async def _create_new_user(body: UserCreate) -> ShowUser:
    async with async_session() as session:
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
async def create_user(body: UserCreate) -> ShowUser:
    return await _create_new_user(body)


main_api_router = APIRouter()

main_api_router.include_router(user_routrer, prefix="/user", tags=["user"])
app.include_router(main_api_router)

# endregion

if __name__ == "__main__":
    # run app on the host and port
    uvicorn.run(app, host="0.0.0.0", port=8000)