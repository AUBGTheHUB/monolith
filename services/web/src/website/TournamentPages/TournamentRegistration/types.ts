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
