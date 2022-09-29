# syntax=docker/dockerfile:1

# SECRETS SHOULD BE ADDED

FROM golang:1.18-alpine

WORKDIR /app

COPY . .

WORKDIR /app/go-modules

RUN go mod download

WORKDIR /app

RUN go build -o /api

EXPOSE 8000

CMD [ "/api" ]

