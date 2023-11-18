import json

from bson.errors import InvalidId
from bson.json_util import dumps
from bson.objectid import ObjectId
from fastapi.responses import JSONResponse
from py_api.database.initialize import participants_col
from py_api.models import NewParticipant, UpdateParticipant
from py_api.utilities.jwt_creation import create_verification_jwt_token
from py_api.utilities.parsers import filter_none_values


class ParticipantsController:

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
            print(create_verification_jwt_token(specified_participant))

            print(create_verification_jwt_token(specified_participant))
        except (InvalidId, TypeError) as e:
            return JSONResponse(content={"message": "Invalid object_id format!"}, status_code=400)

        if not specified_participant:
            return JSONResponse(content={"message": "The targeted participant was not found!"}, status_code=404)

        return JSONResponse(content={"participant": json.loads(dumps(specified_participant))}, status_code=200)

    def delete_participant(object_id: str) -> JSONResponse:
        deleted_participant = participants_col.find_one_and_delete(
            filter={"_id": ObjectId(object_id)},
        )

        if not deleted_participant:
            return JSONResponse(content={"message": "The targeted participant was not found!"}, status_code=404)

        return JSONResponse(content={"message": "The participant was deleted successfully!"}, status_code=200)

    def update_participant(object_id: str, participant_form: UpdateParticipant) -> JSONResponse:

        # filters the values set to None in the model
        fields_to_be_updated = filter_none_values(participant_form)

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

        if participants_col.find_one(filter={"email": participant_form_dump["email"]}):
            return JSONResponse(content={"message": "The email of the participant already exists!"}, status_code=409)

        participants_col.insert_one(participant_form_dump)
        return JSONResponse(content={"message": "The participant was successfully added!"}, status_code=200)
