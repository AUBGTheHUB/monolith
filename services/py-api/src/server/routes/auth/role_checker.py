from result import is_err
from starlette.requests import Request
from fastapi import Header, HTTPException

from src.service.jwt_utils.schemas import JwtAdminToken
from src.database.model.admin.hub_admin_model import Role
from structlog.stdlib import get_logger

LOG = get_logger()


class RoleChecker:

    def __init__(self, allowed_roles: list[Role]):
        # This runs when you call RoleChecker("admin")
        self._allowed_roles = set(allowed_roles) | {Role.SUPER}

    async def __call__(self, request: Request, authorization: str = Header(..., alias="Authorization")) -> None:
        # This runs when the request hits the route
        jwt_utility = request.app.state.jwt_utility

        if not (authorization and authorization.startswith("Bearer ")):
            raise HTTPException(detail="Unauthorized", status_code=401)

        auth_token = authorization[len("Bearer ") :]
        decoded_token_result = jwt_utility.decode_data(token=auth_token, schema=JwtAdminToken)

        if is_err(decoded_token_result):
            error = decoded_token_result.err_value
            LOG.warning(error.message, error=error)
            raise HTTPException(status_code=401, detail="Unauthorized")

        token_data: JwtAdminToken = decoded_token_result.ok_value

        if token_data.site_role not in self._allowed_roles:
            LOG.warning("Role mismatch", allowed=self._allowed_roles, actual=token_data.site_role)
            raise HTTPException(status_code=403, detail=f"Access denied.")
