export const RADIO_OPTIONS = [
    { label: 'Yes', value: true },
    { label: 'No', value: false },
];

export const TSHIRT_OPTIONS = [
    { label: 'Small (S)', value: 'Small (S)' },
    { label: 'Medium (M)', value: 'Medium (M)' },
    { label: 'Large (L)', value: 'Large (L)' },
];

export const LEVEL_OPTIONS = [
    { label: 'Beginner', value: 'Beginner' },
    { label: 'Intermediate', value: 'Intermediate' },
    { label: 'Advanced', value: 'Advanced' },
    { label: 'I am not participating as a programmer', value: 'I am not participating as a programmer' },
    { label: 'Other', value: 'Other' },
];

export const REFERRAL_OPTIONS = [
    { label: 'University', value: 'University' },
    { label: 'Friends', value: 'Friends' },
    { label: 'I was on a previous edition of Hack AUBG', value: 'I was on a previous edition of Hack AUBG' },
    { label: 'Other', value: 'Other' },
];

export const PROGRAMMING_LANGUAGE_OPTIONS = [
    { label: 'Programming in JavaScript', value: 'Programming in JavaScript' },
    { label: 'Programming in Python', value: 'Programming in Python' },
    { label: 'Programming in Java', value: 'Programming in Java' },
    { label: 'Programming in C++', value: 'Programming in C++' },
    { label: 'Programming in C#', value: 'Programming in C#' },
    { label: `I don't have experience with any languages`, value: `I don't have experience with any languages` },
    { label: 'Other', value: 'Other' },
];

export const REGISTRATION_TYPE_OPTIONS = [
    { label: 'Team', value: 'admin' },
    { label: 'Individual', value: 'random' },
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
