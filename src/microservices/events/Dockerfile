FROM python:3.14-slim

WORKDIR /app

ENV PYTHONUNBUFFERED=1

LABEL authors="Nikita Selivanov"

COPY ./poetry.lock ./pyproject.toml /app/

RUN pip install poetry && poetry config virtualenvs.create false && poetry install --no-root

COPY ./src/ /app/

CMD python3 -m events
