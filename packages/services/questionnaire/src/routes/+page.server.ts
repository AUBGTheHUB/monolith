import { questions } from '$lib/database/mongo';

/** @type {import('./$types').PageLoad} */
export function load({ url }: { url: any }) {
    // fetch questions for department
    const department = url.searchParams.get('department');
    console.log(questions.find());
}
