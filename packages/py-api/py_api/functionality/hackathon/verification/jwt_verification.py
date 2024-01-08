from datetime import datetime, timedelta
from typing import Any

import jwt
from jwt import encode
from py_api.environment import SECRET_KEY


class JWTVerification:
    @classmethod
    def decode_token(cls, token: str) -> Any:
        return jwt.decode(token, SECRET_KEY, algorithms=["HS256"])

    @classmethod
    def create_jwt_token(cls, team_name: str) -> str:
        payload = {
            "team_name": team_name,
            "exp": datetime.utcnow() + timedelta(hours=24),
        }
        return str(encode(payload, SECRET_KEY, algorithm="HS256"))
