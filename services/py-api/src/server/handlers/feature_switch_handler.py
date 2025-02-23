from result import is_err
from src.server.handlers.base_handler import BaseHandler
from src.server.schemas.response_schemas.schemas import FeatureSwitchResponse, Response, AllFeatureSwitchesResponse
from src.service.feature_switch_service import FeatureSwitchService
from starlette import status


class FeatureSwitchHandler(BaseHandler):

    def __init__(self, service: FeatureSwitchService) -> None:
        self._service = service

    async def handle_feature_switch(self, feature: str) -> Response:
        result = await self._service.check_feature_switch(feature)

        if is_err(result):
            return self.handle_error(result.err_value)

        return Response(
            response_model=FeatureSwitchResponse(feature=result.ok_value),
            status_code=status.HTTP_200_OK,
        )

    async def handle_all_feature_switches(self) -> Response:
        result = await self._service.check_all_feature_switches()

        if is_err(result):
            return self.handle_error(result.err_value)

        return Response(
            response_model=AllFeatureSwitchesResponse(features=result.ok_value),
            status_code=status.HTTP_200_OK,
        )


def feature_switch_handlers_provider(service: FeatureSwitchService) -> FeatureSwitchHandler:
    """
    Args:
        service: A FeatureSwitchService instance

    Returns:
        A FeatureSwitchHandler instance
    """
    return FeatureSwitchHandler(service=service)
