from datetime import datetime
from typing import Optional

from fastapi import UploadFile, File
from result import Err, Ok, Result, is_err
from motor.motor_asyncio import AsyncIOMotorClientSession
from uuid import uuid4

from src.database.model.admin.refresh_token import RefreshToken, UpdateRefreshTokenParams
from src.database.mongo.transaction_manager import MongoTransactionManager
from src.database.repository.admin.hub_members_repository import HubMembersRepository
from src.database.repository.admin.refresh_token_repository import RefreshTokenRepository
from src.exception import (
    DuplicateHubMemberUsernameError,
    HubMemberNotFoundError,
    PasswordsMismatchError,
    RefreshTokenIsInvalid,
    RefreshTokenNotFound,
)
from src.server.schemas.dto_schemas.auth_dto_schemas import AdminTokens, AuthTokens
from src.server.schemas.request_schemas.auth.schemas import LoginHubAdminData, RegisterHubAdminData
from src.service.auth.auth_token_service import AuthTokenService
from src.service.auth.password_hash_service import PasswordHashService
from src.service.utility.image_storing.image_storing_service import ImageStoringService


class AuthService:
    def __init__(
        self,
        hub_members_repo: HubMembersRepository,
        refresh_token_repo: RefreshTokenRepository,
        password_hash_service: PasswordHashService,
        auth_token_service: AuthTokenService,
        tx_manager: MongoTransactionManager,
        image_storing_service: ImageStoringService,
    ) -> None:
        self._image_storing_service = image_storing_service
        self._hub_members_repo = hub_members_repo
        self._password_hash_service = password_hash_service
        self._auth_token_service = auth_token_service
        self._refresh_token_repo = refresh_token_repo
        self._tx_manager = tx_manager

    async def _invalidate_old_and_create_new_refresh_token_callback(
        self, refresh_token_id: str, refresh_expiration: datetime, session: Optional[AsyncIOMotorClientSession] = None
    ) -> Result[RefreshToken, Exception]:

        # Invalidate the old refresh token
        updated_token_result = await self._refresh_token_repo.update(
            refresh_token_id, obj_fields=UpdateRefreshTokenParams(is_valid=False), session=session
        )

        if is_err(updated_token_result):
            return updated_token_result

        hub_admin_id = updated_token_result.ok_value.hub_member_id
        family_id = updated_token_result.ok_value.family_id

        # Create new refresh token from this family id
        new_refresh_token = RefreshToken(
            hub_member_id=hub_admin_id, family_id=family_id, is_valid=True, expires_at=refresh_expiration
        )
        new_token_result = await self._refresh_token_repo.create(new_refresh_token, session=session)

        if is_err(new_token_result):
            return new_token_result

        return Ok(new_token_result.ok_value)

    async def login_admin(
        self, credentials: LoginHubAdminData
    ) -> Result[AdminTokens, HubMemberNotFoundError | PasswordsMismatchError | Exception]:
        # Find admin from repo
        result = await self._hub_members_repo.fetch_admin_by_username(username=credentials.username)

        if is_err(result):
            return result

        hub_admin = result.ok_value

        # check_passwords
        passwords_match = await self._password_hash_service.check_password(
            password_attempt=credentials.password, actual_password=hub_admin.password_hash
        )

        if not passwords_match:
            return Err(PasswordsMismatchError())

        # Build the auth token
        jwt_auth_token = self._auth_token_service.generate_access_token_for(hub_admin=hub_admin)

        # Build the id token
        jwt_id_token = self._auth_token_service.generate_id_token_for(hub_admin=hub_admin)

        # Save the refresh token in db
        family_id = str(uuid4())
        refresh_expiration = self._auth_token_service.generate_refresh_expiration()
        refresh_token = RefreshToken(
            hub_member_id=hub_admin.id, is_valid=True, family_id=family_id, expires_at=refresh_expiration
        )
        refresh_token_result = await self._refresh_token_repo.create(refresh_token=refresh_token)

        if is_err(refresh_token_result):
            return refresh_token_result

        refresh_token_id = refresh_token_result.ok_value.id

        # Build the refresh token
        jwt_refresh_token = self._auth_token_service.generate_refresh_token(
            refresh_token_id=str(refresh_token_id),
            family_id=family_id,
            hub_member_id=str(hub_admin.id),
            refresh_expiration=int(refresh_expiration.timestamp()),
        )
        tokens = AdminTokens(access_token=jwt_auth_token, id_token=jwt_id_token, refresh_token=jwt_refresh_token)
        return Ok(tokens)

    async def register_admin(
        self, credentials: RegisterHubAdminData, avatar: UploadFile = File(...)
    ) -> Result[None, DuplicateHubMemberUsernameError | Exception]:

        password_hash = await self._password_hash_service.hash_password(password_string=credentials.password)
        hub_admin = credentials.convert_to_hub_admin(password_hash=password_hash.decode("utf-8"), avatar_url="")

        avatar_url = await self._image_storing_service.upload_image(
            file=avatar, file_name=f"hub-members/{str(hub_admin.id)}"
        )
        hub_admin.avatar_url = str(avatar_url)
        result = await self._hub_members_repo.create(hub_member=hub_admin)

        if is_err(result):
            return result

        return Ok(None)

    async def refresh_token(
        self, refresh_token: str | None
    ) -> Result[AuthTokens, RefreshTokenNotFound | RefreshTokenIsInvalid | HubMemberNotFoundError | Exception]:

        if refresh_token is None:
            return Err(RefreshTokenNotFound())

        # Decode the refresh token
        decoded_token_result = self._auth_token_service.decode_refresh_token(refresh_token=refresh_token)

        if is_err(decoded_token_result):
            return decoded_token_result

        refresh_id = decoded_token_result.ok_value.jti
        family_id = decoded_token_result.ok_value.family_id

        # Find the refresh token in db
        refresh_token_result = await self._refresh_token_repo.fetch_by_id(refresh_id)

        if is_err(refresh_token_result):
            return refresh_token_result

        if not refresh_token_result.ok_value.is_valid:
            invalidate_result = await self._refresh_token_repo.invalidate_all_tokens_by_family_id(family_id=family_id)
            if is_err(invalidate_result):
                return invalidate_result
            return Err(RefreshTokenIsInvalid())

        # Get the id of the hub admin for whom a new access token should be generated
        hub_admin_id = refresh_token_result.ok_value.hub_member_id

        # Find hub admin in db
        hub_admin_result = await self._hub_members_repo.fetch_by_id(obj_id=hub_admin_id)

        if is_err(hub_admin_result):
            return hub_admin_result

        hub_admin = hub_admin_result.ok_value

        # Generate new access token for hub admin
        jwt_auth_token = self._auth_token_service.generate_access_token_for(hub_admin=hub_admin)

        refresh_expiration = self._auth_token_service.generate_refresh_expiration()
        # Invalidate the old refresh token in db and create a new one in transaction
        result = await self._tx_manager.with_transaction(
            callback=self._invalidate_old_and_create_new_refresh_token_callback,
            refresh_token_id=refresh_id,
            refresh_expiration=refresh_expiration,
        )

        if is_err(result):
            return result

        new_refresh_id = result.ok_value.id

        # Generate new refresh token
        jwt_refresh_token = self._auth_token_service.generate_refresh_token(
            refresh_token_id=str(new_refresh_id),
            family_id=family_id,
            refresh_expiration=int(refresh_expiration.timestamp()),
            hub_member_id=str(hub_admin.id),
        )

        tokens = AuthTokens(access_token=jwt_auth_token, refresh_token=jwt_refresh_token)
        return Ok(tokens)
