from typing import cast
from unittest.mock import MagicMock

import httpx
import pytest
from httpx import AsyncClient
from result import Err, Ok

from src.environment import WW_LIVE_KEY
from src.service.event.tickets_service import (
    WW_API_URL,
    WW_PASSES_URL,
    TicketsService,
    DEFAULT_TICKET_FIELDS,
)
from tests.unit_tests.conftest import HttpClientMock, HttpClientResponseMock

# adjust to your real module path

SERIAL = "serial-123"
PASS_DATA = "ZmFrZS1wYXNzLWJhc2U2NA=="
GOOGLE_URL = "https://pay.google.com/gp/v/save/fi3nofiwnf"
PASSES_URL = f"{WW_API_URL}{WW_PASSES_URL}"
AUTH_HEADERS = {"Content-Type": "application/json", "Authorization": f"Bearer {WW_LIVE_KEY}"}


@pytest.fixture
def tickets_service(http_client_mock: HttpClientMock) -> TicketsService:
    return TicketsService(cast(AsyncClient, http_client_mock))


# ---------- create ----------


@pytest.mark.asyncio
async def test_create_returns_pass_data_and_serial(
    tickets_service: TicketsService, http_client_mock: HttpClientMock, http_client_response_mock: HttpClientResponseMock
) -> None:
    http_client_response_mock.json.return_value = {
        "applePass": PASS_DATA,
        "serialNumber": SERIAL,
        "googleSaveUrl": GOOGLE_URL,
    }
    http_client_mock.post.return_value = http_client_response_mock
    result = await tickets_service.create("VIP", "BARCODE-1", {"Name": "Jane"}, {"Seat": "A1"})

    assert isinstance(result, Ok)
    assert result.ok_value == (PASS_DATA, SERIAL, GOOGLE_URL)


@pytest.mark.asyncio
async def test_create_converts_serial_number_to_str(
    tickets_service: TicketsService, http_client_mock: HttpClientMock, http_client_response_mock: HttpClientResponseMock
) -> None:
    http_client_response_mock.json.return_value = {
        "applePass": PASS_DATA,
        "serialNumber": 12345,
        "googleSaveUrl": GOOGLE_URL,
    }
    http_client_mock.post.return_value = http_client_response_mock

    result = await tickets_service.create("VIP", "BARCODE-1", {}, {})

    assert isinstance(result, Ok)
    assert result.ok_value == (PASS_DATA, "12345", GOOGLE_URL)


@pytest.mark.asyncio
async def test_create_posts_to_passes_endpoint_with_auth(
    tickets_service: TicketsService, http_client_mock: HttpClientMock
) -> None:
    await tickets_service.create("VIP", "BARCODE-1", {}, {})

    http_client_mock.post.assert_awaited_once()
    kwargs = http_client_mock.post.call_args.kwargs
    assert kwargs["url"] == PASSES_URL
    assert kwargs["headers"] == AUTH_HEADERS


@pytest.mark.asyncio
async def test_create_sends_defaults_and_formatted_fields(
    tickets_service: TicketsService, http_client_mock: HttpClientMock
) -> None:
    await tickets_service.create("VIP", "BARCODE-1", {"Name": "Jane"}, {"Seat": "A1", None: "Row 2"})

    payload = http_client_mock.post.call_args.kwargs["json"]
    assert payload == {
        **DEFAULT_TICKET_FIELDS,
        "barcodeValue": "https://thehub-aubg.com/tournament/verify/BARCODE-1",
        "headerFields": [{"label": "Ticket Type", "value": "VIP"}],
        "primaryFields": [{"label": "Name", "value": "Jane"}],
        "secondaryFields": [{"label": "Seat", "value": "A1"}, {"value": "Row 2"}],
    }


@pytest.mark.asyncio
async def test_create_does_not_mutate_default_ticket_fields(tickets_service: TicketsService) -> None:
    before = dict(DEFAULT_TICKET_FIELDS)

    await tickets_service.create("VIP", "BARCODE-1", {}, {})

    assert DEFAULT_TICKET_FIELDS == before


@pytest.mark.asyncio
async def test_create_returns_err_on_http_status_error(
    tickets_service: TicketsService, http_client_mock: HttpClientMock, http_client_response_mock: HttpClientResponseMock
) -> None:
    http_client_response_mock.raise_for_status.side_effect = httpx.HTTPStatusError(
        "Error", request=MagicMock(), response=http_client_response_mock
    )
    http_client_mock.post.return_value = http_client_response_mock

    result = await tickets_service.create("VIP", "BARCODE-1", {}, {})

    assert isinstance(result, Err)
    assert isinstance(result.err_value, httpx.HTTPStatusError)


@pytest.mark.asyncio
async def test_create_returns_err_on_network_error(
    tickets_service: TicketsService, http_client_mock: HttpClientMock
) -> None:
    http_client_mock.post.side_effect = httpx.ConnectError("unreachable")

    result = await tickets_service.create("VIP", "BARCODE-1", {}, {})

    assert isinstance(result, Err)
    assert isinstance(result.err_value, httpx.ConnectError)


@pytest.mark.asyncio
async def test_create_returns_err_when_response_is_missing_keys(
    tickets_service: TicketsService, http_client_mock: HttpClientMock, http_client_response_mock: HttpClientResponseMock
) -> None:
    http_client_response_mock.json.return_value = {"applePass": PASS_DATA, "googleSaveUrl": GOOGLE_URL}
    http_client_mock.post.return_value = http_client_response_mock

    result = await tickets_service.create("VIP", "BARCODE-1", {}, {})

    assert isinstance(result, Err)
    assert isinstance(result.err_value, KeyError)


# ---------- update ----------


@pytest.mark.asyncio
async def test_update_returns_ok_none(tickets_service: TicketsService) -> None:
    result = await tickets_service.update(SERIAL, None, None)

    assert isinstance(result, Ok)
    assert result.ok_value is None


@pytest.mark.asyncio
async def test_update_puts_to_serial_endpoint_with_auth(
    tickets_service: TicketsService, http_client_mock: HttpClientMock
) -> None:
    await tickets_service.update(SERIAL, None, None)

    http_client_mock.put.assert_awaited_once()
    kwargs = http_client_mock.put.call_args.kwargs
    assert kwargs["url"] == f"{PASSES_URL}/{SERIAL}"
    assert kwargs["headers"] == AUTH_HEADERS


@pytest.mark.asyncio
async def test_update_with_no_changes_sends_only_defaults(
    tickets_service: TicketsService, http_client_mock: HttpClientMock
) -> None:
    await tickets_service.update(SERIAL, None, None)

    assert http_client_mock.put.call_args.kwargs["json"] == DEFAULT_TICKET_FIELDS


@pytest.mark.asyncio
async def test_update_includes_only_provided_fields(
    tickets_service: TicketsService, http_client_mock: HttpClientMock
) -> None:
    await tickets_service.update(SERIAL, "VIP", "BARCODE-2", {"Name": "Jane"}, {"Seat": "A1"})

    assert http_client_mock.put.call_args.kwargs["json"] == {
        **DEFAULT_TICKET_FIELDS,
        "barcodeValue": "BARCODE-2",
        "headerFields": [{"label": "Ticket Type", "value": "VIP"}],
        "primaryFields": [{"label": "Name", "value": "Jane"}],
        "secondaryFields": [{"label": "Seat", "value": "A1"}],
    }


@pytest.mark.parametrize(
    ("kwargs", "expected_key"),
    [
        ({"barcode_value": "B"}, "barcodeValue"),
        ({"ticket_type": "VIP"}, "headerFields"),
        ({"primary_fields": {"Name": "Jane"}}, "primaryFields"),
        ({"secondary_fields": {"Seat": "A1"}}, "secondaryFields"),
    ],
)
@pytest.mark.asyncio
async def test_update_omits_unprovided_keys(
    tickets_service: TicketsService, http_client_mock: HttpClientMock, kwargs: dict[str, None], expected_key: str
) -> None:
    all_optional = {"barcodeValue", "headerFields", "primaryFields", "secondaryFields"}
    params = {"ticket_type": None, "barcode_value": None, **kwargs}

    await tickets_service.update(SERIAL, **params)

    payload = http_client_mock.put.call_args.kwargs["json"]
    assert expected_key in payload
    assert all_optional - {expected_key} <= all_optional - set(payload)


@pytest.mark.asyncio
async def test_update_empty_dict_is_sent_as_empty_list_not_skipped(
    tickets_service: TicketsService, http_client_mock: HttpClientMock
) -> None:
    await tickets_service.update(SERIAL, None, None, primary_fields={})

    assert http_client_mock.put.call_args.kwargs["json"]["primaryFields"] == []


@pytest.mark.asyncio
async def test_update_does_not_mutate_default_ticket_fields(tickets_service: TicketsService) -> None:
    before = dict(DEFAULT_TICKET_FIELDS)

    await tickets_service.update(SERIAL, "VIP", "BARCODE-2", {"Name": "Jane"}, {"Seat": "A1"})

    assert DEFAULT_TICKET_FIELDS == before


@pytest.mark.asyncio
async def test_update_returns_err_on_http_status_error(
    tickets_service: TicketsService, http_client_mock: HttpClientMock, http_client_response_mock: HttpClientResponseMock
) -> None:
    http_client_response_mock.raise_for_status.side_effect = httpx.HTTPStatusError(
        "Error", request=MagicMock(), response=http_client_response_mock
    )
    http_client_mock.put.return_value = http_client_response_mock

    result = await tickets_service.update(SERIAL, None, None)

    assert isinstance(result, Err)
    assert isinstance(result.err_value, httpx.HTTPStatusError)


@pytest.mark.asyncio
async def test_update_returns_err_on_network_error(
    tickets_service: TicketsService, http_client_mock: HttpClientMock
) -> None:
    http_client_mock.put.side_effect = httpx.ReadTimeout("slow")

    result = await tickets_service.update(SERIAL, None, None)

    assert isinstance(result, Err)
    assert isinstance(result.err_value, httpx.ReadTimeout)


# ---------- delete ----------


@pytest.mark.asyncio
async def test_delete_returns_ok_none(tickets_service: TicketsService) -> None:
    result = await tickets_service.delete(SERIAL)

    assert isinstance(result, Ok)
    assert result.ok_value is None


@pytest.mark.asyncio
async def test_delete_calls_serial_endpoint_with_auth_only(
    tickets_service: TicketsService, http_client_mock: HttpClientMock
) -> None:
    await tickets_service.delete(SERIAL)

    http_client_mock.delete.assert_awaited_once_with(
        url=f"{PASSES_URL}/{SERIAL}",
        headers={"Authorization": f"Bearer {WW_LIVE_KEY}"},
    )


@pytest.mark.asyncio
async def test_delete_returns_err_on_http_status_error(
    tickets_service: TicketsService, http_client_mock: HttpClientMock, http_client_response_mock: HttpClientResponseMock
) -> None:
    http_client_response_mock.raise_for_status.side_effect = httpx.HTTPStatusError(
        "Error", request=MagicMock(), response=http_client_response_mock
    )
    http_client_mock.delete.return_value = http_client_response_mock

    result = await tickets_service.delete(SERIAL)

    assert isinstance(result, Err)
    assert isinstance(result.err_value, httpx.HTTPStatusError)


@pytest.mark.asyncio
async def test_delete_returns_err_on_network_error(
    tickets_service: TicketsService, http_client_mock: HttpClientMock
) -> None:
    http_client_mock.delete.side_effect = httpx.ConnectError("unreachable")

    result = await tickets_service.delete(SERIAL)

    assert isinstance(result, Err)
    assert isinstance(result.err_value, httpx.ConnectError)
