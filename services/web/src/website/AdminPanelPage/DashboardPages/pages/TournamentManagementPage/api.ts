import { z } from 'zod';
import { apiClient } from '@/services/apiClient';
import type { TournamentGroup, TournamentTeam } from './types';

// Group.dump_as_json in backend PR #1387 returns team IDs without display names.
const teamSchema = z
    .string()
    .min(1)
    .transform((id) => ({ id, name: id }))
    .nullable();
const groupSchema = z.object({
    id: z.string().min(1),
    round: z.number().int().positive(),
    bracket_number: z.number().int().min(1).max(4),
    first_team_id: teamSchema,
    second_team_id: teamSchema,
    winner_id: z.string().min(1).nullable(),
});
const groupsSchema = z.object({ groups: z.array(groupSchema) });

export function parseGroups(response: unknown): TournamentGroup[] {
    const parsed = groupsSchema.safeParse(response);
    if (!parsed.success) {
        throw new Error(
            'The server returned an unsupported group format. Please contact someone from Dev.',
        );
    }
    const { groups } = parsed.data;
    if (new Set(groups.map((group) => group.id)).size !== groups.length) {
        throw new Error('The server returned duplicate groups. Please refresh the page.');
    }
    return groups.map((group) => {
        const teams: TournamentGroup['teams'] = [group.first_team_id, group.second_team_id];
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
    getActive: async () => parseGroups(await apiClient.get<unknown>('/groups/active')),
    getInactive: async () => parseGroups(await apiClient.get<unknown>('/groups/inactive')),
    generateBracket: () => apiClient.get<unknown>('/groups/generate-bracket'),
    declareWinner: (groupId: string, team: TournamentTeam) => {
        const endpoint = `/groups/${encodeURIComponent(groupId)}/declare-winner`;
        const query = new URLSearchParams({ winner_id: team.id });
        return apiClient.post<unknown, undefined>(`${endpoint}?${query}`, undefined);
    },
};
