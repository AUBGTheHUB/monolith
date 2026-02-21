export const ROLE_OPTIONS = [
    { label: 'Frontend Developer', value: 'frontend' },
    { label: 'Backend Developer', value: 'backend' },
    { label: 'UI/UX Designer', value: 'design' },
    { label: 'Project Manager', value: 'pm' },
    { label: 'Marketing Specialist', value: 'marketing' },
    { label: 'Something else', value: 'other' },
];

export const TRAIT_OPTIONS = [
    { label: 'Risk-taker', value: 'risk_taker' },
    { label: 'Observant', value: 'observant' },
    { label: 'Networker', value: 'networker' },
    { label: 'Reflective', value: 'reflective' },
    { label: 'Creator', value: 'creator' },
    { label: 'Problem finder', value: 'problem_finder' },
    { label: 'Problem solver', value: 'problem_solver' },
    { label: 'Empathetic', value: 'empathetic' },
    { label: 'Resilient', value: 'resilient' },
];

export type RegistrationInfo = {
    registration_info: {
        first_name: string;
        last_name: string;
        email: string;
        country: string;
        address: string;

        has_team: boolean;
        role: string;
        has_participated_in_hackathons: boolean;

        idea: string;
        challenge: string;
        motivation: string;
        best_describes: string;

        registration_type?: string;
        is_admin?: boolean | null;
        team_name?: string;
    };
};

export type ResendEmailType = {
    participant_id: string;
};
