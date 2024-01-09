from datetime import datetime, timedelta
from typing import Any

import jwt
from py_api.environment import IS_OFFLINE, SECRET_KEY


class JWTFunctionality:
    @classmethod
    def decode_token(cls, token: str) -> Any:
        return jwt.decode(token, SECRET_KEY, algorithms=["HS256"])

    @classmethod
    def create_jwt_token(cls, team_name: str) -> str:
        payload = {
            "team_name": team_name,
            "exp": datetime.utcnow() + timedelta(hours=24),
        }
        return str(jwt.encode(payload, SECRET_KEY, algorithm="HS256"))

    @classmethod
    def get_verification_link(cls, jwt_token: str, domain: str = "https://thehub-aubg.com", for_frontend: bool = False) -> str:
        IS_OFFLINE = False
        if IS_OFFLINE:
            domain = f"http://localhost:{'3000' if for_frontend else '6969'}"

        if for_frontend:
            url = f"{domain}/hackaubg?jwt_token={jwt_token}"
        else:
            url = f"{domain}/v2/hackathon/verify/admin?jwt_token={jwt_token}"

        return url
