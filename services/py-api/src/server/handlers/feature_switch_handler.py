from result import Result, Ok, Err
from src.server.handlers.base_handler import BaseHandler
from src.service.feature_switch_service import FeatureSwitchService

class FeatureSwitchHandler(BaseHandler):

    def __init__(self, service: FeatureSwitchService) -> None:
        self._service = service

    async def check_registration_status(self) -> Result[bool, str]:
        result = await self._service.is_registration_open()

        if result:
            return Ok(True)
        else:
            return Err("Registration is closed")