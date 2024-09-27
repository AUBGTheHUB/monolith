FROM python:3.12.6-bullseye AS builder
LABEL authors="ivanobreshkov"

# https://medium.com/@albertazzir/blazing-fast-python-docker-builds-with-poetry-a78a66f5aed0

RUN pip install poetry

ENV POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_IN_PROJECT=1 \
    POETRY_VIRTUALENVS_CREATE=1 \
    POETRY_CACHE_DIR=/tmp/poetry_cache

WORKDIR /app

COPY pyproject.toml poetry.lock README.md ./

RUN poetry install --no-root && rm -rf $POETRY_CACHE_DIR

# The runtime image, used to just run the code provided its virtual environment
FROM python:3.12.6-slim-bullseye AS runtime

RUN apt-get update && apt-get install -y --no-install-recommends curl && rm -rf /var/lib/apt/lists/*

ENV VIRTUAL_ENV=/app/.venv \
    PATH="/app/.venv/bin:$PATH"

COPY --from=builder ${VIRTUAL_ENV} ${VIRTUAL_ENV}

WORKDIR /app

COPY src ./src
COPY .env ./

EXPOSE 6969

# As we are using self-signed certs we don't check the validity of the certs with -k
HEALTHCHECK --interval=1m --timeout=10s CMD curl -k -f https://localhost:6969/email-service/v1/ping

ENTRYPOINT ["python", "-m", "src.server.app_entrypoint"]
