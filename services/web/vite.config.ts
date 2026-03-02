import path from 'path';
import react from '@vitejs/plugin-react';
import { defineConfig, ServerOptions } from 'vite';

export default defineConfig(({ mode }) => {
    const serverConfig: ServerOptions = {
        host: '0.0.0.0',
        port: 3000,
        watch: {
            usePolling: true,
        },
    };
    console.log('Vite mode is:', mode);

    if (mode === 'development') {
        serverConfig.proxy = {
            '/api/v3': {
                target: 'https://localhost:8080',
                changeOrigin: true,
                secure: false,
                cookieDomainRewrite: '',
            },
        };
    }

    return {
        plugins: [react()],
        resolve: {
            alias: {
                '@': path.resolve(__dirname, './src'),
            },
        },
        server: serverConfig,
    };
});
