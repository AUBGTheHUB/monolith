FROM node:16-alpine as builder
# Set the working directory to /app inside the container
WORKDIR /app
# Copy app files
COPY . .

ARG REACT_APP_OBJ_UPLOADER_URL
ARG REACT_APP_GCP_TOKEN

ENV REACT_APP_OBJ_UPLOADER_URL=${REACT_APP_OBJ_UPLOADER_URL}
ENV REACT_APP_GCP_TOKEN=${REACT_APP_GCP_TOKEN}

RUN echo -e "REACT_APP_OBJ_UPLOADER_URL=${REACT_APP_OBJ_UPLOADER_URL}\nREACT_APP_GCP_TOKEN=${REACT_APP_GCP_TOKEN}\n">>./.env.production && cat ./.env.production;

# Install dependencies (npm ci makes sure the exact versions in the lockfile gets installed)
RUN npm ci 
# Build the app
RUN npm run build

# Bundle static assets with nginx
FROM nginx:1.21.0-alpine as production
ENV NODE_ENV production
# Copy built assets from `builder` image
COPY --from=builder /app/build /usr/share/nginx/html
# Add your nginx.conf
COPY nginx.conf /etc/nginx/conf.d/default.conf
# Expose port
EXPOSE 80 443
# Start nginx
CMD ["nginx", "-g", "daemon off;"]