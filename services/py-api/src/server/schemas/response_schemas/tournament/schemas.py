from typing import Any

from pydantic import BaseModel, ConfigDict, field_serializer
from src.database.model.tournament_registration.tournament_participant_model import TournamentParticipant
from src.database.model.tournament_registration.tournament_team_model import TournamentTeam


class TournamentTeamAndParticipantResponse(BaseModel):
    """
    Responds upon a successful team and admin registration for the tournament
    or when a member is successfully added to the team via a team code
    """

    model_config = ConfigDict(arbitrary_types_allowed=True)

    tournament_team: TournamentTeam
    tournament_participant: TournamentParticipant

    @field_serializer("tournament_team")
    def serialize_tournament_team(self, tournament_team: TournamentTeam) -> dict[str, Any]:
        return tournament_team.dump_as_json()

    @field_serializer("tournament_participant")
    def serialize_judge(self, tournament_participant: TournamentParticipant) -> dict[str, Any]:
        return tournament_participant.dump_as_json()


class TournamentSoloParticipantResponse(BaseModel):
    """
    Responds upon a successful solo registration
    """

    model_config = ConfigDict(arbitrary_types_allowed=True)

    tournament_participant: TournamentParticipant

    @field_serializer("tournament_participant")
    def serialize_judge(self, tournament_participant: TournamentParticipant) -> dict[str, Any]:
        return tournament_participant.dump_as_json()
