import uuid

from sqlalchemy import Column, String, Boolean
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import declarative_base

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
