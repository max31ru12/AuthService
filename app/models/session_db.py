from datetime import datetime, timedelta
from secrets import token_urlsafe
from typing import ClassVar, Self

from sqlalchemy import CHAR, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from pydantic_marshals.sqlalchemy import MappedModel

from app.common.config import Base
from .users_db import User


class Session(Base):

    __tablename__ = "session"
    token_length: ClassVar[int] = 40
    token_randomness: ClassVar[int] = 50
    lifetime: ClassVar[timedelta] = timedelta(days=1, seconds=1)

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    token: Mapped[str] = mapped_column(CHAR(token_length))
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)
    user_id: Mapped[int] = mapped_column(ForeignKey(User.id, ondelete="CASCADE"))
    user: Mapped[User] = relationship(passive_deletes=True)

    status: Mapped[bool] = mapped_column(default=True)

    def disable(self) -> None:
        self.status = False  # noqa

    @staticmethod
    def generate_token() -> str:
        return token_urlsafe(Session.token_randomness)[: Session.token_length]

    @classmethod
    async def create(cls, **kwargs) -> Self:
        kwargs["token"] = cls.generate_token()
        return await super().create(**kwargs)

    FullModel = MappedModel.create(
        columns=[token, user_id, created_at]
    )

    @property
    def session_expired(self) -> bool:
        return datetime.utcnow() > self.created_at + self.lifetime

