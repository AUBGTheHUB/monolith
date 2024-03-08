from typing import Any, Dict, Tuple

from bson import ObjectId
from py_api.database.initialize import client, participants_col
from py_api.functionality.hackathon.teams_base import TeamFunctionality
from py_api.models.hackathon_participants_models import (
    NewParticipant,
    UpdateParticipant,
)
from pymongo import results
from pymongo.client_session import ClientSession


class ParticipantsFunctionality:
    pcol = participants_col

    @classmethod
    def check_if_email_exists(cls, email: str) -> bool:
        if participants_col.find_one(filter={"email": email}):
            return True

        return False

    @classmethod
    def insert_participant(cls, participant: NewParticipant, session: ClientSession | None = None) -> results.InsertOneResult:
        if session:
            return cls.pcol.insert_one(participant.model_dump(), session=session)

        with client.start_session() as session:
            with session.start_transaction():
                return cls.pcol.insert_one(
                    participant.model_dump(), session=session,
                )

    @classmethod
    def delete_participant(cls, object_id: str) -> results.DeleteResult | None:
        with client.start_session() as session:
            with session.start_transaction():
                return cls.pcol.delete_one({"_id": ObjectId(object_id)}, session=session)

    @classmethod
    def get_participant_by_id(cls, object_id: str) -> Any | None:
        return cls.pcol.find_one({"_id": ObjectId(object_id)})

    @classmethod
    def update_participant(cls, object_id: str, participant: UpdateParticipant | NewParticipant) -> Any:
        obj = {
            key: value for key, value in participant.model_dump().items() if
            value is not None
        }

        with client.start_session() as session:
            with session.start_transaction():
                return cls.pcol.find_one_and_update(
                    {"_id": ObjectId(object_id)}, {"$set": obj}, return_document=True,
                )

    @classmethod
    def remove_participant_from_team(cls, participant_id: str, team_name: str) -> Tuple[Dict[str, str], int]:
        team = TeamFunctionality.fetch_team(team_name=team_name)

        if not team:
            return {"message": "Team with such name does not exist"}, 404

        if participant_id in team.team_members:
            team.team_members.remove(participant_id)

        else:
            return {"message": "The participant is not in the specified team"}, 404

        updated_team = TeamFunctionality.update_team_query_using_dump(
            team.model_dump(),
        )

        if not updated_team:
            return {"message": "Something went wrong updating team document"}, 500

        return {"message": "The participant was deleted successfully from team!"}, 200
