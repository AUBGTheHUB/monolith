from result import Err, Ok, Result, is_err
from src.database.repository.feature_switch_repository import FeatureSwitchRepository

class FeatureSwitchService:
    def __init__(self, repository: FeatureSwitchRepository):
        self._repository = repository

    async def check_feature_switch(self, feature: str) -> Result[bool, str]:

        result = await self._repository.get_feature_switch(feature)

        if is_err(result):
            return Err("Feature switch not found or registration is closed")

        return result
        
