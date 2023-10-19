import json

from bson.json_util import dumps
from bson.objectid import ObjectId
from fastapi.responses import JSONResponse
from py_api.database.initialize import participants_col
from py_api.models import NewParticipant
from py_api.utilities.parsers import has_prohibited_characters


class PartcipantsController:

    @classmethod
    def get_all_participants(cls) -> JSONResponse:
        participants = list(participants_col.find())

        if not participants:
            return JSONResponse(content={"message": "No participants were found!"}, status_code=404)

        # the dumps funtion from bson.json_util returns a string
        return JSONResponse(content={"participants": json.loads(dumps(participants))}, status_code=200)

    @classmethod
    def get_specified_participant(cls, object_id: str) -> JSONResponse:
        try:
            specified_participant = participants_col.find_one(
                filter={"_id": ObjectId(object_id)},
            )
        except:
            return JSONResponse(content={"message: Invalid object_id value!"})

        if not specified_participant:
            return JSONResponse(content={"message": "The targeted participant was not found!"}, status_code=404)

        return JSONResponse(content={"participant": json.loads(dumps(specified_participant))}, status_code=200)

    @classmethod
    def delete_participant(cls, object_id: str) -> JSONResponse:
        deleted_participant = participants_col.find_one_and_delete(
            filter={"_id": ObjectId(object_id)},
        )

        if not deleted_participant:
            return JSONResponse(content={"message": "The targeted participant was not found!"}, status_code=404)

        return JSONResponse(content={"message": "The participant was deletd successfully!"}, status_code=200)

    @classmethod
    def upsert_participant(cls, object_id: str, participant_form: NewParticipant) -> JSONResponse:
        # Creates a dictionary for participant_form
        participant_form_dump = participant_form.model_dump()
        # Queries the given participant and updates it
        to_be_updated_participant = participants_col.find_one_and_update(
            {"_id": ObjectId(object_id)}, {
                "$set": participant_form_dump,
            },
            return_document=True,
        )

        return JSONResponse(content={"participant": json.loads(dumps(to_be_updated_participant))}, status_code=200)

    @classmethod
    def add_participant(cls, participant_form: NewParticipant) -> JSONResponse:
        participant_form_dump = participant_form.model_dump()
        participant_email = participant_form_dump["email"]

        if participants_col.find_one(filter={"email": participant_email}):
            return JSONResponse(content={"message": "The email of the participant already exists!"}, status_code=409)

        participants_col.insert_one(participant_form_dump)
        return JSONResponse(content={"message": "The participant was successfully added!"}, status_code=200)
