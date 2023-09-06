FROM node:19

WORKDIR /app

COPY ./packages/services/questionnaire /app
RUN rm /app/.env || true
COPY ../../../.env /app/.env

COPY ./data/certs/devenv.key /app
COPY ./data/certs/devenv.crt /app

RUN npm install
RUN npm run build

EXPOSE 3000

CMD ["node", "-r", "dotenv/config", "build"]
