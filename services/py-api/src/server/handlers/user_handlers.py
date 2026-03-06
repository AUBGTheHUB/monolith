from result import is_err
from starlette import status
from starlette.responses import Response as StarletteResponse
from src.server.handlers.base_handler import BaseHandler
from src.server.schemas.request_schemas.user.schemas import UserRoleChangeRequest

from src.service.user.user_service import UserService


class UserHandlers(BaseHandler):
    def __init__(self, service: UserService) -> None:
        self._service = service

    async def change_role(self, object_id: str, data: UserRoleChangeRequest) -> StarletteResponse:
        result = await self._service.change_role(object_id, data.role)

        if is_err(result):
            return self.handle_error(result.err_value)
        return StarletteResponse(status_code=status.HTTP_204_NO_CONTENT)
