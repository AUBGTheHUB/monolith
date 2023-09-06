// src/routes/api/[file].js
import fs from 'fs';
import path from 'path';

export async function GET({ params }: { params: any }) {
    const { folder, filename } = params;

    try {
        const filePath = `src/routes/questionnaires/shiki/${folder}/${filename}`;
        try {
            const buffer = await fs.promises.readFile(filePath);
            return new Response(buffer, {
                status: 200,
                headers: {
                    'Content-Type': 'application/octet-stream',
                    'Content-Disposition': `'attachment; filename*=UTF-8''${encodeURIComponent(filename)}`,
                },
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
