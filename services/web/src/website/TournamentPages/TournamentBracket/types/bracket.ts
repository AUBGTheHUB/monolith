export type Winner = 'first' | 'second' | null;

export type Group = {
    round: number;
    bracket_number: number;
    first_team_id: string | null;
    first_team_name: string | null;
    second_team_id: string | null;
    second_team_name: string | null;
    winner_id: string | null;
    winner?: Winner;
};

export const TOTAL_ROUNDS = 3;
export const ROUND_TITLES = ['QUARTER-FINALS', 'SEMI-FINALS', 'FINALS'];

// round 1 -> 4 boxes, round 2 -> 2, round 3 -> 1
export const slotsInRound = (round: number) => 4 / 2 ** (round - 1);

export const findGroup = (groups: Group[], round: number, bracketNumber: number) =>
    groups.find((g) => g.round === round && g.bracket_number === bracketNumber);

export const getWinnerName = (groups: Group[]) => {
    if (groups) {
        const group = groups[groups.length - 1];
        if (group && group.round === 3 && group.winner_id) {
            if (group.winner_id === group.first_team_id) return group.first_team_name;
            if (group.winner_id === group.second_team_id) return group.second_team_name;
        }
    }
    return null;
};
