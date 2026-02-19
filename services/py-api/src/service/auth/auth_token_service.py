from datetime import datetime, timedelta, timezone
from result import Result
from src.database.model.admin.hub_admin_model import HubAdmin
from src.service.jwt_utils.codec import JwtUtility
from src.service.jwt_utils.schemas import JwtAdminToken, JwtIdToken, JwtRefreshToken


class AuthTokenService:
    def __init__(self, jwt_utility: JwtUtility):
        self._jwt_utility = jwt_utility

    def generate_access_token_for(self, hub_admin: HubAdmin) -> str:
        expiration = int((datetime.now(timezone.utc) + timedelta(minutes=7)).timestamp())
        payload = JwtAdminToken(sub=str(hub_admin.id), exp=expiration, member_type=hub_admin.member_type)
        return self._jwt_utility.encode_data(data=payload)

    def generate_id_token_for(self, hub_admin: HubAdmin) -> str:
        # TODO: Discuss expiration for id tokens
        expiration = int((datetime.now(timezone.utc) + timedelta(hours=10)).timestamp())
        payload = JwtIdToken(
            sub=str(hub_admin.id),
            exp=expiration,
            avatar_url=hub_admin.avatar_url,
            username=hub_admin.username,
            site_role=hub_admin.site_role,
        )

        return self._jwt_utility.encode_data(data=payload)

    def generate_refresh_token(
        self, hub_member_id: str, refresh_token_id: str, family_id: str, refresh_expiration: int
    ) -> str:

        refresh_payload = JwtRefreshToken(
            sub=hub_member_id, exp=refresh_expiration, family_id=family_id, jti=refresh_token_id
        )

        return self._jwt_utility.encode_data(data=refresh_payload)

    def generate_refresh_expiration(self) -> datetime:
        return datetime.now(timezone.utc) + timedelta(days=1)

    def decode_refresh_token(self, refresh_token: str) -> Result[JwtRefreshToken, Exception]:
        return self._jwt_utility.decode_data(token=refresh_token, schema=JwtRefreshToken)
