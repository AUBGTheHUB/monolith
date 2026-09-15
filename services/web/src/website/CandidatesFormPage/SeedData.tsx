import { API_URL } from '@/constants';
import { questionPrompts } from '@/website/CandidatesFormPage/QuestionPromps.ts';
import { FormEvent } from 'react';

export function SeedDataPage() {
    const seedData = async (form: FormEvent<HTMLFormElement>) => {
        form.preventDefault();
        const result = await fetch(`${API_URL}/questions/seed`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                questions: questionPrompts,
            }),
        });
        console.log(questionPrompts);
        console.log(result);
    };
    return (
        <form method="POST" onSubmit={seedData}>
            <button type="submit">Seed data</button>
        </form>
    );
}
