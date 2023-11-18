from typing import Dict, Tuple

import jwt
from py_api.environment import SECRET_KEY


class VerificationController:
    @classmethod
    def verify_participant(cls, token: str) -> Tuple[Dict[str, str], int]:
        response, status_code = cls.verify_token(token)

        if status_code != 200:
            return response, status_code

        participant = response.get("_id")
        if not participant:
            return {"Message": f"Participant with id {response.get('_id')} does not exist!"}, 404

        return {"Message": "Your account has been verified"}, 200

    @classmethod
    def verify_token(cls, token: str) -> Tuple[Dict[str, str], int]:
        if not token:
            return {"Message": "No verification token provided"}, 401
        try:
            decoded_token = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        except jwt.exceptions.ExpiredSignatureError:
            return {"Message": "Verification link expired."}, 498
        except jwt.exceptions.InvalidSignatureError:
            return {"Message": "Invalid verification token signature."}, 401
        except jwt.exceptions.DecodeError:
            return {"Message": "Invalid or missing verification token."}, 401

        participant_id = decoded_token.get("sub", None)
        if not participant_id:
            return {"Message": "No participant_id provided"}, 403

        return {"participant_id": participant_id}, 200
