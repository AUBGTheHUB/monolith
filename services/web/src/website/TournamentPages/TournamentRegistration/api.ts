import { apiClient } from '@/services/apiClient';
import { TournamentRegistrationFormData } from './schema';
import { TournamentParticipantPayload, TournamentAdminAndTeam, TournamentMemberWithCode } from './types';

export function registerParticipant(data: TournamentRegistrationFormData): Promise<Response> {
    const participantData: TournamentParticipantPayload = {
        full_name: data.full_name,
        age: data.age,
        email: data.email,
        university: data.university,
        location: data.address,
        share_info_with_sponsors: data.share_info_with_sponsors,
        game_rank: data.rank,
        primary_role: data.primary_role,
        alternative_role: data.alternative_role,
    };

    if (data.team_option == 'create_team') {
        const adminPayload: TournamentAdminAndTeam = {
            tournament_participant: participantData,
            team_name: data.team_name ?? '',
        };

        return apiClient.post('/tournament/register/team', adminPayload);
    } else if (data.team_option == 'has_code') {
        const memberPayload: TournamentMemberWithCode = {
            tournament_participant: participantData,
            team_code: data.team_code ?? '',
        };

        return apiClient.post('/tournament/register/member', memberPayload);
    }
    return apiClient.post('/tournament/register/solo', participantData);
}
