# Create a new build stage from a base image
FROM node:23-alpine AS build-stage

# https://nodejs.org/en/learn/getting-started/nodejs-the-difference-between-development-and-production
# Use production node environment by default.
ENV NODE_ENV=production

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

ENV VITE_ENV="PROD"

# Build the app
RUN npm run build

# Bundle static assets with nginx
# TODO: Change image with https://hub.docker.com/r/nginxinc/nginx-unprivileged when the auto renew of ssl certs is
# implemented, as oer: https://docs.docker.com/build/building/best-practices/#user
FROM nginx:1.27-alpine AS dev

# The build args are passed in the CD pipeline.
ARG DOMAIN

# Perstig the build argument in order to be used in healthchecks
ENV DOMAIN=${DOMAIN}

# Copy built assets from the build-stage
COPY --from=build-stage /app/dist /usr/share/nginx/html

# We override the `default.conf` that comes with the base ngixn image.
# In the main nginx.conf located at /etc/nignx/nginx.conf, the `include` directive is used to include all .conf files
# in the /etc/nginx/conf.d directory. This is where we add our custom Feature-Specific Configuration.
# https://docs.nginx.com/nginx/admin-guide/basic-functionality/managing-configuration-files/#feature-specific-configuration-files
COPY nginx.prod.conf /etc/nginx/conf.d/default.conf

# Inform Docker that the container listens on the specified network ports at runtime.
# https://docs.docker.com/reference/dockerfile/#expose
EXPOSE 80 443

# We are using the default nginx image ENTRYPOINT and CMD, that's why we don't set them explicitly

# NB!!!:
# If you add a custom CMD in the dev.Dockerfile, be sure to include -g daemon off; in the CMD in order for nginx to
# stay in the foreground, so that Docker can track the process properly (otherwise your container will stop immediately
# after starting)! Source: https://hub.docker.com/_/nginx
