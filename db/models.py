import uuid

from sqlalchemy import Column, String, Boolean
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import declarative_base

# Создание базового класса для объявления моделей SQLAlchemy
Base = declarative_base()


# Определение модели данных для пользователей
class User(Base):
    # Имя таблицы в базе данных
    __tablename__ = "users"

    # Уникальный идентификатор пользователя (UUID)
    user_id = Column(
        type_=UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )
    # Имя пользователя, обязательное поле
    f_name = Column(
        type_=String,
        nullable=False,
    )
    # Фамилия пользователя, обязательное поле
    l_name = Column(
        type_=String,
        nullable=False,
    )
    # Электронная почта пользователя, уникальное и обязательное поле
    email = Column(
        type_=String,
        nullable=False,
        unique=True,
    )
    # Флаг активности пользователя, по умолчанию True
    is_active = Column(
        type_=Boolean(),
        default=True,
    )
