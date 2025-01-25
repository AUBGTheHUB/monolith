# Create a new build stage from a base image
FROM node:23-alpine AS builder

# Change the working directory to /app inside of the container. If that directory does not already exist, it will
# be created. Reference: https://docs.docker.com/reference/dockerfile/#workdir
WORKDIR /app

# Copy app files
COPY . .

# Install dependencies (npm ci makes sure the exact versions in the lockfile gets installed)
RUN npm ci

# Build the app
RUN npm run build

# Bundle static assets with nginx
FROM nginx:1.27.3-alpine AS production


ENV NODE_ENV=production

# Copy built assets from `builder` image
COPY --from=builder /app/dist /usr/share/nginx/html

# Copy the correct nginx configuration based on the domain
RUN if [ "$DOMAIN" = "dev.thehub-aubg.com" ]; then \
        cp nginx.dev.conf /etc/nginx/conf.d/default.conf; \
    else \
        cp nginx.conf /etc/nginx/conf.d/default.conf; \
    fi

# Expose port
EXPOSE 80 443

# Start nginx
CMD ["nginx", "-g", "daemon off;"]
