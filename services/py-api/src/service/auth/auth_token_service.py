from datetime import datetime, timedelta, timezone
from result import Result
from src.database.model.admin.hub_admin_model import HubAdmin
from src.service.jwt_utils.codec import JwtUtility
from src.service.jwt_utils.schemas import JwtAdminToken, JwtRefreshToken


class AuthTokenService:
    def __init__(self, jwt_utility: JwtUtility):
        self._jwt_utility = jwt_utility

    def generate_auth_token(self, hub_admin: HubAdmin) -> str:
        expiration = int((datetime.now(timezone.utc) + timedelta(minutes=7)).timestamp())
        payload = JwtAdminToken(
            sub=str(hub_admin.id), exp=expiration, site_role=hub_admin.site_role, member_type=hub_admin.member_type
        )
        return self._jwt_utility.encode_data(data=payload)

    def generate_refresh_token(self, refresh_token_id: str) -> str:
        refresh_expiration = int((datetime.now(timezone.utc) + timedelta(days=1)).timestamp())
        refresh_payload = JwtRefreshToken(sub=refresh_token_id, exp=refresh_expiration)

        return self._jwt_utility.encode_data(data=refresh_payload)

    def decode_refresh_token(self, refresh_token: str) -> Result[JwtRefreshToken, Exception]:
        return self._jwt_utility.decode_data(token=refresh_token, schema=JwtRefreshToken)
