from __future__ import annotations

from typing import cast

import pytest
from fastapi import UploadFile
from pydantic import HttpUrl
from result import Err, Ok

from src.database.model.admin.sponsor_model import Sponsor
from src.database.repository.admin.sponsors_repository import SponsorsRepository
from src.exception import SponsorNotFoundError
from src.server.schemas.request_schemas.admin.sponsor_schemas import (
    SponsorPostReqData,
)
from src.service.admin.sponsors_service import SponsorsService
from src.service.utility.image_storing.image_storing_service import ImageStoringService
from tests.unit_tests.conftest import SponsorsRepoMock, ImageStoringServiceMock


@pytest.fixture
def sponsors_service(
    sponsors_repo_mock: SponsorsRepoMock, image_storing_service_mock: ImageStoringServiceMock
) -> SponsorsService:
    return SponsorsService(
        repo=cast(SponsorsRepository, sponsors_repo_mock),
        image_storing_service=cast(ImageStoringService, image_storing_service_mock),
    )


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
    sponsors_service: SponsorsService,
    sponsors_repo_mock: SponsorsRepoMock,
    image_storing_service_mock: ImageStoringServiceMock,
    sponsor_mock: Sponsor,
    image_mock: UploadFile,
) -> None:
    req = SponsorPostReqData(
        name=sponsor_mock.name, tier=sponsor_mock.tier, website_url=sponsor_mock.website_url, logo=image_mock
    )

    sponsors_repo_mock.create.return_value = Ok(sponsor_mock)
    image_storing_service_mock.upload_image.return_value = sponsor_mock.logo_url

    result = await sponsors_service.create(
        name=sponsor_mock.name, tier=sponsor_mock.tier, website_url=sponsor_mock.website_url, logo=image_mock
    )

    assert result.is_ok()
    sponsors_repo_mock.create.assert_awaited_once()

    assert sponsors_repo_mock.create.call_args is not None
    sponsor = sponsors_repo_mock.create.call_args.args[0]
    assert isinstance(sponsor, Sponsor)
    assert sponsor.name == req.name
    assert sponsor.tier == req.tier
    assert sponsor.website_url == str(req.website_url)
    assert sponsor.logo_url == sponsor_mock.logo_url


@pytest.mark.asyncio
async def test_update_calls_repo_with_update_params(
    sponsors_service: SponsorsService,
    sponsors_repo_mock: SponsorsRepoMock,
    image_storing_service_mock: ImageStoringServiceMock,
    sponsor_mock: Sponsor,
    image_mock: UploadFile,
) -> None:
    updated = Sponsor(
        name="New name", tier=sponsor_mock.tier, website_url=sponsor_mock.website_url, logo_url=sponsor_mock.logo_url
    )

    sponsors_repo_mock.update.return_value = Ok(updated)
    image_storing_service_mock.upload_image.return_value = HttpUrl(sponsor_mock.logo_url)

    result = await sponsors_service.update(
        sponsor_id=str(sponsor_mock.id),
        name=sponsor_mock.name,
        tier=sponsor_mock.tier,
        website_url=HttpUrl(sponsor_mock.website_url),
        logo=image_mock,
    )

    assert result.is_ok()
    sponsors_repo_mock.update.assert_awaited_once()

    assert sponsors_repo_mock.update.call_args is not None
    assert sponsors_repo_mock.update.call_args.args[0] == sponsor_mock.id

    body = result.ok_value
    assert body.name == updated.name
    assert body.tier == updated.tier
    assert body.website_url == updated.website_url


@pytest.mark.asyncio
async def test_delete_calls_repo(
    sponsors_service: SponsorsService,
    sponsors_repo_mock: SponsorsRepoMock,
    image_storing_service_mock: ImageStoringServiceMock,
    sponsor_mock: Sponsor,
) -> None:
    sponsors_repo_mock.delete.return_value = Ok(sponsor_mock)
    image_storing_service_mock.delete_image.return_value = f"sponsors/{str(sponsor_mock.id)}"

    result = await sponsors_service.delete(str(sponsor_mock.id))

    assert result.is_ok()
    sponsors_repo_mock.delete.assert_awaited_once_with(str(sponsor_mock.id))
    image_storing_service_mock.delete_image.assert_called_once_with(f"sponsors/{str(sponsor_mock.id)}")
