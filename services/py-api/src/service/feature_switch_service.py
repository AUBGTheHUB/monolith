from src.database.repository.feature_switch_repository import FeatureSwitchRepository

class FeatureSwitchService:
    def __init__(self, repository: FeatureSwitchRepository):
        self.repository = repository

    async def is_registration_open(self) -> bool:
        feature_switch = await self.repository.get_feature_switch("isRegistrationOpen")
        return feature_switch.state if feature_switch else False