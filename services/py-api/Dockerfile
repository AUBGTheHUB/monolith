FROM python:3.12.6-bullseye AS builder

# https://medium.com/@albertazzir/blazing-fast-python-docker-builds-with-poetry-a78a66f5aed0

RUN pip install poetry

ENV POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_IN_PROJECT=1 \
    POETRY_VIRTUALENVS_CREATE=1 \
    POETRY_CACHE_DIR=/tmp/poetry_cache

WORKDIR /app

# Poetry will complain if a README.md is not found
COPY pyproject.toml poetry.lock README.md ./

# we use --no-root to avoid installing the project itself. This helps maintain the Docker cache, as changes to the
# project source won't invalidate the cached dependencies.
# https://python-poetry.org/docs/faq/#poetry-busts-my-docker-cache-because-it-requires-me-to-copy-my-source-files-in-before-installing-3rd-party-dependencies
RUN poetry install --without dev --no-root && rm -rf $POETRY_CACHE_DIR

# The runtime image, used to just run the code provided its virtual environment
FROM python:3.12.6-slim-bullseye AS runtime

# we use --no-install-recommends and removing the list of packages to make the finall image size smaller
RUN apt-get update && apt-get install -y --no-install-recommends curl && rm -rf /var/lib/apt/lists/*

# Prepending the venv's bin directory to PATH to ensure executables are found
# Prepending is important because Linux searches the PATH from left to right, so executables in /app/.venv/bin will be used
# first before any system-wide executables
ENV VIRTUAL_ENV=/app/.venv \
    PATH="/app/.venv/bin:$PATH"

# This ensures that the runtime image has access to the packages and dependencies installed in the venv
COPY --from=builder ${VIRTUAL_ENV} ${VIRTUAL_ENV}

# Any subsecuent commmands like COPY and RUN that use relative path will use /app as the base directory
WORKDIR /app

COPY src ./src
COPY shared ./shared

# For documentation between the person who builds the image and the person who runs the container, about which ports
# are intended to be published
# https://docs.docker.com/reference/dockerfile/#expose
EXPOSE 8080

HEALTHCHECK --interval=1m --timeout=10s --retries=3 CMD \
    # This is needed as when we run the container locally we need to use the self-signed certs
    # If not passes with --cacert curl will fail with exit code 60, meaning there is a problem with the SSL
    if [ "$DOMAIN" = "localhost" ]; then \
        curl --cacert /app/src/server/certs/localhost.crt -f https://$DOMAIN:8080/api/v3/ping; \
    else \
        curl -f https://$DOMAIN:8080/api/v3/ping; \
    fi

# Run the uvicorn server
ENTRYPOINT ["python", "-m", "src.app_entrypoint"]
