from typing import cast

import pytest
from result import Err, Ok
from starlette import status

from src.database.model.admin.hub_admin_model import HubAdmin, AssignableRole, Role
from src.exception import HubMemberNotFoundError
from src.server.handlers.user_handlers import UserHandlers
from src.server.schemas.request_schemas.user.schemas import UserRoleChangeRequest
from src.service.user.user_service import UserService
from tests.unit_tests.conftest import UserServiceMock


@pytest.fixture
def user_handlers(user_service_mock: UserServiceMock) -> UserHandlers:
    return UserHandlers(service=cast(UserService, user_service_mock))


@pytest.mark.asyncio
async def test_change_role_success(
    user_handlers: UserHandlers,
    user_service_mock: UserServiceMock,
    hub_admin_mock: HubAdmin,
) -> None:
    # Given
    user_id = str(hub_admin_mock.id)
    new_role = AssignableRole.DEV
    request_data = UserRoleChangeRequest(role=new_role)

    # Destructure dataclass and change the role for the expected object
    hub_admin_mock.site_role = Role.DEV
    user_service_mock.change_role.return_value = Ok(hub_admin_mock)

    # When
    resp = await user_handlers.change_role(object_id=user_id, data=request_data)

    # Then
    assert resp.status_code == status.HTTP_204_NO_CONTENT


async def test_change_role_not_found(
    user_handlers: UserHandlers,
    user_service_mock: UserServiceMock,
) -> None:
    # Given
    user_id = "non_existent_id"
    request_data = UserRoleChangeRequest(role=AssignableRole.BOARD)
    error = HubMemberNotFoundError(user_id)

    user_service_mock.change_role.return_value = Err(error)

    # When
    # BaseHandler.handle_error typically converts Errors to standard responses
    resp = await user_handlers.change_role(object_id=user_id, data=request_data)

    # Then
    # In your architecture, handle_error returns the specific error Response
    assert resp.status_code == status.HTTP_404_NOT_FOUND


async def test_change_role_internal_error(
    user_handlers: UserHandlers,
    user_service_mock: UserServiceMock,
) -> None:
    # Given
    user_id = "507f1f77bcf86cd799439011"
    request_data = UserRoleChangeRequest(role=AssignableRole.DEV)
    generic_error = Exception("Database connection failed")

    user_service_mock.change_role.return_value = Err(generic_error)
    # When
    resp = await user_handlers.change_role(object_id=user_id, data=request_data)

    # Then
    assert resp.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
