export interface TournamentTeam {
    id: string;
    name: string;
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
