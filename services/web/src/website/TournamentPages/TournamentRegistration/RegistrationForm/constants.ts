export const AGE_OPTIONS = Array.from({ length: 54 }, (_, i) => {
    const age = String(i + 16);
    return { label: age, value: age };
});

export const COUNTRY_OPTIONS = [
    { label: 'Bulgaria', value: 'Bulgaria' },
    { label: 'Albania', value: 'Albania' },
    { label: 'Georgia', value: 'Georgia' },
    { label: 'Kosovo', value: 'Kosovo' },
    { label: 'North Macedonia', value: 'North Macedonia' },
    { label: 'Romania', value: 'Romania' },
    { label: 'Serbia', value: 'Serbia' },
    { label: 'Turkey', value: 'Turkey' },
    { label: 'Ukraine', value: 'Ukraine' },
    { label: 'United Kingdom', value: 'United Kingdom' },
    { label: 'United States', value: 'United States' },
    { label: 'Other', value: 'Other' },
];
export const TEAM_OPTIONS = [
    { label: 'I already have a code', value: 'has_code' },
    { label: 'I want to register a team', value: 'create_team' },
    { label: 'I want to join a team', value: 'join_team' },
];

export const RADIO_OPTIONS = [
    { label: 'Yes', value: true },
    { label: 'No', value: false },
];

export const UNIVERSITY_OPTIONS = [
    { label: 'American University in Bulgaria', value: 'American University in Bulgaria' },
    { label: 'Sofia University', value: 'Sofia University' },
    { label: 'Technical University - Sofia', value: 'Technical University - Sofia' },
    { label: 'Plovdiv University', value: 'Plovdiv University' },
    { label: 'Other', value: 'Other' },
];


export type RegistrationInfo = {
    registration_info: {
        name: string;
        email: string;
        tshirt_size: string;
        university: string;
        location: string;
        age: number;
        source_of_referral: string;
        programming_language: string;
        programming_level: string;
        has_participated_in_hackaubg: boolean;
        has_internship_interest: boolean;
        has_participated_in_hackathons: boolean;
        has_previous_coding_experience: boolean;
        share_info_with_sponsors: boolean;
        registration_type: string;
        is_admin?: boolean | null;
        team_name?: string;
    };
};
