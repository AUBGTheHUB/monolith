export interface TournamentTeam {
    id: string | null;
    name: string | null;
}

export interface TournamentGroup {
    id: string;
    round: number;
    bracketNumber?: number;
    teams: [TournamentTeam | null, TournamentTeam | null];
    winnerId?: string;
}

export interface WinnerSelection {
    group: TournamentGroup;
    team: TournamentTeam;
}
