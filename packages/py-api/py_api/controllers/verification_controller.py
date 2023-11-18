# In your VerificationController
from typing import Dict, Tuple

import jwt
from bson.objectid import ObjectId
from fastapi.responses import JSONResponse
from py_api.database.initialize import participants_col
from py_api.environment import SECRET_KEY


class VerificationController:
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

    @classmethod
    def verify_token(cls, token: str) -> JSONResponse:
        if not token:
            return JSONResponse(content={"Message": "No verification token provided"}, status_code=401)
        try:
            decoded_token = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        except jwt.exceptions.ExpiredSignatureError:
            return JSONResponse(content={"Message": "Verification link expired"}, status_code=498)
        except jwt.exceptions.InvalidSignatureError:
            return JSONResponse(content={"Message": "Invalid verification token signature."}, status_code=401)
        except jwt.exceptions.DecodeError:
            return JSONResponse(content={"Message": "Invalid or missing verification token."}, status_code=401)

        participant_id = decoded_token.get("sub", None)
        if not participant_id:
            return JSONResponse(content={"Message": "No participant_id provided."}, status_code=403)

        return {"participant_id": participant_id}, 200
