from __future__ import annotations

from typing import cast

import pytest
from result import Err, Ok

from src.database.model.admin.sponsor_model import Sponsor
from src.exception import SponsorNotFoundError
from src.server.handlers.admin.sponsors_handlers import SponsorsHandlers
from src.server.schemas.request_schemas.admin.sponsor_schemas import (
    SponsorPostReqData,
    SponsorPatchReqData,
)
from src.server.schemas.response_schemas.schemas import Response
from src.service.admin.sponsors_service import SponsorsService
from tests.unit_tests.conftest import SponsorsServiceMock


@pytest.fixture
def sponsors_handlers(sponsors_service_mock: SponsorsServiceMock) -> SponsorsHandlers:
    return SponsorsHandlers(cast(SponsorsService, sponsors_service_mock))


@pytest.mark.asyncio
async def test_create_sponsor_returns_201(
    sponsors_handlers: SponsorsHandlers,
    sponsors_service_mock: SponsorsServiceMock,
    sponsor_mock: Sponsor,
) -> None:
    req = SponsorPostReqData(
        name=sponsor_mock.name, tier=sponsor_mock.tier, website_url=sponsor_mock.website_url, logo_url=sponsor_mock.logo_url
    )

    sponsors_service_mock.create.return_value = Ok(sponsor_mock)

    resp = await sponsors_handlers.create_sponsor(req)

    assert isinstance(resp, Response)
    assert resp.status_code == 201
    sponsors_service_mock.create.assert_awaited_once_with(req)


@pytest.mark.asyncio
async def test_get_all_sponsors_returns_200(
    sponsors_handlers: SponsorsHandlers,
    sponsors_service_mock: SponsorsServiceMock,
    sponsor_mock: Sponsor,
) -> None:
    sponsors_service_mock.get_all.return_value = Ok([sponsor_mock])

    resp = await sponsors_handlers.get_all_sponsors()

    assert resp.status_code == 200
    sponsors_service_mock.get_all.assert_awaited_once()


@pytest.mark.asyncio
async def test_get_sponsor_returns_200(
    sponsors_handlers: SponsorsHandlers,
    sponsors_service_mock: SponsorsServiceMock,
    sponsor_mock: Sponsor,
) -> None:
    sponsors_service_mock.get.return_value = Ok(sponsor_mock)

    resp = await sponsors_handlers.get_sponsor(str(sponsor_mock.id))

    assert resp.status_code == 200
    sponsors_service_mock.get.assert_awaited_once_with(str(sponsor_mock.id))


@pytest.mark.asyncio
async def test_update_sponsor_returns_200(
    sponsors_handlers: SponsorsHandlers,
    sponsors_service_mock: SponsorsServiceMock,
    sponsor_mock: Sponsor,
) -> None:
    req = SponsorPatchReqData(
        name=sponsor_mock.name, tier=sponsor_mock.tier, website_url=sponsor_mock.website_url, logo_url=sponsor_mock.logo_url
    )

    sponsors_service_mock.update.return_value = Ok(sponsor_mock)

    resp = await sponsors_handlers.update_sponsor(str(sponsor_mock.id), req)

    assert resp.status_code == 200
    sponsors_service_mock.update.assert_awaited_once_with(str(sponsor_mock.id), req)


@pytest.mark.asyncio
async def test_delete_sponsor_returns_200(
    sponsors_handlers: SponsorsHandlers,
    sponsors_service_mock: SponsorsServiceMock,
    sponsor_mock: Sponsor,
) -> None:
    sponsors_service_mock.delete.return_value = Ok(sponsor_mock)

    resp = await sponsors_handlers.delete_sponsor(str(sponsor_mock.id))

    assert resp.status_code == 200
    sponsors_service_mock.delete.assert_awaited_once_with(str(sponsor_mock.id))


@pytest.mark.asyncio
async def test_get_sponsor_returns_404_when_missing(
    sponsors_handlers: SponsorsHandlers, sponsors_service_mock: SponsorsServiceMock
) -> None:
    sponsors_service_mock.get.return_value = Err(SponsorNotFoundError())

    resp = await sponsors_handlers.get_sponsor("missing sponsor")

    assert resp.status_code == 404
    sponsors_service_mock.get.assert_awaited_once_with("missing sponsor")
