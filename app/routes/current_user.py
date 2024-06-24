from fastapi import APIRouter

from app.dependencies.authorization import AuthorizedUser
from app.models.users_db import User

router = APIRouter(prefix='/current_user')


@router.get(
    "/",
    response_model=User.FullModel
)
async def get_profile(user: AuthorizedUser) -> User:
    return user
