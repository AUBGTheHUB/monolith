from typing import Any, Dict, Tuple

from bson import ObjectId
from py_api.database.initialize import client, participants_col
from py_api.functionality.hackathon.teams_base import TeamFunctionality
from py_api.models.hackathon_participants_models import (
    NewParticipant,
    UpdateParticipant,
)
from pymongo import results


class ParticipantsFunctionality:
    pcol = participants_col

    @classmethod
    def check_if_email_exists(cls, email: str) -> bool:
        if participants_col.find_one(filter={"email": email}):
            return True

        return False

    @classmethod
    def insert_participant(cls, participant: NewParticipant) -> results.InsertOneResult:
        with client.start_session() as session:
            with session.start_transaction():
                new_participant = cls.pcol.insert_one(
                    participant.model_dump(), session=session,
                )
                return new_participant

    @classmethod
    def delete_participant(cls, object_id: str) -> results.DeleteResult | None:
        return cls.pcol.delete_one({"_id": object_id})

    @classmethod
    def update_participant(cls, object_id: str, participant: UpdateParticipant | NewParticipant) -> Any:
        obj = {
            key: value for key, value in participant.model_dump().items() if
            value != None
        }

        cls.pcol.find_one_and_update(
            {"_id": ObjectId(object_id)}, {"$set": obj},
        )
        # Returns the updated participant
        return cls.pcol.find_one({"_id": ObjectId(object_id)})

    @classmethod
    def remove_participant_from_team(cls, deleted_participant: Dict[str, Any]) -> Tuple[Dict[str, str], int]:
        team = TeamFunctionality.fetch_team(
            deleted_participant.get("team_name"),
        )
        if not team:
            return {"message": "The participant is not in a team"}, 404

        deleted_participant_id = str(deleted_participant["_id"])

        if deleted_participant_id in team.team_members:
            team.team_members.remove(deleted_participant_id)
        else:
            return {"message": "The participant is not in the specified team"}, 404

        updated_team = TeamFunctionality.update_team_query_using_dump(
            team.model_dump(),
        )
        if not updated_team:
            return {"message": "Something went wrong updating team document"}, 500

        return {"message": "The participant was deleted successfully from team!"}, 200
