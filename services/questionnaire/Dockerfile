FROM node:19

WORKDIR /app

COPY ./packages/services/questionnaire /app
RUN rm /app/.env || true
COPY ../../../.env /app/.env

RUN npm install
RUN npm run build

EXPOSE 6420

CMD ["node", "-r", "dotenv/config", "server.js"]
