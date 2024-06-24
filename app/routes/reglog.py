from enum import Enum

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from starlette.responses import Response
from starlette.status import HTTP_409_CONFLICT, HTTP_404_NOT_FOUND, HTTP_401_UNAUTHORIZED

from app.dependencies.authorization import add_session_to_response, AuthorizedUser, AuthorizedSession
from app.models.session_db import Session
from app.models.users_db import User
from app.utils.responses import Responses

router = APIRouter(prefix="/users")


class RegisterResponses(Responses, Enum):
    EMAIL_ALREADY_IN_USE = 409, "Email or username already in use"


class UserResponses(Responses, Enum):
    USER_NOT_FOUND = 404, "User not found"


class SignInResponses(Responses, Enum):
    USER_NOT_FOUND = 404, "User not found"
    WRONG_PASSWORD = 401, "Wrong password"


class AuthData(BaseModel):
    username: str
    password: str


@router.post(
    "/signup",
    response_model=User.FullModel,
    responses=RegisterResponses.get_responses()
)
async def sign_up(data: User.RegisterModel) -> User:
    if (await User.select_first_by_kwargs(email=data.email)) is not None:
        raise HTTPException(
            status_code=HTTP_409_CONFLICT,
            detail="Email already in use",
        )

    if (await User.select_first_by_kwargs(username=data.username)) is not None:
        raise HTTPException(
            status_code=HTTP_409_CONFLICT,
            detail="Username already in use",
        )

    user = await User.create(**data.model_dump())
    return user


@router.post(
    "/signin",
    responses=SignInResponses.get_responses(),
)
async def sign_in(response: Response, auth_data: AuthData) -> None:

    user = await User.select_first_by_kwargs(username=auth_data.username)
    if user is None:
        raise HTTPException(
            status_code=HTTP_404_NOT_FOUND,
            detail="User not found",
        )
    if not user.is_password_valid(auth_data.password):
        raise HTTPException(
            status_code=HTTP_401_UNAUTHORIZED,
            detail="Wrong password",
        )

    session = await Session.create(
        user_id=user.id,
        user=user,
    )

    add_session_to_response(response, session)



@router.get(
    "/",
    response_model=list[User.FullModel],
)
async def get_users() -> list[User]:
    users = await User().select_all()
    return users


@router.get(
    "/{user_id}",
    response_model=User.FullModel,
    responses=UserResponses.get_responses(),
)
async def get_user_by_id(user_id: int) -> User:
    user = await User.select_first_by_kwargs(id=user_id)
    if user is None:
        raise HTTPException(
            status_code=HTTP_404_NOT_FOUND,
            detail="User not found",
        )
    return user
