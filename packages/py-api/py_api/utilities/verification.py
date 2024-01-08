from datetime import datetime, timedelta
from typing import Any, Dict

from jwt import encode
from py_api.environment import SECRET_KEY

# TODO: Move to functionality folder

# when create verification jwt token is called it creates the token with argunment the participant
# must be called when email is being created to create the url


def create_verification_jwt_token(particiapnt: Dict[str, Any]) -> str:
    is_admin: bool = particiapnt["is_admin"]
    payload = {
        "sub": str(particiapnt["_id"]),
        "is_admin": is_admin,
        "exp": datetime.utcnow() + timedelta(hours=24),
    }
    return str(encode(payload, SECRET_KEY, algorithm="HS256"))


def create_invite_link(team: Dict[str, Any]) -> str:
    payload = {
        "sub": team["_id"],
        "team_name": team["team_name"],
        "exp": datetime.utcnow() + timedelta(hours=24),
    }

    return str(encode(payload, SECRET_KEY, algorithm="HS256"))
