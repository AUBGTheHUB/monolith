from datetime import datetime, timedelta
from typing import Any, Dict, Tuple

from jwt import (
    DecodeError,
    ExpiredSignatureError,
    InvalidSignatureError,
    decode,
    encode,
)
from py_api.environment import IS_OFFLINE, SECRET_KEY


class JWTFunctionality:

    @classmethod
    def create_jwt_token(
            cls, participant_obj_id: str | None = None, team_name: str | None = None,
            is_invite: bool = False, ) -> str:
        payload = {
            "sub": participant_obj_id,
            "team_name": team_name,
            "invite": False,
            "exp": datetime.utcnow() + timedelta(hours=24),
        }

        if is_invite:
            payload["invite"] = True

        return str(encode(payload, SECRET_KEY, algorithm="HS256"))

    @classmethod
    def decode_token(cls, jwt_token: str, is_invite: bool = False) -> Dict[str, Any] | Tuple[Dict[str, str], int]:
        try:
            decoded_token: Dict[str, Any] = decode(
                jwt_token, SECRET_KEY, algorithms=["HS256"],
            )
            return decoded_token

        except ExpiredSignatureError:
            message = "Verification link expired." if is_invite else "Invite link expired."
            return {"message": message}, 498

        except InvalidSignatureError:
            message = "Invalid verification token signature." if is_invite else "Invalid invite token signature."
            return {"message": message}, 401

        except DecodeError:
            message = "Invalid verification link." if is_invite else "Invalid invite link."
            return {"message": message}, 499

    @classmethod
    def get_verification_link(
        cls, jwt_token: str, domain: str = "https://thehub-aubg.com",
        for_frontend: bool = False,
    ) -> str:
        if IS_OFFLINE:
            domain = f"http://localhost:{'3000' if for_frontend else '6969'}"

        if for_frontend:
            url = f"{domain}/hackaubg?jwt_token={jwt_token}"
        else:
            url = f"{domain}/v2/hackathon/verify/participant?jwt_token={jwt_token}"

        return url