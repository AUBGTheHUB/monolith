# Create a new build stage from a base image
FROM node:23-alpine AS builder

# Change the working directory to /app inside of the container. If that directory does not already exist, it will
# be created. Reference: https://docs.docker.com/reference/dockerfile/#workdir
WORKDIR /app

# Copy first only the package.json and package-lock.json files to leverage Docker cache
COPY package*.json ./

# Install dependencies (npm ci makes sure the exact versions in the lockfile gets installed)
RUN npm ci

# Copy the rest of the application files
COPY . .

# The environment variables set using ENV will persist when a container is run from the resulting image.
ENV VITE_ENV="DEV"

# Build the app
RUN npm run build

# Bundle static assets with nginx
FROM nginx:latest AS dev

# Copy built assets from `builder` stage
COPY --from=builder /app/dist /usr/share/nginx/html

# We override the `default.conf` that comes with the base ngixn image.
# In the main nginx.conf located at /etc/nignx/nginx.conf, the `include` directive is used to include all .conf files
# in the /etc/nginx/conf.d directory. This is where we add our custom Feature-Specific Configuration.
# https://docs.nginx.com/nginx/admin-guide/basic-functionality/managing-configuration-files/#feature-specific-configuration-files
COPY nginx.dev.conf /etc/nginx/conf.d/default.conf

# Inform Docker that the container listens on the specified network ports at runtime.
# https://docs.docker.com/reference/dockerfile/#expose
EXPOSE 80 443

# The build args are passed in the CD pipeline.
ARG DOMAIN

# Perstig the build argument in order for the healthcheck to use it
ENV DOMAIN=${DOMAIN}

# HEALTHCHECK --interval=1m --timeout=10s --retries=3 CMD curl -f https://${DOMAIN}

CMD ["nginx", "-g", "daemon off;"]

# NB!!!:
# If you add a custom CMD in the dev.Dockerfile, be sure to include -g daemon off; in the CMD in order for nginx to stay in
# the foreground, so that Docker can track the process properly (otherwise your container will stop immediately after
# starting)! Source: https://hub.docker.com/_/nginx
