from fastapi import Cookie, status
from result import is_err
from src.server.handlers.base_handler import BaseHandler
from src.server.schemas.request_schemas.auth.schemas import LoginHubAdminData, RegisterHubAdminData
from src.server.schemas.response_schemas.auth.schemas import (
    AccessTokenSuccessfullyIssued,
    HubMemberSuccessfullyRegistered,
)
from src.service.auth.auth_service import AuthService
from src.server.schemas.response_schemas.schemas import Response


class AuthHandlers(BaseHandler):
    def __init__(self, service: AuthService) -> None:
        self._service = service

    async def login(self, credentials: LoginHubAdminData) -> Response:

        result = await self._service.login_admin(credentials=credentials)

        if is_err(result):
            return self.handle_error(result.err_value)

        tokens = result.ok_value
        response = Response(
            AccessTokenSuccessfullyIssued(
                access_token=tokens[0],
            ),
            status_code=status.HTTP_200_OK,
        )

        response.set_cookie(key="refresh_token", value=tokens[1], httponly=True, secure=True)

        return response

    async def register(self, credentials: RegisterHubAdminData) -> Response:
        result = await self._service.register_admin(credentials=credentials)

        if is_err(result):
            return self.handle_error(result.err_value)

        return Response(HubMemberSuccessfullyRegistered(hub_admin=result.ok_value), status_code=status.HTTP_201_CREATED)

    async def refresh_token(self, refresh_token: str | None = Cookie(default=None)) -> Response:
        result = await self._service.refresh_token(refresh_token=refresh_token)

        if is_err(result):
            return self.handle_error(result.err_value)

        tokens = result.ok_value

        response = Response(
            AccessTokenSuccessfullyIssued(
                access_token=tokens[0],
            ),
            status_code=status.HTTP_200_OK,
        )

        response.set_cookie(key="refresh_token", value=tokens[1], httponly=True, secure=True)

        return response
