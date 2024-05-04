from typing import Annotated

from fastapi import APIRouter
from starlette.exceptions import HTTPException
from starlette.requests import Request
from starlette.responses import Response
from starlette.status import (
    HTTP_409_CONFLICT,
    HTTP_404_NOT_FOUND,
    HTTP_403_FORBIDDEN
)
from pydantic import BaseModel, Field

from app.models.users_db import User
from app.utils.authorization import set_session_cookie, delete_session_cookie

router = APIRouter(tags=["register"])


@router.post(
    "/register/",
    response_model=User.FullModel,
    status_code=201,
)
async def sing_up(data: User.RegisterModel):

    if await User.select_first_by_kwargs(email=data.email) is not None:
        raise HTTPException(
            HTTP_409_CONFLICT,
            detail="Email already in use"
        )
    new_user = await User.create(**data.model_dump())
    return new_user


class SignIn(BaseModel):
    username: str
    password: Annotated[str, Field(min_length=4, max_length=100)]


@router.post(
    "/signin/",
)
async def sign_in(response: Response, auth_data: SignIn):
    user: User = await User.select_first_by_kwargs(username=auth_data.username)
    if user is None:
        raise HTTPException(
            HTTP_404_NOT_FOUND,
            detail="User not found",
        )
    if not user.is_password_valid(auth_data.password):
        raise HTTPException(
            HTTP_403_FORBIDDEN,
            detail="Wrong password",
        )
    await set_session_cookie(response, user)


@router.post("/signout/")
async def sign_out(request: Request, response: Response) -> None:
    await delete_session_cookie(request, response)



