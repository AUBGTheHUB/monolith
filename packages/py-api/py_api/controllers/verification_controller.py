from typing import Dict, Tuple

import jwt
from bson.objectid import ObjectId
from fastapi.responses import JSONResponse
from py_api.database.initialize import participants_col
from py_api.environment import SECRET_KEY


class VerificationController:
    @classmethod
    def invite(cls) -> JSONResponse:
        # TODO:
        #  - Check the cap of the team
        #  - If cap reached -> return proper message
        #  - Else insert a new participant document and add the inserted
        #  Object id to the list of paticipnats ids for the provided team (team_name from jwt)
        pass

    @classmethod
    def verify(cls) -> JSONResponse:
        # This is when a participant is registering (Either with a team or without one)
        # TODO:
        #   - 1. Check the result of the verify_participant
        #   - 2. Get the team_name from the jwt
        #   - 3. Based on it use the functions in py_api/functionality/hackathon/teams/teams_utility_functions.py to create a team
        #   You can look at a sample code snippet in the ad_participant func in py_api/controllers/hackathon_participants_controller.py
        pass

    # TODO: Move to functionality folder
    @classmethod
    def verify_participant(cls, token: str) -> Tuple[Dict[str, str], int]:
        response, status_code = cls.verify_token(token)

        if status_code != 200:
            return {"message": response.get("Message", "Verification failed")}, status_code

        participant_id = response.get("participant_id")
        if not participant_id:
            return {"message": "Participant ID not found in the response."}, 404

        try:
            participants_col.update_one(
                {"_id": ObjectId(participant_id)},
                {"$set": {"is_verified": True}},
            )
        except Exception as e:
            return {"message": f"Failed to update participant status. Error: {str(e)}"}, 500

        return {"message": "Participant ID is verified."}, 200

    # TODO: Move to functionality folder
    @classmethod
    def verify_token(cls, token: str) -> JSONResponse:
        if not token:
            return {'message': "No verification token provided"}, 401
        try:
            decoded_token = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        except jwt.exceptions.ExpiredSignatureError:
            return {'message': "Verification link expired"}, 498
        except jwt.exceptions.InvalidSignatureError:
            return {'message': "Invalid verification token signature."}, 401
        except jwt.exceptions.DecodeError:
            return {'message': "Invalid or missing verification token."}, 401
        participant_id = decoded_token.get("sub", None)
        if not participant_id:
            return {'message': "No participant_id provided."}, 403

        return {"participant_id": participant_id}, 200
