import { answers, questions } from '$lib/database/mongo';
import { error } from 'console';
import { ReturnDocument } from 'mongodb';

type Body = {
    answers: Answers[];
};

type Answers = {
    title: string;
    answer: string;
};

export async function POST({ request }: { request: Request }) {
    let body = {} as Body;

    try {
        body = await request.json();
    } catch (e) {
        throw error(400, {
            message: (e as Error).toString(),
        });
    }

    let document = null;

    try {
        document = await answers.insertOne(body);
    } catch (e) {
        throw error(500, {
            message: (e as Error).toString(),
        });
    }

    const responseMessage = JSON.stringify({ document });
    return new Response(responseMessage, { headers: { 'Content-Type': 'application/json' } });
}
