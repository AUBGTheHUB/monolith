from typing import Optional
from pymongo.collection import Collection
from src.server.schemas.feature_switch_schemas.feature_switch_schema import FeatureSwitch

class FeatureSwitchRepository:
    def __init__(self, collection: Collection):
        self.collection = collection

    def get_feature_switch(self, feature: str) -> Optional[FeatureSwitch]:
        data = self.collection.find_one({"feature": feature})
        if data:
            return FeatureSwitch(**data)
        return None

    def set_feature_switch(self, feature_switch: FeatureSwitch):
        self.collection.update_one(
            {"feature": feature_switch.feature},
            {"$set": feature_switch.dict()},
            upsert=True
        )