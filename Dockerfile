# Use the official Alpine Linux image as the base
FROM python:3.9-alpine

RUN apk update && apk add --no-cache \
    curl \
    docker \
    docker-compose \
    git \
    openssl

WORKDIR /app

COPY . /app

RUN pip install -r requirements.txt

VOLUME /app

CMD ["/bin/sh"]
