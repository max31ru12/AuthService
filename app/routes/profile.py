from typing import Annotated

from fastapi import APIRouter
from pydantic import BaseModel, Field
from starlette.exceptions import HTTPException
from starlette.status import HTTP_403_FORBIDDEN, HTTP_409_CONFLICT

from app.models.users_db import User
from app.utils.authorization import authorized_user


router = APIRouter(tags=["profiles"])


class PasswordChangeModel(BaseModel):
    old_password: str
    new_password: Annotated[str, Field(min_length=4, max_length=100)]


class EmailChangeModel(BaseModel):
    new_email: str


@router.get(
    "/",
    response_model=User.FullModel,
    summary="Get current user's profile"
)
async def user_profile(user: authorized_user) -> User:
    return user


@router.put(
    "/password/",
    status_code=204,
    responses={403: {"description": "Wrong password",
                     "content": {"application/json": {"example": "Wrong password"}}
                     }},
    summary="Change user's password",
)
async def change_password(
    user: authorized_user,
    put_data: PasswordChangeModel,
) -> None:
    if not user.is_password_valid(put_data.old_password):
        raise HTTPException(
            HTTP_403_FORBIDDEN,
            detail="Wrong password",
        )
    user.change_password(put_data.new_password)


@router.put(
    "/email/",
    status_code=204,
    responses={409: {"description": "Email already in use",
                     "content": {"application/json": {"example": "Email already in use"}}
                     }},
    summary="Change user's email",
)
async def change_email(user: authorized_user, put_data: EmailChangeModel) -> None:

    if User.select_first_by_kwargs(email=put_data.new_email):
        raise HTTPException(
            HTTP_409_CONFLICT,
            detail="Email already in use",
        )
    user.change_email(put_data.new_email)
