import { questions } from '$lib/database/mongo';
import type { DepartmentQuestions } from './types';

/** @type {import('./$types').PageLoad} */
export async function load({ url }: { url: any }) {
    // fetch questions for department
    const department = url.searchParams.get('department');
    const result = (await questions.find({ department }).toArray()) as unknown as DepartmentQuestions[];

    return {
        questions: result[0].questions,
    };
}
