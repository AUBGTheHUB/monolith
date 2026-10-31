export const TEAM_OPTIONS = [
    { label: 'I already have a code', value: 'has_code' },
    { label: 'I want to register a team', value: 'create_team' },
    { label: 'I want to register solo', value: 'solo' },
];

export const RADIO_OPTIONS = [
    { label: 'Yes', value: true },
    { label: 'No', value: false },
];

export const LEAGUE_ROLES = [
    { label: 'Jungle', value: 'Jungle' },
    { label: 'Top Lane', value: 'Top Lane' },
    { label: 'Bot Lane', value: 'Bot Lane' },
    { label: 'Mid Lane', value: 'Mid Lane' },
    { label: 'Support', value: 'Support' },
];

export const UNIVERSITY_OPTIONS = [
    { label: 'American University in Bulgaria', value: 'American University in Bulgaria' },
    { label: 'Sofia University', value: 'Sofia University' },
    { label: 'Technical University - Sofia', value: 'Technical University - Sofia' },
    { label: 'Plovdiv University', value: 'Plovdiv University' },
    { label: 'Other', value: 'Other' },
];

export type TournamentRegistrationInfo = {
    registration_info: {
        first_name: string;
        last_name: string;
        email: string;
        university: string;
        location: string;
        age: number;
        team_name?: string;
    };
};

export type TournamentParticipantPayload = {
    full_name: string;
    age: number;
    email: string;
    university: string;
    location: string;
    share_info_with_sponsors: boolean;
    game_rank: string;
    primary_role: string;
    alternative_role: string;
};

export type TournamentAdminAndTeam = {
    tournament_participant: TournamentParticipantPayload;
    team_name: string;
};

export type TournamentMemberWithCode = {
    tournament_participant: TournamentParticipantPayload;
    team_code: string;
};
