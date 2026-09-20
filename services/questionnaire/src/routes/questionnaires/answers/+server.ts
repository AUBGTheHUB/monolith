import { answers, questions } from '$lib/database/mongo';
import { error } from 'console';
import type { DepartmentQuestions } from '../../types';
import { BEARER_TOKEN } from '$env/static/private';

function isAuthorizedDepartment(headers: Headers, department: string) {
    return headers.get(`DEPARTMENT-TOKEN-${department.toUpperCase()}`) === BEARER_TOKEN || headers.get('BEARER-TOKEN') === BEARER_TOKEN;
}

type Body = {
    department: string;
    answers: Record<string, string>;
};

const verifyAnswers = (answers: Record<string, string> | null, questionnaire: DepartmentQuestions | null) => {
    if (!questionnaire) {
        throw new Error('Questionnaire was not found');
    }

    if (!answers) {
        throw new Error('No answers were provided');
    }

    const answersSet = new Set<string>();
    for (const key in answers) {
        answersSet.add(key);
    }

    const questionsSet = new Set(questionnaire.questions.map(question => question.title));

    const missingTitlesInAnswers = [...answersSet].filter(title => !questionsSet.has(title));
    const missingTitlesInQuestions = [...questionsSet].filter(title => !answersSet.has(title));

    if (missingTitlesInAnswers.length !== 0 || missingTitlesInQuestions.length !== 0) {
        throw new Error('The set of question titles provided does not match those in the questionnaire');
    }
};

export async function POST({ request }: { request: Request }) {
    let body = {} as Body;

    try {
        body = await request.json();
        const questionnaire = (await questions.findOne({ department: body.department })) as DepartmentQuestions | null;
        verifyAnswers(body.answers, questionnaire);
    } catch (e) {
        return new Response(JSON.stringify({ message: (e as Error).message }), {
            headers: { 'Content-Type': 'application/json' },
            status: 400,
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
