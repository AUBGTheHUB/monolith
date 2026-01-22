from __future__ import annotations

from typing import cast

import pytest
from result import Err, Ok

from src.database.model.admin.hub_member_model import HubMember, UpdateHubMemberParams
from src.database.repository.admin.hub_members_repository import HubMembersRepository
from src.exception import HubMemberNotFoundError
from src.server.schemas.request_schemas.admin.hub_member_schemas import (
    HubMemberPostReqData,
    HubMemberPatchReqData,
)
from src.service.admin.hub_members_service import HubMembersService
from tests.unit_tests.conftest import HubMembersRepoMock


@pytest.fixture
def hub_members_service(hub_members_repo_mock: HubMembersRepoMock) -> HubMembersService:
    return HubMembersService(cast(HubMembersRepository, hub_members_repo_mock))


@pytest.mark.asyncio
async def test_get_all_returns_ok(
    hub_members_service: HubMembersService, hub_members_repo_mock: HubMembersRepoMock, hub_member_mock: HubMember
) -> None:
    members = [hub_member_mock]
    hub_members_repo_mock.fetch_all.return_value = Ok(members)

    result = await hub_members_service.get_all()

    assert result.is_ok()
    assert result.unwrap() == members
    hub_members_repo_mock.fetch_all.assert_awaited_once()


@pytest.mark.asyncio
async def test_get_returns_ok(
    hub_members_service: HubMembersService,
    hub_members_repo_mock: HubMembersRepoMock,
    hub_member_mock: HubMember,
) -> None:
    hub_members_repo_mock.fetch_by_id.return_value = Ok(hub_member_mock)

    result = await hub_members_service.get(str(hub_member_mock.id))

    assert result.is_ok()
    assert result.unwrap() == hub_member_mock
    hub_members_repo_mock.fetch_by_id.assert_awaited_once_with(str(hub_member_mock.id))


@pytest.mark.asyncio
async def test_get_returns_err_when_not_found(
    hub_members_service: HubMembersService, hub_members_repo_mock: HubMembersRepoMock
) -> None:
    hub_members_repo_mock.fetch_by_id.return_value = Err(HubMemberNotFoundError())

    result = await hub_members_service.get("mii")

    assert result.is_err()
    assert isinstance(result.unwrap_err(), HubMemberNotFoundError)
    hub_members_repo_mock.fetch_by_id.assert_awaited_once_with("mii")


@pytest.mark.asyncio
async def test_create_calls_repo_with_built_model(
    hub_members_service: HubMembersService, hub_members_repo_mock: HubMembersRepoMock, hub_member_mock: HubMember
) -> None:
    from pydantic import HttpUrl

    req = HubMemberPostReqData(
        name=hub_member_mock.name,
        role_title=hub_member_mock.position,
        department=hub_member_mock.department,
        avatar_url=HttpUrl(hub_member_mock.avatar_url),
        social_links=hub_member_mock.social_links,
    )

    hub_members_repo_mock.create.return_value = Ok(hub_member_mock)

    result = await hub_members_service.create(req)

    assert result.is_ok()
    hub_members_repo_mock.create.assert_awaited_once()

    assert hub_members_repo_mock.create.call_args is not None
    passed_member = hub_members_repo_mock.create.call_args.args[0]
    assert isinstance(passed_member, HubMember)
    assert passed_member.name == req.name
    assert passed_member.position == req.role_title
    assert passed_member.department == req.department
    assert passed_member.avatar_url == str(req.avatar_url)


@pytest.mark.asyncio
async def test_update_calls_repo_with_update_params(
    hub_members_service: HubMembersService, hub_members_repo_mock: HubMembersRepoMock, hub_member_mock: HubMember
) -> None:
    from pydantic import HttpUrl

    req = HubMemberPatchReqData(name="new", role_title="new position")
    updated = HubMember(
        id=hub_member_mock.id,
        name="new",
        position="new position",
        department=hub_member_mock.department,
        avatar_url=hub_member_mock.avatar_url,
        social_links=hub_member_mock.social_links,
    )

    hub_members_repo_mock.update.return_value = Ok(updated)

    result = await hub_members_service.update(str(hub_member_mock.id), req)

    assert result.is_ok()
    hub_members_repo_mock.update.assert_awaited_once()

    assert hub_members_repo_mock.update.call_args is not None
    assert hub_members_repo_mock.update.call_args.args[0] == str(hub_member_mock.id)
    passed_params = hub_members_repo_mock.update.call_args.args[1]
    assert isinstance(passed_params, UpdateHubMemberParams)
    assert passed_params.name == req.name
    assert passed_params.position == req.role_title


@pytest.mark.asyncio
async def test_delete_calls_repo(
    hub_members_service: HubMembersService, hub_members_repo_mock: HubMembersRepoMock, hub_member_mock: HubMember
) -> None:
    hub_members_repo_mock.delete.return_value = Ok(hub_member_mock)

    result = await hub_members_service.delete(str(hub_member_mock.id))

    assert result.is_ok()
    hub_members_repo_mock.delete.assert_awaited_once_with(str(hub_member_mock.id))

