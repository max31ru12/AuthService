FROM python:3.12-alpine

WORKDIR /auth

RUN pip install poetry
RUN poetry config virtualenvs.create false

COPY poetry.lock ./
COPY pyproject.toml ./

RUN poetry install

COPY ./app /auth/app
COPY ./alembic.ini ./alembic.ini
COPY ./alembic ./alembic

ENTRYPOINT ["poetry", "run", "uvicorn", "app.main:app", "--host", "0.0.0.0"]
