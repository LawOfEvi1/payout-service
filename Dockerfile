# Базовый образ с Python 3.12 (или 3.10+)
FROM python:3.12-slim

# Рабочая директория
WORKDIR /app

# Копируем pyproject.toml и poetry.lock
COPY pyproject.toml poetry.lock* /app/

# Устанавливаем poetry
RUN pip install --upgrade pip && \
    pip install poetry

# Устанавливаем зависимости
RUN poetry config virtualenvs.create false && \
    poetry install --no-root --no-interaction --no-ansi

# Копируем проект
COPY ./src /app/src

# Устанавливаем рабочую директорию для Django
WORKDIR /app/src
