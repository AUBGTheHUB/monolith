from typing import Optional, List, cast, Any, Dict

from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorClientSession
from pymongo.asynchronous.collection import ReturnDocument
from result import Result, Err, Ok
from structlog.stdlib import get_logger

from src.database.model.feature_switch_model import FeatureSwitch, UpdateFeatureSwitchParams
from src.database.mongo.collections.admin_collections import FEATURE_SWITCH_COLLECTION
from src.database.mongo.db_manager import MongoDatabaseManager
from src.database.repository.base_repository import CRUDRepository
from src.exception import FeatureSwitchNotFoundError

LOG = get_logger()


class FeatureSwitchRepository(CRUDRepository[FeatureSwitch]):
    def __init__(self, db_manager: MongoDatabaseManager):
        self._collection = db_manager.get_collection(FEATURE_SWITCH_COLLECTION)

    async def get_feature_switch(self, feature: str) -> Result[FeatureSwitch, FeatureSwitchNotFoundError | Exception]:
        try:
            LOG.debug("Fetching feature switch by name...", feature=feature)
            feature_switch = cast(Dict[str, Any], await self._collection.find_one({"name": feature}))

            if feature_switch is None:
                return Err(FeatureSwitchNotFoundError())

            feature_switch["id"] = feature_switch.pop("_id")

            return Ok(FeatureSwitch(**feature_switch))

        except Exception as e:
            LOG.exception("Failed to fetch feature switch due to error", error=e, feature_name=feature)
            return Err(e)

    async def create(
        self, obj: FeatureSwitch, session: Optional[AsyncIOMotorClientSession] = None
    ) -> Result[FeatureSwitch, Exception]:
        return Err(NotImplementedError())

    async def delete(
        self, obj_id: str, session: Optional[AsyncIOMotorClientSession] = None
    ) -> Result[FeatureSwitch, Exception]:
        return Err(NotImplementedError())

    async def fetch_all(self) -> Result[List[FeatureSwitch], Exception]:

        try:
            LOG.info("Fetching all feature switches...")
            # Note that find does not require an await expression, because find merely creates a MotorCursor without
            # performing any operations on the server. MotorCursor methods such as to_list() perform actual operations.
            # Learn more: https://motor.readthedocs.io/en/stable/api-asyncio/asyncio_motor_collection.html#motor.motor_asyncio.AsyncIOMotorCollection.find
            feature_switches_data = await self._collection.find({}).to_list(length=None)

            feature_switches = []

            for doc in feature_switches_data:
                doc["id"] = doc.pop("_id")

                feature_switches.append(FeatureSwitch(**doc))

            LOG.debug(f"Fetched {len(feature_switches)} feature switches.")
            return Ok(feature_switches)

        except Exception as e:
            LOG.exception("Failed to fetch all feature switches due to error", error=e)
            return Err(e)

    async def fetch_by_id(self, obj_id: str) -> Result[FeatureSwitch, FeatureSwitchNotFoundError | Exception]:
        try:
            LOG.debug("Fetching feature switch by ObjectID...", feature_switch_id=obj_id)

            # Query the database for the feature switch with the given object id
            feature_switch = await self._collection.find_one(filter={"_id": ObjectId(obj_id)}, projection={"_id": 0})

            if feature_switch is None:  # If no feature switch is found, return an Err
                return Err(FeatureSwitchNotFoundError())

            return Ok(FeatureSwitch(id=ObjectId(obj_id), **feature_switch))

        except Exception as e:
            LOG.exception("Failed to fetch feature switch due to error", feature_switch_id=obj_id, error=e)
            return Err(e)

    async def update(
        self, obj_id: str, obj_fields: UpdateFeatureSwitchParams, session: Optional[AsyncIOMotorClientSession] = None
    ) -> Result[FeatureSwitch, FeatureSwitchNotFoundError | Exception]:
        try:
            LOG.info(f"Updating Feature Switch...", feature_switch_id=obj_id, updated_fields=obj_fields.model_dump())

            # ReturnDocument.AFTER returns the updated document instead of the original document which is the
            # default behaviour.
            result = await self._collection.find_one_and_update(
                filter={"_id": ObjectId(obj_id)},
                update={"$set": obj_fields.model_dump()},
                projection={"_id": 0},
                return_document=ReturnDocument.AFTER,
                session=session,
            )

            # The result is None when the feature switch with the specified ObjectId is not found
            if result is None:
                return Err(FeatureSwitchNotFoundError())

            return Ok(FeatureSwitch(id=ObjectId(obj_id), **result))

        except Exception as e:
            LOG.exception("Failed to update the feature switch", feature_switch_id=obj_id, error=e)
            return Err(e)

    async def update_by_name(
        self, name: str, obj_fields: UpdateFeatureSwitchParams, session: Optional[AsyncIOMotorClientSession] = None
    ) -> Result[FeatureSwitch, FeatureSwitchNotFoundError | Exception]:
        try:
            LOG.info(f"Updating Feature Switch...", feature_switch_name=name, updated_fields=obj_fields.model_dump())

            # ReturnDocument.AFTER returns the updated document instead of the original document which is the
            # default behaviour.
            result = await self._collection.find_one_and_update(
                filter={"name": name},
                update={"$set": obj_fields.model_dump()},
                return_document=ReturnDocument.AFTER,
                session=session,
            )

            # The result is None when the feature switch with the specified ObjectId is not found
            if result is None:
                return Err(FeatureSwitchNotFoundError())

            result_dict = cast(Dict[str, Any], result)

            result_dict["id"] = result_dict.pop("_id")

            return Ok(FeatureSwitch(**result))

        except Exception as e:
            LOG.exception("Failed to update the feature switch", feature_switch_name=name, error=e)
            return Err(e)
