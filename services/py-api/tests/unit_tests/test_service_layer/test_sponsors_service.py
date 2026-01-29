from __future__ import annotations

from typing import cast

import pytest
from result import Err, Ok

from src.database.model.admin.sponsor_model import Sponsor, UpdateSponsorParams
from src.database.repository.admin.sponsors_repository import SponsorsRepository
from src.exception import SponsorNotFoundError
from src.server.schemas.request_schemas.admin.sponsor_schemas import (
    SponsorPostReqData,
    SponsorPatchReqData,
)
from src.service.admin.sponsors_service import SponsorsService
from tests.unit_tests.conftest import SponsorsRepoMock


@pytest.fixture
def sponsors_service(sponsors_repo_mock: SponsorsRepoMock) -> SponsorsService:
    return SponsorsService(cast(SponsorsRepository, sponsors_repo_mock))


@pytest.mark.asyncio
async def test_get_all_returns_ok(
    sponsors_service: SponsorsService, sponsors_repo_mock: SponsorsRepoMock, sponsor_mock: Sponsor
) -> None:
    sponsors = [sponsor_mock]
    sponsors_repo_mock.fetch_all.return_value = Ok(sponsors)

    result = await sponsors_service.get_all()

    assert result.is_ok()
    assert result.unwrap() == sponsors
    sponsors_repo_mock.fetch_all.assert_awaited_once()


@pytest.mark.asyncio
async def test_get_returns_ok(
    sponsors_service: SponsorsService,
    sponsors_repo_mock: SponsorsRepoMock,
    sponsor_mock: Sponsor,
) -> None:
    sponsors_repo_mock.fetch_by_id.return_value = Ok(sponsor_mock)

    result = await sponsors_service.get(str(sponsor_mock.id))

    assert result.is_ok()
    assert result.unwrap() == sponsor_mock
    sponsors_repo_mock.fetch_by_id.assert_awaited_once_with(str(sponsor_mock.id))


@pytest.mark.asyncio
async def test_get_returns_err_when_not_found(
    sponsors_service: SponsorsService, sponsors_repo_mock: SponsorsRepoMock
) -> None:
    sponsors_repo_mock.fetch_by_id.return_value = Err(SponsorNotFoundError())

    result = await sponsors_service.get("missing sponsor")

    assert result.is_err()
    assert isinstance(result.unwrap_err(), SponsorNotFoundError)
    sponsors_repo_mock.fetch_by_id.assert_awaited_once_with("missing sponsor")


@pytest.mark.asyncio
async def test_create_calls_repo_with_built_model(
    sponsors_service: SponsorsService, sponsors_repo_mock: SponsorsRepoMock, sponsor_mock: Sponsor
) -> None:
    req = SponsorPostReqData(
        name=sponsor_mock.name, tier=sponsor_mock.tier, website_url=sponsor_mock.website_url, logo_url=sponsor_mock.logo_url
    )

    sponsors_repo_mock.create.return_value = Ok(sponsor_mock)

    result = await sponsors_service.create(req)

    assert result.is_ok()
    sponsors_repo_mock.create.assert_awaited_once()

    assert sponsors_repo_mock.create.call_args is not None
    sponsor = sponsors_repo_mock.create.call_args.args[0]
    assert isinstance(sponsor, Sponsor)
    assert sponsor.name == req.name
    assert sponsor.tier == req.tier
    assert sponsor.website_url == str(req.website_url)
    assert sponsor.logo_url == str(req.logo_url)


@pytest.mark.asyncio
async def test_update_calls_repo_with_update_params(
    sponsors_service: SponsorsService, sponsors_repo_mock: SponsorsRepoMock, sponsor_mock: Sponsor
) -> None:
    req = SponsorPatchReqData(
        name=sponsor_mock.name, tier=sponsor_mock.tier, website_url=sponsor_mock.website_url, logo_url=sponsor_mock.logo_url
    )
    updated = Sponsor(
        name="New name", tier=sponsor_mock.tier, website_url=sponsor_mock.website_url, logo_url=sponsor_mock.logo_url
    )

    sponsors_repo_mock.update.return_value = Ok(updated)

    result = await sponsors_service.update(sponsor_mock.id, req)

    assert result.is_ok()
    sponsors_repo_mock.update.assert_awaited_once()

    assert sponsors_repo_mock.update.call_args is not None
    assert sponsors_repo_mock.update.call_args.args[0] == sponsor_mock.id
    updated_params = sponsors_repo_mock.update.call_args.args[1]
    assert isinstance(updated_params, UpdateSponsorParams)
    assert updated_params.name == req.name
    assert updated_params.tier == req.tier
    assert updated_params.website_url == str(req.website_url)
    assert updated_params.logo_url == str(req.logo_url)


@pytest.mark.asyncio
async def test_delete_calls_repo(
    sponsors_service: SponsorsService, sponsors_repo_mock: SponsorsRepoMock, sponsor_mock: Sponsor
) -> None:
    sponsors_repo_mock.delete.return_value = Ok(sponsor_mock)

    result = await sponsors_service.delete(str(sponsor_mock.id))

    assert result.is_ok()
    sponsors_repo_mock.delete.assert_awaited_once_with(str(sponsor_mock.id))
