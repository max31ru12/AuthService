from fastapi import APIRouter
from pydantic import BaseModel

from app.models.users_db import User

router = APIRouter(prefix="/users")


class SignUp(BaseModel):
    username: str
    email: str
    password: str


@router.post("/", response_model=User.FullModel)
async def sign_up(data: SignUp) -> User:
    user = await User.create(**data.model_dump())
    return user


# @router.get("/")
# async def get_users():
#     users = await UserRepository().select_all()
#     return users
#
#
# @router.get("/{user_id}")
# async def get_user_by_id(user_id: int):
#     user = await UserRepository().select_first_by_kwargs(id=user_id)
#     return user
