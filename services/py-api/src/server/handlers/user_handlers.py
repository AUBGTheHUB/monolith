from result import is_err

from src.server.handlers.base_handler import BaseHandler
from src.server.schemas.request_schemas.user.schemas import UserRoleChangeRequest
from src.server.schemas.response_schemas.auth.schemas import UserResponse
from src.server.schemas.response_schemas.schemas import Response

from src.service.auth.user_service import UserService


class UserHandlers(BaseHandler):
    def __init__(self, service: UserService) -> None:
        self._service = service

    async def change_role(self, user_id: str, data: UserRoleChangeRequest) -> Response:
        result = await self._service.change_role(user_id, data.role)

        if is_err(result):
            return self.handle_error(result.err_value)

        return Response(response_model=UserResponse(hub_admin=result.ok_value), status_code=200)
