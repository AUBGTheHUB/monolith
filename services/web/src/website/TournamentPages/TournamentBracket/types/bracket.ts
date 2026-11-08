export type Winner = 'first' | 'second' | null;

export type BackendGroup = {
    round: number;
    bracket_number: number;
    first: string | null;
    second: string | null;
    winner?: Winner;
};

export const TOTAL_ROUNDS = 3;
export const ROUND_TITLES = ['QUARTER-FINALS', 'SEMI-FINALS', 'FINALS'];

// round 1 -> 4 boxes, round 2 -> 2, round 3 -> 1
export const slotsInRound = (round: number) => 4 / 2 ** (round - 1);

export const findGroup = (groups: BackendGroup[], round: number, bracketNumber: number) =>
    groups.find((g) => g.round === round && g.bracket_number === bracketNumber);

export const getWinnerName = (group?: BackendGroup) => (group?.winner ? group[group.winner] : null);
