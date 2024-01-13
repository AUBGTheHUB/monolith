from typing import Dict

from py_api.database.initialize import participants_col
from py_api.models.hackathon_participants_models import NewParticipant
from pymongo import results


class ParticipantsFunctionality:
    pcol = participants_col

    @classmethod
    def check_if_email_exists(cls, email: str) -> bool:
        if participants_col.find_one(filter={"email": email}):
            return True

        return False

    @classmethod
    def create_participant(cls, participant: NewParticipant) -> results.InsertOneResult | None:
        return cls.pcol.insert_one(participant.model_dump())
