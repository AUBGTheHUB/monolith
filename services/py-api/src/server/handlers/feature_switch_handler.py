from fastapi import Response
from fastapi.responses import JSONResponse
from result import Err, Ok, Result, is_err
from src.server.handlers.base_handler import BaseHandler
from src.server.schemas.response_schemas.schemas import ErrResponse, RegistrationOpenResponse
from src.service.feature_switch_service import FeatureSwitchService
from starlette import status

class FeatureSwitchHandler(BaseHandler):

    def __init__(self, service: FeatureSwitchService) -> None:
        self._service = service

    async def handle_feature_switch(self, feature: str) -> Response:
        result = await self._service.check_feature_switch(feature)

        if is_err(result):
            return Response(
                content=ErrResponse(error=result.err_value).model_dump_json(),
                status_code=status.HTTP_409_CONFLICT,
                media_type="application/json"
            )

        return Response(
            content=RegistrationOpenResponse(feature=result.ok_value).model_dump_json(),
            status_code=status.HTTP_200_OK,
            media_type="application/json"
            )
