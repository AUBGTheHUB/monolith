from typing import List

from result import Result
from src.database.model.feature_switch_model import FeatureSwitch
from src.database.repository.feature_switch_repository import FeatureSwitchRepository
from src.exception import FeatureSwitchNotFoundError


class FeatureSwitchService:
    def __init__(self, repository: FeatureSwitchRepository):
        self._repository = repository

    async def check_feature_switch(self, feature: str) -> Result[FeatureSwitch, FeatureSwitchNotFoundError | Exception]:
        return await self._repository.get_feature_switch(feature)

    async def check_all_feature_switches(self) -> Result[List[FeatureSwitch], Exception]:
        return await self._repository.fetch_all()


def feature_switch_service_provider(repository: FeatureSwitchRepository) -> FeatureSwitchService:
    """
    Args:
        repository: A FeatureSwitchRepository instance

    Returns:
        A FeatureSwitchService instance
    """
    return FeatureSwitchService(repository)
