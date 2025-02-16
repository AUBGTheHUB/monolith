from result import Result
from src.database.model.feature_switch_model import FeatureSwitch
from src.database.repository.feature_switch_repository import FeatureSwitchRepository
from src.server.exception import FeatureSwitchNotFoundError

class FeatureSwitchService:
    def __init__(self, repository: FeatureSwitchRepository):
        self._repository = repository

    async def check_feature_switch(self, feature: str) -> Result[FeatureSwitch, FeatureSwitchNotFoundError | Exception]:
        return await self._repository.get_feature_switch(feature)
        
