from copy import deepcopy
from typing import Optional, List, cast
from motor.motor_asyncio import AsyncIOMotorClientSession
from result import Result, Err, Ok
from src.database.db_manager import DatabaseManager
from src.database.model.feature_switch_model import FeatureSwitch
from structlog.stdlib import get_logger
from src.database.repository.base_repository import CRUDRepository
from src.server.exception import FeatureSwitchNotFoundError

LOG = get_logger()


class FeatureSwitchRepository(CRUDRepository[FeatureSwitch]):
    def __init__(self, db_manager: DatabaseManager, collection_name: str):
        self._collection = db_manager.get_collection(collection_name)

    async def get_feature_switch(self, feature: str) -> Result[FeatureSwitch, FeatureSwitchNotFoundError | Exception]:
        try:
            LOG.debug("Fetching feature switch by name...", feature=feature)
            feature_switch = await self._collection.find_one({"name": feature})

            if feature_switch is None:
                return Err(FeatureSwitchNotFoundError())

            feature_switch_copy = cast(deepcopy(feature_switch), dict)

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
        return Err(NotImplementedError())

    async def fetch_by_id(self, obj_id: str) -> Result[FeatureSwitch, Exception]:
        return Err(NotImplementedError())

    async def update(
        self, obj_id: str, obj: FeatureSwitch, session: Optional[AsyncIOMotorClientSession] = None
    ) -> Result[FeatureSwitch, Exception]:
        return Err(NotImplementedError())
