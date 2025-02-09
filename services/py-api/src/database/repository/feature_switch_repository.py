from typing import Optional
from pymongo.collection import Collection
from src.database.db_manager import DatabaseManager
from src.database.repository.base_repository import CRUDRepository
from src.server.schemas.feature_switch_schemas.feature_switch_schema import FeatureSwitch

class FeatureSwitchRepository(CRUDRepository[FeatureSwitch]):

    def __init__(self, db_manager: DatabaseManager, collection_name: str):
        self._collection = db_manager.get_collection(collection_name)

    async def get_feature_switch(self, feature: str) -> Optional[FeatureSwitch]:
        data = await self._collection.find_one({"feature": feature})
        if data:
            return FeatureSwitch(**data)
        return None

    async def set_feature_switch(self, feature_switch: FeatureSwitch):
        await self._collection.update_one(
            {"feature": feature_switch.feature},
            {"$set": feature_switch.dict()},
            upsert=True
        )