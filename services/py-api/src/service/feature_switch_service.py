from result import Ok
from src.database.repository.feature_switch_repository import FeatureSwitchRepository

class FeatureSwitchService:
    def __init__(self, repository: FeatureSwitchRepository):
        self.repository = repository

    async def is_registration_open(self) -> bool:
        result = await self.repository.get_feature_switch("isRegistrationOpen")
        if isinstance(result, Ok):
            feature_switch = result.unwrap()
            return feature_switch.state
        return False