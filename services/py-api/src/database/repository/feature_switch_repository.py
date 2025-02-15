from typing import Optional, List
from motor.motor_asyncio import AsyncIOMotorClientSession
from result import Result, Err, Ok
from src.database.db_manager import DatabaseManager
from src.server.schemas.feature_switch_schemas.feature_switch_schema import FeatureSwitch
from structlog.stdlib import get_logger
from pymongo.collection import Collection
from src.database.repository.base_repository import CRUDRepository
from src.server.exception import FeatureSwitchNotFoundError

LOG = get_logger()

class FeatureSwitchRepository(CRUDRepository[FeatureSwitch]):
    def __init__(self, db_manager: DatabaseManager, collection_name: str):
        self._collection = db_manager.get_collection(collection_name)

    async def get_feature_switch(self, feature: str) -> Result[Ok, Err | Exception]:
        try:
            LOG.debug("Fetching feature switch by name...", feature=feature)
            data = await self._collection.find_one({"name": feature}, projection={"_id": 0})
            
            if data is None:
                return Err(FeatureSwitchNotFoundError())
            
            return Ok(FeatureSwitch(**data))
            
        except Exception as e:
            LOG.exception(f"Failed to fetch feature switch by feature {feature} due to err {e}")
            return Err(e)

    async def set_feature_switch(self, feature_switch: FeatureSwitch):
        await self._collection.update_one(
            {"feature": feature_switch.feature},
            {"$set": feature_switch.dict()},
            upsert=True
        )

    async def create(self, obj: FeatureSwitch, session: Optional[AsyncIOMotorClientSession] = None) -> Result[FeatureSwitch, Exception]:
        return Err(NotImplementedError())

    async def delete(self, obj_id: str, session: Optional[AsyncIOMotorClientSession] = None) -> Result[FeatureSwitch, Exception]:
        return Err(NotImplementedError())

    async def fetch_all(self) -> Result[List[FeatureSwitch], Exception]:
        return Err(NotImplementedError())

    async def fetch_by_id(self, obj_id: str) -> Result[FeatureSwitch, Exception]:
        return Err(NotImplementedError())

    async def update(self, obj_id: str, obj: FeatureSwitch, session: Optional[AsyncIOMotorClientSession] = None) -> Result[FeatureSwitch, Exception]:
        return Err(NotImplementedError())