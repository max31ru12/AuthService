# AuthService
Experiment with authentication 

## How to run project

Clone repository
```shell
git clone https://github.com/max31ru12/AuthService.git
```

Run docker-containers
```shell
docker compose up --build -d
```

Install and run poetry
```shell
# .../AuthService
poetry init

# activate virtual env
poetry shell
```

Run project with uvicorn
```shell
uvicorn app.main:app --reload
```
