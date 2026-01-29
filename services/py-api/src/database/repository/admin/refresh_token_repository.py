from typing import Optional
from bson import ObjectId
from pymongo import ReturnDocument
from result import Err, Ok, Result
from src.exception import RefreshTokenNotFound
from structlog.stdlib import get_logger
from motor.motor_asyncio import AsyncIOMotorClientSession

from src.database.mongo.collections.admin_collections import REFRESH_TOKENS
from src.database.mongo.db_manager import MongoDatabaseManager
from src.database.model.admin.refresh_token import RefreshToken, UpdateRefreshTokenParams
from src.database.repository.base_repository import CRUDRepository

LOG = get_logger()


class RefreshTokenRepository(CRUDRepository[RefreshToken]):
    def __init__(self, db_manager: MongoDatabaseManager) -> None:
        self._collection = db_manager.get_collection(REFRESH_TOKENS)

    async def create(
        self, refresh_token: RefreshToken, session: Optional[AsyncIOMotorClientSession] = None
    ) -> Result[RefreshToken, Exception]:
        try:
            LOG.info("Inserting refresh token for HUB member with id", hub_member_id=refresh_token.hub_member_id)
            await self._collection.insert_one(document=refresh_token.dump_as_mongo_db_document(), session=session)
            return Ok(refresh_token)

        except Exception as e:
            LOG.exception(
                f"Refresh token for HUB member with id {refresh_token.hub_member_id} insertion failed due to error {e}"
            )
            return Err(e)

    async def fetch_by_id(self, obj_id: str) -> Result[RefreshToken, RefreshTokenNotFound | Exception]:
        try:
            LOG.info("Fetching refresh token by ObjectID...", refresh_token_id=obj_id)
            refresh_token = await self._collection.find_one(filter={"_id": ObjectId(obj_id)})

            if refresh_token is None:
                return Err(RefreshTokenNotFound())

            refresh_token["id"] = refresh_token.pop("_id")
            return Ok(RefreshToken(**refresh_token))

        except Exception as e:
            LOG.exception(f"Failed to fetch refresh token due to error {e}")
            return Err(e)

    async def delete(
        self, obj_id: str, session: Optional[AsyncIOMotorClientSession] = None
    ) -> Result[RefreshToken, Exception]:
        try:
            LOG.info("Deleting refresh token...", refresh_token_id=obj_id)
            refresh_token = await self._collection.find_one_and_delete(filter={"_id": ObjectId(obj_id)})

            if refresh_token is None:
                return Err(RefreshTokenNotFound())

            refresh_token["id"] = refresh_token.pop("_id")
            return Ok(RefreshToken(**refresh_token))

        except Exception as e:
            LOG.exception("Refresh token deletion failed due to error", error=e)
            return Err(e)

    async def fetch_all(self) -> Result[list[RefreshToken], Exception]:
        try:
            LOG.info("Fetching all refresh tokens...")
            refresh_tokens_result = await self._collection.find({}).to_list(length=None)

            refresh_tokens = []
            for refresh_token in refresh_tokens_result:
                token = dict(refresh_token)
                token["id"] = token.pop("_id")
                refresh_tokens.append(token)

            return Ok(refresh_tokens)

        except Exception as e:
            LOG.exception("Could not fetch all refresh tokens due to error", error=e)
            return Err(e)

    async def update(
        self, obj_id: str, obj_fields: UpdateRefreshTokenParams, session: Optional[AsyncIOMotorClientSession] = None
    ) -> Result[RefreshToken, RefreshTokenNotFound | Exception]:
        try:
            LOG.info("Updating refresh token...", refresh_token_id=obj_id)

            refresh_token = await self._collection.find_one_and_update(
                filter={"_id": ObjectId(obj_id)},
                update={"$set": obj_fields.model_dump()},
                return_document=ReturnDocument.AFTER,
                session=session,
            )

            if refresh_token is None:
                return Err(RefreshTokenNotFound())

            refresh_token["id"] = refresh_token.pop("_id")
            return Ok(RefreshToken(**refresh_token))

        except Exception as e:
            LOG.exception("Could not update refresh token due to error", refresh_token_id=obj_id, error=e)
            return Err(e)
