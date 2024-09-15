import { questions } from '$lib/database/mongo';
import { error } from '@sveltejs/kit';
import { ReturnDocument } from 'mongodb';
import type { DepartmentQuestions } from '../types';
import { BEARER_TOKEN, LEAKED_TOKEN } from '$env/static/private';

function isAuthenticated(headers: Headers) {
    if (headers.get('BEARER-TOKEN') !== BEARER_TOKEN) {
        throw error(401, {
            message: 'User is unauthenticated',
        });
    }
}

function leakedSecretsGame(headers: Headers) {
    if (headers.get('BEARER-TOKEN') === LEAKED_TOKEN) {
        throw error(418, {
            message:
                'Good job! You hacked the server! Take a screenshot of the request response, head to https://imgbb.com/, upload it and paste the link in the input box.',
        });
    }
}

export async function POST({ request }: { request: Request }) {
    leakedSecretsGame(request.headers);
    isAuthenticated(request.headers);
    let body = {} as DepartmentQuestions;

    try {
        body = await request.json();
    } catch (e) {
        throw error(400, {
            message: (e as Error).toString(),
        });
    }

    const updateValues = { $set: body };
    let document = null;

    try {
        document = await questions.findOneAndUpdate({ department: body.department }, updateValues, {
            upsert: true,
            returnDocument: ReturnDocument.AFTER,
        });
    } catch (e) {
        throw error(500, {
            message: (e as Error).toString(),
        });
    }

    const responseMessage = JSON.stringify({ document });
    return new Response(responseMessage);
}
