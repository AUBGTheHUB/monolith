from datetime import datetime, timedelta
from typing import Any, Dict, Tuple

import jwt
from bson.objectid import ObjectId
from fastapi.responses import JSONResponse
from jwt import encode
from py_api.database.initialize import participants_col
from py_api.environment import SECRET_KEY


class JWTVerification:
    @classmethod
    def invite_participant(cls, token: str) -> Tuple[Dict[str, str], int]:
        response, status_code = cls.decode_query_param_token(
            token, is_verification=False,
        )

        if status_code != 200:
            return response, status_code

        team_name = response.get("team_name")
        if not team_name:
            return {"message": "Team name not found in the response."}, 404

        return {"team_name": team_name}, 200

    @classmethod
    def verify_participant(cls, token: str) -> Tuple[Dict[str, str], int]:
        response, status_code = cls.decode_query_param_token(
            token, is_verification=True,
        )

        if status_code != 200:
            return response, status_code

        participant_id = response.get("sub")
        if not participant_id:
            return {"message": "Participant ID not found in the response."}, 404

        participants_col.update_one(
            {"_id": ObjectId(participant_id)},
            {"$set": {"is_verified": True}},
        )

        return {"message": "Participant successfully verified."}, 200

    @classmethod
    def decode_query_param_token(cls, token: str, is_verification: bool) -> Tuple[Dict[str, str], int]:
        try:
            decoded_token = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        except jwt.exceptions.ExpiredSignatureError:
            message = "Verification link expired." if is_verification else "Invite link expired."
            return {"message": message}, 420
        except jwt.exceptions.InvalidSignatureError:
            message = "Invalid verification token signature." if is_verification else "Invalid invite token signature."
            return {"message": message}, 401
        except jwt.exceptions.DecodeError:
            message = "Invalid verification link." if is_verification else "Invalid invite link."
            return {"message": message}, 499

        return decoded_token, 200

    # when create verification jwt token is called it creates the token with argunment the participant
    # must be called when email is being created to create the url
    @classmethod
    def create_jwt_token(cls, team_name: str) -> str:
        payload = {
            "team_name": team_name,
            "exp": datetime.utcnow() + timedelta(hours=24),
        }
        return str(encode(payload, SECRET_KEY, algorithm="HS256"))
