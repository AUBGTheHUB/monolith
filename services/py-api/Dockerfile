# Inspiration: https://medium.com/@albertazzir/blazing-fast-python-docker-builds-with-poetry-a78a66f5aed0

FROM python:3.12-bookworm AS build-stage

RUN pip install poetry==2.1.1

ENV POETRY_VIRTUALENVS_IN_PROJECT=1 \
    POETRY_CACHE_DIR=/tmp/poetry_cache

WORKDIR /app

# Poetry will complain if a README.md is not found
RUN touch README.md

# Download dependencies as a separate step to take advantage of Docker's caching. https://docs.docker.com/build/cache/
# Leverage a cache mount to $POETRY_CACHE_DIR to speed up subsequent builds.
# Leverage a bind mount to pyproject.toml and poetry.lock to avoid having to copy them into into this layer.
# See https://docs.docker.com/build/building/best-practices/#add-or-copy
#
# we use --no-root to avoid installing the project itself. This helps maintain the Docker cache, as changes to the
# project source won't invalidate the cached dependencies.
# https://python-poetry.org/docs/faq/#poetry-busts-my-docker-cache-because-it-requires-me-to-copy-my-source-files-in-before-installing-3rd-party-dependencies
RUN --mount=type=cache,target=$POETRY_CACHE_DIR \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    --mount=type=bind,source=poetry.lock,target=poetry.lock \
    poetry install --without dev --no-root

# The image, used to just run the code provided its virtual environment. We use the slim version, to keep the image
FROM python:3.12-slim-bookworm AS runtime

# Insatll curl to perform healtchecks. We use --no-install-recommends and removing the list of packages to make the
# final image size smaller
# See https://docs.docker.com/build/building/best-practices/#apt-get
RUN apt-get update && apt-get install -y --no-install-recommends curl && rm -rf /var/lib/apt/lists/*

# Prepending the venv's bin directory to PATH to ensure executables are found
# Prepending is important because Linux searches the PATH from left to right, so executables in /app/.venv/bin will be
# used first before any system-wide executables
ENV VIRTUAL_ENV=/app/.venv \
    PATH="/app/.venv/bin:$PATH"

# This ensures that the runtime image has access to the packages and dependencies installed in the venv
COPY --from=build-stage ${VIRTUAL_ENV} ${VIRTUAL_ENV}

# Any subsecuent commmands like COPY and RUN that use relative path will use /app as the base directory
WORKDIR /app

# Create a non-privileged user that the app will run under.
# See https://docs.docker.com/go/dockerfile-user-best-practices/
RUN adduser \
    --disabled-password \
    --gecos "" \
    --home "/nonexistent" \
    --shell "/sbin/nologin" \
    --no-create-home \
    --uid "10001" \
    appuser

# Switch to the non-privileged user to run the application.
USER appuser

COPY src ./src
# Give appuser ownership to the log files, so that we can write to them
COPY --chown=appuser:appuser shared ./shared

# Inform Docker that the container listens on the specified network ports at runtime.
# https://docs.docker.com/reference/dockerfile/#expose
EXPOSE 8080

ARG ENV
ARG DOMAIN

# Set environment variables based on build arguments. These are passed in the CD pipeline.
# The environment variables set using ENV will persist when a container is run from the resulting image.
ENV ENV=${ENV}
ENV DOMAIN=${DOMAIN}

# These stay constant for deployed environments
ENV ADDRESS=0.0.0.0
ENV PORT=8080

# Keeps Python from buffering stdout and stderr to avoid situations where the application crashes without emitting any
# logs due to buffering.
ENV PYTHONUNBUFFERED=1

# Run the uvicorn server
ENTRYPOINT ["python", "-m", "src.app_entrypoint"]
