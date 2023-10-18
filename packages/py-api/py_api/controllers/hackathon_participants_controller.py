import json

from bson.json_util import dumps
from bson.objectid import ObjectId
from fastapi.responses import JSONResponse
from py_api.database.initialize import participants_col
from py_api.models import RandomParticipant
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
        specified_participant = participants_col.find_one(
            filter={"_id": ObjectId(object_id)},
        )

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
    def upsert_participant(cls, object_id: str, participant_form: RandomParticipant) -> JSONResponse:
        # Creates a dictionary for participant_form
        participant_form_dump = participant_form.model_dump()
        # Queries the given participant and updates it
        targeted_participant = participants_col.find_one_and_update(
            {"_id": ObjectId(object_id)}, {
                "$set": participant_form_dump,
            }, upsert=True,
            return_document=True,
        )

        return JSONResponse(content={"participant": json.loads(dumps(targeted_participant))}, status_code=200)

    @classmethod
    def add_participant(cls, participant_form: RandomParticipant) -> JSONResponse:
        participant_form_dump = participant_form.model_dump()
        # prohibited_chars = "'\";/:!@#$%\\[]^*()_-+{}=?.,§~`"

        # for e in participant_form_dump:
        #     if has_prohibited_characters(participant_form_dump[e], prohibited_chars):
        #         return JSONResponse(content={"message": f"Provided endpoint includes a prohibited character - {prohibited_chars}"}, status_code=400)

        participants_col.insert_one(participant_form_dump)
        return JSONResponse(content={"message": "The participant was successfully added!"}, status_code=200)
