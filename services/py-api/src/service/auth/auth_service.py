from typing import Optional
from result import Err, Ok, Result, is_err
from motor.motor_asyncio import AsyncIOMotorClientSession

from src.database.model.admin.hub_admin_model import HubAdmin
from src.database.model.admin.refresh_token import RefreshToken
from src.database.mongo.transaction_manager import MongoTransactionManager
from src.database.repository.admin.hub_members_repository import HubMembersRepository
from src.database.repository.admin.refresh_token_repository import RefreshTokenRepository
from src.exception import (
    DuplicateHUBMemberNameError,
    HubMemberNotFoundError,
    PasssordsMismatchError,
    RefreshTokenNotFound,
)
from src.server.schemas.request_schemas.auth.schemas import LoginHubAdminData, RegisterHubAdminData
from src.service.auth.auth_token_service import AuthTokenService
from src.service.auth.password_hash_service import PasswordHashService


class AuthService:
    def __init__(
        self,
        hub_members_repo: HubMembersRepository,
        refresh_token_repo: RefreshTokenRepository,
        password_hash_service: PasswordHashService,
        auth_token_service: AuthTokenService,
        tx_manager: MongoTransactionManager,
    ) -> None:
        self._hub_members_repo = hub_members_repo
        self._password_hash_service = password_hash_service
        self._auth_token_service = auth_token_service
        self._refresh_token_repo = refresh_token_repo
        self._tx_manager = tx_manager

    async def login_admin(
        self, credentials: LoginHubAdminData
    ) -> Result[tuple[str, str], HubMemberNotFoundError | PasssordsMismatchError | Exception]:
        # Find admin from repo
        result = await self._hub_members_repo.fetch_admin_by_name(name=credentials.name)

        if is_err(result):
            return result

        hub_admin = result.ok_value

        # check_passwords
        passwords_match = self._password_hash_service.check_password(
            password_attempt=credentials.password, actual_password=hub_admin.password_hash
        )

        if not passwords_match:
            return Err(PasssordsMismatchError())

        # Build the auth token
        jwt_auth_token = self._auth_token_service.generate_auth_token(hub_admin=hub_admin)

        # Save the refresh token in db
        refresh_token = RefreshToken(hub_member_id=hub_admin.id)
        refresh_token_result = await self._refresh_token_repo.create(refresh_token=refresh_token)

        if is_err(refresh_token_result):
            return refresh_token_result

        refresh_token_id = refresh_token_result.ok_value.id

        # Build the actual refresh token
        jwt_refresh_token = self._auth_token_service.generate_refresh_token(refresh_token_id=str(refresh_token_id))

        return Ok((jwt_auth_token, jwt_refresh_token))

    async def register_admin(
        self, credentials: RegisterHubAdminData
    ) -> Result[HubAdmin, DuplicateHUBMemberNameError | Exception]:

        # Check if there is another admin with the same name
        hub_admin_exists = await self._hub_members_repo.check_if_admin_exists_by_name(credentials.name)

        if is_err(hub_admin_exists):
            return hub_admin_exists

        if hub_admin_exists.ok_value:
            return Err(DuplicateHUBMemberNameError())

        hub_admin = credentials.convert_to_hub_admin()
        hub_admin.password_hash = self._password_hash_service.hash_password(
            password_string=credentials.password
        ).decode("utf-8")

        result = await self._hub_members_repo.create(hub_member=hub_admin)

        if is_err(result):
            return result

        return Ok(result.ok_value)

    async def refresh_token(
        self, refresh_token: str | None
    ) -> Result[tuple[str, str], HubMemberNotFoundError | Exception]:

        if refresh_token is None:
            return Err(RefreshTokenNotFound())

        # Decode the refresh token
        decoded_token_result = self._auth_token_service.decode_refresh_token(refresh_token=refresh_token)

        if is_err(decoded_token_result):
            return decoded_token_result

        refresh_id = decoded_token_result.ok_value.sub

        # Find the refresh token in db
        refresh_token_result = await self._refresh_token_repo.fetch_by_id(refresh_id)

        if is_err(refresh_token_result):
            return refresh_token_result

        # Get the id of the hub admin for whom a new access token should be generated
        hub_admin_id = refresh_token_result.ok_value.hub_member_id

        # Find hub admin in db
        hub_admin_result = await self._hub_members_repo.fetch_by_id(obj_id=hub_admin_id)

        if is_err(hub_admin_result):
            return hub_admin_result

        hub_admin = hub_admin_result.ok_value

        # Generate new access token for hub admin
        jwt_auth_token = self._auth_token_service.generate_auth_token(hub_admin=hub_admin)

        # Delete the old refresh token in db and create a new one in transaction
        result = await self._tx_manager.with_transaction(
            callback=self._delete_old_and_create_new_refresh_token_callback, refresh_token_id=refresh_id
        )

        if is_err(result):
            return result

        new_refresh_id = result.ok_value.id

        # Generate new refresh token
        jwt_refresh_token = self._auth_token_service.generate_refresh_token(refresh_token_id=str(new_refresh_id))

        return Ok((jwt_auth_token, jwt_refresh_token))

    async def _delete_old_and_create_new_refresh_token_callback(
        self, refresh_token_id: str, session: Optional[AsyncIOMotorClientSession] = None
    ) -> Result[RefreshToken, Exception]:

        # Delete the old refresh token
        deleted_token_result = await self._refresh_token_repo.delete(obj_id=refresh_token_id, session=session)

        if is_err(deleted_token_result):
            return deleted_token_result

        hub_admin_id = deleted_token_result.ok_value.hub_member_id

        new_refresh_token = RefreshToken(hub_member_id=hub_admin_id)
        new_token_result = await self._refresh_token_repo.create(new_refresh_token, session=session)

        if is_err(new_token_result):
            return new_token_result

        return Ok(new_token_result.ok_value)
