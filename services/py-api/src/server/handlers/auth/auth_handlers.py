from result import is_err
from starlette.responses import Response as StarletteResponse
from fastapi import Cookie, HTTPException, status, Depends, UploadFile, File

from src.server.handlers.base_handler import BaseHandler
from src.server.schemas.request_schemas.auth.schemas import LoginHubAdminData, RegisterHubAdminData
from src.server.schemas.response_schemas.auth.schemas import AccessTokenSuccessfullyIssued, AuthTokensSuccessfullyIssued
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
            AuthTokensSuccessfullyIssued(access_token=tokens.access_token, id_token=tokens.id_token),
            status_code=status.HTTP_200_OK,
        )

        response.set_cookie(
            key="refresh_token", value=tokens.refresh_token, httponly=True, secure=True, samesite="strict"
        )

        return response

    async def register(
        self, credentials: RegisterHubAdminData = Depends(RegisterHubAdminData.as_form), avatar: UploadFile = File(...)
    ) -> StarletteResponse:
        result = await self._service.register_admin(credentials=credentials, avatar=avatar)

        if is_err(result):
            error_response = self.handle_error(result.err_value)
            raise HTTPException(
                status_code=error_response.status_code,
                detail=error_response.response_model.error,
                headers=dict(error_response.headers),
            )

        return StarletteResponse(status_code=status.HTTP_204_NO_CONTENT)

    async def refresh_token_pair(self, refresh_token: str | None = Cookie(default=None)) -> Response:
        result = await self._service.refresh_token(refresh_token=refresh_token)

        if is_err(result):
            return self.handle_error(result.err_value)

        tokens = result.ok_value

        response = Response(
            AccessTokenSuccessfullyIssued(
                access_token=tokens.access_token,
            ),
            status_code=status.HTTP_200_OK,
        )

        response.set_cookie(
            key="refresh_token", value=tokens.refresh_token, httponly=True, secure=True, samesite="strict"
        )

        return response
