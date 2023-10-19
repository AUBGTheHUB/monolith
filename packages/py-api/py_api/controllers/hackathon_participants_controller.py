import json
from typing import Any, Dict

from bson.json_util import dumps
from bson.objectid import ObjectId
from fastapi.responses import JSONResponse
from py_api.database.initialize import participants_col
from py_api.models import NewParticipant, UpdateParticipant


class PartcipantsController:

    def filter_none_values(document: UpdateParticipant) -> Dict[str, Any]:
        # Creates a dictionary for participant_form
        participant_form_dump = document.model_dump()
        fields_to_be_updated = {}

        # It pushes the fields whose value is not null to the empty dictionary
        for key, value in participant_form_dump.items():
            if value:
                fields_to_be_updated[key] = value

        return fields_to_be_updated

    def get_all_participants() -> JSONResponse:
        participants = list(participants_col.find())

        if not participants:
            return JSONResponse(content={"message": "No participants were found!"}, status_code=404)

        # the dumps funtion from bson.json_util returns a string
        return JSONResponse(content={"participants": json.loads(dumps(participants))}, status_code=200)

    def get_specified_participant(object_id: str) -> JSONResponse:
        try:
            specified_participant = participants_col.find_one(
                filter={"_id": ObjectId(object_id)},
            )
        except:
            return JSONResponse(content={"message: Invalid object_id value!"})

        if not specified_participant:
            return JSONResponse(content={"message": "The targeted participant was not found!"}, status_code=404)

        return JSONResponse(content={"participant": json.loads(dumps(specified_participant))}, status_code=200)

    def delete_participant(object_id: str) -> JSONResponse:
        deleted_participant = participants_col.find_one_and_delete(
            filter={"_id": ObjectId(object_id)},
        )

        if not deleted_participant:
            return JSONResponse(content={"message": "The targeted participant was not found!"}, status_code=404)

        return JSONResponse(content={"message": "The participant was deletd successfully!"}, status_code=200)

    @classmethod
    def update_participant(cls, object_id: str, participant_form: UpdateParticipant) -> JSONResponse:

        # filters the values set to None in the model
        fields_to_be_updated = cls.filter_none_values(participant_form)

        # Queries the given participant and updates it
        to_be_updated_participant = participants_col.find_one_and_update(
            {"_id": ObjectId(object_id)}, {
                "$set": fields_to_be_updated,
            },
            return_document=True,
        )

        return JSONResponse(content={"participant": json.loads(dumps(to_be_updated_participant))}, status_code=200)

    def add_participant(participant_form: NewParticipant) -> JSONResponse:
        participant_form_dump = participant_form.model_dump()
        participant_email = participant_form_dump["email"]

        if participants_col.find_one(filter={"email": participant_email}):
            return JSONResponse(content={"message": "The email of the participant already exists!"}, status_code=409)

        participants_col.insert_one(participant_form_dump)
        return JSONResponse(content={"message": "The participant was successfully added!"}, status_code=200)
