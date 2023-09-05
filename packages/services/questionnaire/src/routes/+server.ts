import { questions } from '$lib/database/mongo';
import { error } from '@sveltejs/kit';
import { ReturnDocument } from 'mongodb';
import type { DepartmentQuestions } from './types';

export async function POST({ request }: { request: any }) {
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
