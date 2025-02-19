from copy import deepcopy
from typing import Optional, List, cast, Any
from motor.motor_asyncio import AsyncIOMotorClientSession
from result import Result, Err, Ok

from src.database.db_manager import MongoDatabaseManager
from src.database.model.feature_switch_model import FeatureSwitch
from structlog.stdlib import get_logger
from src.database.repository.base_repository import CRUDRepository
from src.exception import FeatureSwitchNotFoundError

LOG = get_logger()


class FeatureSwitchRepository(CRUDRepository[FeatureSwitch]):
    def __init__(self, db_manager: MongoDatabaseManager, collection_name: str):
        self._collection = db_manager.get_collection(collection_name)

    async def get_feature_switch(self, feature: str) -> Result[FeatureSwitch, FeatureSwitchNotFoundError | Exception]:
        try:
            LOG.debug("Fetching feature switch by name...", feature=feature)
            feature_switch = await self._collection.find_one({"name": feature})

            if feature_switch is None:
                return Err(FeatureSwitchNotFoundError())

            feature_switch_copy = cast(dict[str, Any], deepcopy(feature_switch))

            feature_switch_copy["id"] = str(feature_switch_copy.pop("_id"))

            return Ok(FeatureSwitch(**feature_switch_copy))

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

                doc_copy = dict(doc)

                doc_copy["id"] = str(doc_copy.pop("_id"))

                feature_switches.append(FeatureSwitch(**doc_copy))

            LOG.debug(f"Fetched {len(feature_switches)} feature switches.")
            return Ok(feature_switches)

        except Exception as e:
            LOG.exception("Failed to fetch all feature switches due to error", error=e)
            return Err(e)

    async def fetch_by_id(self, obj_id: str) -> Result[FeatureSwitch, Exception]:
        return Err(NotImplementedError())

    async def update(
        self, obj_id: str, obj: FeatureSwitch, session: Optional[AsyncIOMotorClientSession] = None
    ) -> Result[FeatureSwitch, Exception]:
        return Err(NotImplementedError())


def feature_switch_repo_provider(db_manager: MongoDatabaseManager, collection_name: str) -> FeatureSwitchRepository:
    """
    Args:
        db_manager: A MongoDatabaseManager implementation instance
        collection_name: The name of the collection in the Mongo database

    Returns:
         A FeatureSwitchRepository instance.
    """
    return FeatureSwitchRepository(db_manager=db_manager, collection_name=collection_name)
