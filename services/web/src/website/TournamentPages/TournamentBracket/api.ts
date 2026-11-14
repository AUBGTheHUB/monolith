import { z } from 'zod';
import { apiClient } from '@/services/apiClient';
import { TournamentGroup } from '@/website/AdminPanelPage/DashboardPages/pages/TournamentManagementPage/types.ts';

const groupSchema = z.object({
    id: z.string().min(1),
    round: z.number().int().positive(),
    bracket_number: z.number().int().min(1).max(4),
    first_team_id: z.string().min(1).nullable(),
    second_team_id: z.string().min(1).nullable(),
    first_team_name: z.string().min(1).nullable(),
    second_team_name: z.string().min(1).nullable(),
    winner_id: z.string().min(1).nullable(),
});
const groupsSchema = z.object({ groups: z.array(groupSchema) });

export function parseGroups(response: unknown): TournamentGroup[] {
    const parsed = groupsSchema.safeParse(response);
    if (!parsed.success) {
        throw new Error('The server returned an unsupported group format. Please contact someone from Dev.');
    }
    const { groups } = parsed.data;
    if (new Set(groups.map((group) => group.id)).size !== groups.length) {
        throw new Error('The server returned duplicate groups. Please refresh the page.');
    }
    return groups.map((group) => {
        const teams: TournamentGroup['teams'] = [
            {
                id: group.first_team_id,
                name: group.first_team_name,
            },
            {
                id: group.second_team_id,
                name: group.second_team_name,
            },
        ];
        if (group.winner_id && !teams.some((team) => team?.id === group.winner_id)) {
            throw new Error('A group has an unknown winner. Please contact the tournament administrator.');
        }
        return {
            id: group.id,
            round: group.round,
            bracketNumber: group.bracket_number,
            teams,
            winnerId: group.winner_id ?? undefined,
        };
    });
}

export const tournamentApi = {
    getGroups: async () => parseGroups(await apiClient.get<unknown>('/groups')),
};
