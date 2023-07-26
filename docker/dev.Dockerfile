FROM python:3.11-slim
  
ENV PYTHONDONTWRITEBYTECODE=1
ENV POETRY_VIRTUALENVS_CREATE=false

RUN pip3 install -U pip setuptools
RUN pip3 install poetry

WORKDIR /code
COPY pyproject.toml poetry.lock /code/
RUN PATH="$PATH:$HOME/.poetry/bin" && poetry install --no-root
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8080"]