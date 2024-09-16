FROM python:3.12-slim
ENV POETRY_VIRTUALENVS_CREATE=false

# Instalar dependencias del sistema
RUN apt-get update && apt-get install -y \
    libpq-dev \
    gcc \
    && apt-get clean

WORKDIR /app
COPY . . 

RUN pip install poetry

RUN poetry config installer.max-workers 10
RUN poetry install --no-interaction --no-ansi

EXPOSE 8000
# CMD poetry run uvicorn --host 0.0.0.0 fast_zero.app:app

CMD poetry run fastapi run fast_zero/app.py