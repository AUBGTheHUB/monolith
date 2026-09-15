import { API_URL } from '@/constants';
import  { CandidateForm, DEPARTMENTS_OPTIONS, Question, RegistrationInfo, ResendEmailType } from './constants';

export async function getQuestions(): Promise<{ questions: Question[] }> {
    let response: Response;
    try {
        response = await fetch(`${API_URL}/questions`);
    } catch {
        throw new Error('Unable to get questions from API');
    }

    if (!response.ok) {
        throw new Error('Unable to get questions from API');
    }

    return (await response.json()) as Promise<{ questions: Question[] }>;
}

export async function registerCandidate(data: CandidateForm): Promise<void> {
    let response: Response;
    try {
        const questions: Question[] = [
            ...data.form.generalQuestions,
            {
                prompt: 'Which department(s) would you like to apply for?',
                options: DEPARTMENTS_OPTIONS.map((d) => d.label),
                answer: data.form.departments.map((d) => d.toUpperCase()),
                question_type: 'GENERAL',
                answer_type: 'MULTIPLE_CHOICE',
            },
            ...data.form.developmentQuestions,
            ...data.form.designQuestions,
            ...data.form.marketingQuestions,
            ...data.form.prQuestions,
            ...data.form.logisticsQuestions,
        ];
        response = await fetch(`${API_URL}/candidate-forms`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                questions: questions
            }),
        })
    } catch {
        throw new Error('Unable to create candidate');
    }

    if (!response.ok) {
        throw new Error('Unable to create candidate');
    }
}

export async function registerParticipant(data: RegistrationInfo, token?: string): Promise<string> {
    const params = token ? new URLSearchParams({ jwt_token: token }) : undefined;

    let response: Response;
    try {
        response = await fetch(`${API_URL}/hackathon/participants?${params?.toString() ?? ''}`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data),
        });
    } catch {
        throw new Error('Registration failed, try refreshing the page or contact us.');
    }

    const responseData = await response.json();
    if (!response.ok) {
        throw new Error(responseData?.error || 'Registration failed, try refreshing the page or contact us.');
    }

    return responseData.participant?.id;
}

export async function resendEmail(data: ResendEmailType): Promise<void> {
    let response: Response;
    try {
        response = await fetch(`${API_URL}/hackathon/participants/verify/send-email`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data),
        });
    } catch {
        throw new Error('Failed to resend verification email. Please try again.');
    }

    if (!response.ok) {
        throw new Error('Failed to resend verification email.');
    }
}
