from app.models.session_db import Session
from app.models.users_db import User
from app.utils.repository import BaseRepository


class UserRepo(BaseRepository):
    model = User


class SessionRepo(BaseRepository):
    model = Session
