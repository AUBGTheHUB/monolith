from src.server.handlers.base_handler import BaseHandler
from src.service.auth.auth_service import AuthService
from src.server.schemas.response_schemas.schemas import Response


# TODO IMPLEMENT:
class AuthHandlers(BaseHandler):
    def __init__(self, service: AuthService) -> None:
        self._service = service

    # TODO: Create suitable request/response schemas

    def login(self) -> Response:
        raise NotImplementedError()

    def register(self) -> Response:
        raise NotImplementedError()

    def refresh_token(self) -> Response:
        raise NotImplementedError()
