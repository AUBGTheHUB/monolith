export interface DecodedToken {
    sub: string;
    team_id: string;
    team_name: string;
    exp: number;
}

export const RESEND_COOLDOWN_SECONDS = 90;

export const REGISTRATION_CUTOFF_DATE = new Date('2026-03-14T00:00:00');

const currentDate = new Date();
export const registrationMessage =
    currentDate < REGISTRATION_CUTOFF_DATE ? 'Registration is coming soon...' : 'Registration is closed';
