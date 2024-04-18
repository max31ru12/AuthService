from datetime import datetime
from typing import Annotated

from pydantic import Field, AfterValidator
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String
from pydantic_marshals.sqlalchemy import MappedModel
from passlib.handlers.pbkdf2 import pbkdf2_sha256

from app.common.config import Base


class User(Base):

    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    username: Mapped[str] = mapped_column(String(100))
    email: Mapped[str] = mapped_column(String(100))
    password: Mapped[str] = mapped_column(String(100))
    registered_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)

    def is_password_valid(self, password: str) -> bool:
        return pbkdf2_sha256.verify(password, self.password)

    @staticmethod
    def generate_hash(password):
        return pbkdf2_sha256.hash(password)

    PasswordType = Annotated[
        str, Field(min_length=4, max_length=100), AfterValidator(generate_hash)
    ]

    RegisterModel = MappedModel.create(
        columns=[username, email, (password, PasswordType)]
    )

    FullModel = MappedModel.create(
        columns=[id, username, registered_at]
    )

