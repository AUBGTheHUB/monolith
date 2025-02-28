from typing import List

from result import Result, is_err
from src.database.model.feature_switch_model import FeatureSwitch, UpdateFeatureSwitchParams
from src.database.repository.feature_switch_repository import FeatureSwitchRepository
from src.exception import FeatureSwitchNotFoundError


class FeatureSwitchService:
    def __init__(self, repository: FeatureSwitchRepository):
        self._repository = repository

    async def check_feature_switch(self, feature: str) -> Result[FeatureSwitch, FeatureSwitchNotFoundError | Exception]:
        return await self._repository.get_feature_switch(feature)

    async def check_all_feature_switches(self) -> Result[List[FeatureSwitch], Exception]:
        return await self._repository.fetch_all()

    async def update_feature_switch(
        self, name: str, state: bool
    ) -> Result[FeatureSwitch, FeatureSwitchNotFoundError | Exception]:

        return await self._repository.update_by_name(name=name, obj_fields=UpdateFeatureSwitchParams(state=state))

    async def toggle_feature_switch(
        self, feature_switch_id: str
    ) -> Result[FeatureSwitch, FeatureSwitchNotFoundError | Exception]:
        # Get the feature switch from the repository
        get_result = await self._repository.fetch_by_id(obj_id=feature_switch_id)

        if is_err(get_result):
            return get_result

        update_result = await self._repository.update(
            obj_id=feature_switch_id, obj_fields=UpdateFeatureSwitchParams(state=(not get_result.ok_value))
        )

        return update_result


def feature_switch_service_provider(repository: FeatureSwitchRepository) -> FeatureSwitchService:
    """
    Args:
        repository: A FeatureSwitchRepository instance

    Returns:
        A FeatureSwitchService instance
    """
    return FeatureSwitchService(repository)
