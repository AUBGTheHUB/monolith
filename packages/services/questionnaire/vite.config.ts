import { sveltekit } from '@sveltejs/kit/vite';
import { defineConfig } from 'vite';
import fs from 'fs';

export default defineConfig({
    plugins: [sveltekit()],
    //TODO: Add check for ENV - if PROD load the certs
    server: {
        https: {
            key: fs.readFileSync(`${__dirname}/devenv.key`),
            cert: fs.readFileSync(`${__dirname}/devenv.crt`),
        },
    },
});
