# Create a new build stage from a base image
FROM node:23-alpine AS build-stage

# Change the working directory to /app inside of the container. If that directory does not already exist, it will
# be created. Reference: https://docs.docker.com/reference/dockerfile/#workdir
WORKDIR /app

# Download dependencies as a separate step to take advantage of Docker's caching.
# Leverage a cache mount to /root/.npm to speed up subsequent builds.
# Leverage a bind mounts to package.json and package-lock.json to avoid having to copy them into
# into this layer.
# See https://docs.docker.com/build/building/best-practices/#add-or-copy
# We use npm ci to do a clean install of the dependencies. https://docs.npmjs.com/cli/v11/commands/npm-ci
RUN --mount=type=bind,source=package.json,target=package.json \
    --mount=type=bind,source=package-lock.json,target=package-lock.json \
    --mount=type=cache,target=/root/.npm \
    npm ci

# Copy the rest of the application files
COPY . .

ARG VITE_ENV

# Set environment variables based on build arguments. These are passed in the CD pipeline.
# The environment variables set using ENV will persist when a container is run from the resulting image.
ENV VITE_ENV=${VITE_ENV}

# Build the app
RUN npm run build

# Bundle static assets with caddy
# TODO: Figure out how to use non-root user in container as per: https://docs.docker.com/build/building/best-practices/#user
FROM caddy:2.10-alpine AS runtime

# The build args are passed in the CD pipeline.
ARG DOMAIN

# Redeclare the build arg to make it visiable in this stage
ARG VITE_ENV

# Perstig the build argument in order to be used in healthchecks
ENV DOMAIN=${DOMAIN}

# Copy built assets from the build-stage
# /srv is the WORKDIR set by the caddy Dockerfile
# https://github.com/caddyserver/caddy-docker/blob/d0c036065bee3bb086199d212be6f0d3b937c74a/2.10/alpine/Dockerfile#L59
COPY --from=build-stage /app/dist /srv

# https://caddyserver.com/docs/conventions#your-config-files
# This is the default location that the caddy Dockerfile uses to run server from the resulting image
# https://github.com/caddyserver/caddy-docker/blob/d0c036065bee3bb086199d212be6f0d3b937c74a/2.10/alpine/Dockerfile#L61C7-L61C12
COPY Caddyfile /etc/caddy/Caddyfile

# Inform Docker that the container listens on the specified network ports at runtime.
# This acts as documentation for the consumer of the image which ports are intended to be published.
# https://docs.docker.com/reference/dockerfile/#expose
EXPOSE 80 443
