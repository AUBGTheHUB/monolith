from datetime import datetime, timedelta
from typing import Dict, Tuple, TypedDict, cast

from jwt import (
    DecodeError,
    ExpiredSignatureError,
    InvalidSignatureError,
    decode,
    encode,
)
from py_api.environment import HUB_WEB_URL, IS_OFFLINE, SECRET_KEY

JWTType = TypedDict(
    'JWTType', {'sub': str, 'team_name': str, 'invite': bool, 'exp': datetime},
)


class JWTFunctionality:

    @classmethod
    def create_jwt_token(
            cls, participant_obj_id: str | None = None, team_name: str | None = None,
            is_invite: bool = False, is_participant_random: bool = False,
    ) -> str:
        payload = {
            "sub": participant_obj_id,
            "team_name": team_name,
            "invite": is_invite,
            "random_participant": is_participant_random,
            "exp": datetime.utcnow() + timedelta(days=30 if is_invite else 1),
        }

        return str(encode(payload, SECRET_KEY, algorithm="HS256"))

    @classmethod
    def decode_token(cls, jwt_token: str, is_invite: bool = False) -> JWTType | Tuple[Dict[str, str], int]:
        try:
            decoded_token = cast(
                JWTType, decode(
                    jwt_token, SECRET_KEY, algorithms=["HS256"],
                ),
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
    def get_email_link(
            cls, jwt_token: str,
            for_frontend: bool = False, is_invite: bool = False,
    ) -> str:

        if IS_OFFLINE:
            domain = f"{HUB_WEB_URL}:{'3000' if for_frontend else '6969'}"
        else:
            domain = HUB_WEB_URL

        if for_frontend:
            if is_invite:
                url = f"{domain}hackaubg?jwt_token={jwt_token}"
            else:
                url = f"{domain}hackaubg/verify?jwt_token={jwt_token}"

        elif is_invite:
            url = f"{domain}/v2/hackathon/participants?jwt_token={jwt_token}"

        else:
            url = f"{domain}/v2/hackathon/verify/participant?jwt_token={jwt_token}"

        return url
