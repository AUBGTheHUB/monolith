from __future__ import annotations

from typing import cast

import pytest
from result import Err, Ok

from src.database.model.admin.hub_member_model import HubMember
from src.exception import HubMemberNotFoundError
from src.server.handlers.admin.hub_members_handlers import HubMembersHandlers
from src.server.schemas.request_schemas.admin.hub_member_schemas import (
    HubMemberPostReqData,
    HubMemberPatchReqData,
)
from src.server.schemas.response_schemas.schemas import Response
from src.service.admin.hub_members_service import HubMembersService
from tests.unit_tests.conftest import HubMembersServiceMock


@pytest.fixture
def hub_members_handlers(hub_members_service_mock: HubMembersServiceMock) -> HubMembersHandlers:
    return HubMembersHandlers(cast(HubMembersService, hub_members_service_mock))


@pytest.mark.asyncio
async def test_create_hub_member_returns_201(
    hub_members_handlers: HubMembersHandlers,
    hub_members_service_mock: HubMembersServiceMock,
    hub_member_mock: HubMember,
) -> None:
    from pydantic import HttpUrl

    req = HubMemberPostReqData(
        name=hub_member_mock.name,
        position=hub_member_mock.position,
        department=hub_member_mock.department,
        avatar_url=HttpUrl(hub_member_mock.avatar_url),
        social_links=hub_member_mock.social_links,
    )

    hub_members_service_mock.create.return_value = Ok(hub_member_mock)

    resp = await hub_members_handlers.create_hub_member(req)

    assert isinstance(resp, Response)
    assert resp.status_code == 201
    hub_members_service_mock.create.assert_awaited_once_with(req)


@pytest.mark.asyncio
async def test_get_all_hub_members_returns_200(
    hub_members_handlers: HubMembersHandlers,
    hub_members_service_mock: HubMembersServiceMock,
    hub_member_mock: HubMember,
) -> None:
    hub_members_service_mock.get_all.return_value = Ok([hub_member_mock])

    resp = await hub_members_handlers.get_all_hub_members()

    assert resp.status_code == 200
    hub_members_service_mock.get_all.assert_awaited_once()


@pytest.mark.asyncio
async def test_get_hub_member_returns_200(
    hub_members_handlers: HubMembersHandlers,
    hub_members_service_mock: HubMembersServiceMock,
    hub_member_mock: HubMember,
) -> None:
    hub_members_service_mock.get.return_value = Ok(hub_member_mock)

    resp = await hub_members_handlers.get_hub_member(str(hub_member_mock.id))

    assert resp.status_code == 200
    hub_members_service_mock.get.assert_awaited_once_with(str(hub_member_mock.id))


@pytest.mark.asyncio
async def test_update_hub_member_returns_200(
    hub_members_handlers: HubMembersHandlers,
    hub_members_service_mock: HubMembersServiceMock,
    hub_member_mock: HubMember,
) -> None:
    pass

    req = HubMemberPatchReqData(
        name="Updated Name",
        position="Updated Position",
    )

    hub_members_service_mock.update.return_value = Ok(hub_member_mock)

    resp = await hub_members_handlers.update_hub_member(str(hub_member_mock.id), req)

    assert resp.status_code == 200
    hub_members_service_mock.update.assert_awaited_once_with(str(hub_member_mock.id), req)


@pytest.mark.asyncio
async def test_delete_hub_member_returns_200(
    hub_members_handlers: HubMembersHandlers,
    hub_members_service_mock: HubMembersServiceMock,
    hub_member_mock: HubMember,
) -> None:
    hub_members_service_mock.delete.return_value = Ok(hub_member_mock)

    resp = await hub_members_handlers.delete_hub_member(str(hub_member_mock.id))

    assert resp.status_code == 200
    hub_members_service_mock.delete.assert_awaited_once_with(str(hub_member_mock.id))


@pytest.mark.asyncio
async def test_get_hub_member_returns_404_when_missing(
    hub_members_handlers: HubMembersHandlers, hub_members_service_mock: HubMembersServiceMock
) -> None:
    hub_members_service_mock.get.return_value = Err(HubMemberNotFoundError())

    resp = await hub_members_handlers.get_hub_member("mii")

    assert resp.status_code == 404
    hub_members_service_mock.get.assert_awaited_once_with("mii")
