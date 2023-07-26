## Setup

### Enviroment

```
python3 -m venv ~/venv/fastapi-mongodb-app
source ~/venv/fastapi-mongodb-app/bin/activate
pip install poetry
poetry install
```

## How to Run

```
uvicorn server.main:app --host 0.0.0.0 --reload
```
