import { handler } from './build/handler.js';
import express from 'express';
import fs from 'fs';
import https from 'https';
import cors from 'cors';

const privateKey = fs.readFileSync('./certs/devenv.key', 'utf8');
const certificate = fs.readFileSync('./certs/devenv.crt', 'utf8');
const credentials = { key: privateKey, cert: certificate };

const app = express();
app.use(cors());

const httpsServer = https.createServer(credentials, app);

const SSLPORT = 6420;

httpsServer.listen(SSLPORT, function () {
    console.log('HTTPS Server is running on: https://localhost:%s', SSLPORT);
});

app.use(handler);
