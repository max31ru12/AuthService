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
    username: Mapped[str] = mapped_column(String(100), unique=True)
    email: Mapped[str] = mapped_column(String(100), unique=True)
    password: Mapped[str] = mapped_column(String(100))
    registered_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)
    last_password_change: Mapped[datetime] = mapped_column(default=datetime.utcnow)

    @staticmethod
    def generate_hash(password: str):
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

    def is_password_valid(self, password: str) -> bool:
        return pbkdf2_sha256.verify(password, self.password)

    def change_password(self, new_password: str) -> None:
        self.last_password_change = datetime.utcnow()  # noqa
        self.password = self.generate_hash(new_password)  # noqa

    def change_email(self, new_email) -> None:
        self.email = new_email  # noqa
