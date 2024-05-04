from contextlib import asynccontextmanager
from typing import AsyncIterator, Awaitable, Callable

from fastapi import FastAPI
from starlette.requests import Request
from starlette.responses import Response

from app.common.services import session_context
from app.common.config import sessionmaker, DEV_MODE
from app.utils.setup import reinit_database
from app.routes import signing, profile


@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncIterator:
    if DEV_MODE:
        await reinit_database()
    yield


app = FastAPI(
    title="Test FastAPI project",
    lifespan=lifespan,
)

app.include_router(signing.router, prefix="/api/v1")
app.include_router(profile.router, prefix="/api/v1/profile")


@app.middleware("http")
async def session_middleware(
        request: Request,
        call_next: Callable[[Request], Awaitable[Response]]
) -> Response:
    async with sessionmaker.begin() as session:
        session_context.set(session)
        return await call_next(request)
