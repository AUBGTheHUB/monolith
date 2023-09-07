import { questions } from '$lib/database/mongo';
import type { DepartmentQuestions } from '../../types';
import { marked } from 'marked';

/** @type {import('./$types').PageLoad} */
export async function load({ params }: { params: Record<string, any> }) {
    const department = params?.department;
    const result = (await questions.find({ department }).toArray()) as unknown as DepartmentQuestions[];

    result[0].questions.forEach(async ({ body }, index) => {
        result[0].questions[index].body = marked.parse(body);
    });

    return {
        questions: result[0].questions,
        department,
    };
}
