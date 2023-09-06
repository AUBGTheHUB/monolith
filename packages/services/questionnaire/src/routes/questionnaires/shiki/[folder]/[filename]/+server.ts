/**
 * To enable hosting the app through our nginx reverse proxy,
 * it's necessary for us to manage the hosting of our static files independently.
 * When we proxy an endpoint like /questionnaires, the static path / becomes inaccessible
 * because it's already used by the primary frontend.
 */

import fs from 'fs';

export async function GET({ params }: { params: any }) {
    const { folder, filename }: { folder: string; filename: string } = params;

    try {
        const filePath = `src/routes/questionnaires/shiki/${folder}/${filename}`;
        try {
            const buffer = await fs.promises.readFile(filePath);

            const headers = {
                'Content-Type': filename.includes('wasm') ? 'application/wasm' : 'application/octet-stream',
                'Content-Disposition': filename.includes('wasm')
                    ? `attachment; filename="${encodeURIComponent(filename)}"`
                    : `attachment; filename*=UTF-8''${encodeURIComponent(filename)}`,
            };

            return new Response(buffer, {
                status: 200,
                headers,
            });
        } catch (error) {
            const response = JSON.stringify({ message: error });
            return new Response(response);
        }
    } catch (error) {
        return {
            status: 404,
            body: {
                error: 'File not found',
            },
        };
    }
}
