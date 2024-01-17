from typing import Any, Dict

from bson import ObjectId
from py_api.database.initialize import participants_col
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
    def create_participant(cls, participant: NewParticipant) -> results.InsertOneResult:
        new_participant = cls.pcol.insert_one(participant.model_dump())
        if new_participant.acknowledged:
            return new_participant

        raise Exception("Could not create participant")

    @classmethod
    def delete_participant(cls, id: str) -> results.DeleteResult | None:
        return cls.pcol.delete_one({"_id": id})

    @classmethod
    def update_participant(cls, id: str, participant: UpdateParticipant | NewParticipant) -> Any:
        obj = {
            key: value for key, value in participant.model_dump().items() if
            value
        }

        return cls.pcol.find_one_and_update({"_id": ObjectId(id)}, {"$set": obj})
