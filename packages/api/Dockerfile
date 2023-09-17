# syntax=docker/dockerfile:1


FROM golang:1.19-alpine as build

WORKDIR /app

COPY . .

WORKDIR /app/go-modules

RUN go mod download

WORKDIR /app

RUN go build -o /api

FROM build as final

EXPOSE 8000

CMD [ "/api"]
