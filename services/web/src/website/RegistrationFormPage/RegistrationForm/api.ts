import { API_URL } from '@/constants';
import type { RegistrationInfo, ResendEmailType } from './constants';

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
