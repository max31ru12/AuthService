# AuthService
Experiment with authentication

## How to run the app

Clone repository
```shell
git clone https://github.com/max31ru12/AuthService.git
```

Run docker-containers
```shell
docker compose up --build -d
```

Available on: `http://127.0.0.1:8000`

## Developer Mode

Install and run poetry
```shell
# .../AuthService
poetry init

# activate virtual env
poetry shell

# install dependencies
poetry install
```

Up development containers

```shell
docker compose -f ./docker-compose-dev.yml up
```

Run project with uvicorn
```shell
uvicorn app.main:app --reload
```
