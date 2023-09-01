FROM python:3.11 as build

RUN apt update
RUN pip install poetry

WORKDIR /app

COPY . .
RUN poetry install

ARG CON_STR=${CON_STR}
ENV CON_STR=${CON_STR}
RUN rm .env
RUN echo "MONGOURI=${CON_STR}\nIS_OFFLINE=true" > /app/.env

FROM build as final

EXPOSE 6969

CMD ["poetry", "run", "start"]
