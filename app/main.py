from contextlib import asynccontextmanager
from typing import AsyncIterator

from fastapi import FastAPI
from starlette.requests import Request
from starlette.responses import Response

from app.common.config import DEV_MODE, sessionmaker
from app.routes import reglog, current_user
from app.utils.repository import session_context
from app.utils.setup import reinit_database


@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncIterator:
    if DEV_MODE:
        await reinit_database()
    yield


app = FastAPI(
    title="Test FastAPI project",
    lifespan=lifespan,
)

app.include_router(reglog.router, prefix="/api/v1")
app.include_router(current_user.router, prefix="/api/v1")


@app.middleware("http")
async def session_middleware(request: Request, call_next) -> Response:
    async with sessionmaker.begin() as session:
        session_context.set(session)
        return await call_next(request)
