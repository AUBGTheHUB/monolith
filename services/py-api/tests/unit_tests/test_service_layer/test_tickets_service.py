from typing import cast
from unittest.mock import AsyncMock, MagicMock

import httpx
import pytest
from httpx import AsyncClient
from result import Err, Ok

from src.environment import WW_LIVE_KEY
from src.service.event.tickets_service import (
    WW_API_URL,
    WW_PASSES_URL,
    TicketsService,
    TicketField,
    DEFAULT_TICKET_FIELDS,
)

# adjust to your real module path

SERIAL = "serial-123"
PASS_DATA = "ZmFrZS1wYXNzLWJhc2U2NA=="
PASSES_URL = f"{WW_API_URL}{WW_PASSES_URL}"
AUTH_HEADERS = {"Content-Type": "application/json", "Authorization": f"Bearer {WW_LIVE_KEY}"}


def make_response(json_data: object = None) -> MagicMock:
    # httpx's Response.json() and raise_for_status() are sync, so this must be MagicMock, not AsyncMock
    response = MagicMock()
    response.json.return_value = json_data
    return response


def make_status_error_response() -> MagicMock:
    response = make_response()
    response.raise_for_status.side_effect = httpx.HTTPStatusError("boom", request=MagicMock(), response=response)
    return response


@pytest.fixture
def http_client_mock() -> MagicMock:
    client = MagicMock()
    client.post = AsyncMock(return_value=make_response({"applePass": PASS_DATA, "serialNumber": SERIAL}))
    client.put = AsyncMock(return_value=make_response())
    client.delete = AsyncMock(return_value=make_response())
    return client


@pytest.fixture
def tickets_service(http_client_mock: MagicMock) -> TicketsService:
    return TicketsService(cast(AsyncClient, http_client_mock))


# ---------- TicketField ----------


@pytest.mark.parametrize(
    ("field", "expected"),
    [
        (TicketField(label="L", value="V", changeMessage="C"), {"label": "L", "value": "V", "changeMessage": "C"}),
        (TicketField(label="L", value="V"), {"label": "L", "value": "V"}),
        (TicketField(value="V", changeMessage="C"), {"value": "V", "changeMessage": "C"}),
        (TicketField(value="V"), {"value": "V"}),
    ],
)
def test_ticket_field_get_as_json(field: TicketField, expected: dict[str, str]) -> None:
    assert field.get_as_json() == expected


# ---------- _format_fields ----------


def test_format_fields_maps_keys_to_labels(tickets_service: TicketsService) -> None:
    fields = tickets_service._format_fields({"Name": "Jane", None: "No label"})

    assert fields == [TicketField(label="Name", value="Jane"), TicketField(label=None, value="No label")]


def test_format_fields_empty_returns_empty_list(tickets_service: TicketsService) -> None:
    assert tickets_service._format_fields({}) == []


# ---------- create ----------


@pytest.mark.asyncio
async def test_create_returns_pass_data_and_serial(tickets_service: TicketsService) -> None:
    result = await tickets_service.create("VIP", "BARCODE-1", {"Name": "Jane"}, {"Seat": "A1"})

    assert isinstance(result, Ok)
    assert result.ok_value == (PASS_DATA, SERIAL)


@pytest.mark.asyncio
async def test_create_converts_serial_number_to_str(
    tickets_service: TicketsService, http_client_mock: MagicMock
) -> None:
    http_client_mock.post.return_value = make_response({"applePass": PASS_DATA, "serialNumber": 12345})

    result = await tickets_service.create("VIP", "BARCODE-1", {}, {})

    assert isinstance(result, Ok)
    assert result.ok_value == (PASS_DATA, "12345")


@pytest.mark.asyncio
async def test_create_posts_to_passes_endpoint_with_auth(
    tickets_service: TicketsService, http_client_mock: MagicMock
) -> None:
    await tickets_service.create("VIP", "BARCODE-1", {}, {})

    http_client_mock.post.assert_awaited_once()
    kwargs = http_client_mock.post.call_args.kwargs
    assert kwargs["url"] == PASSES_URL
    assert kwargs["headers"] == AUTH_HEADERS


@pytest.mark.asyncio
async def test_create_sends_defaults_and_formatted_fields(
    tickets_service: TicketsService, http_client_mock: MagicMock
) -> None:
    await tickets_service.create("VIP", "BARCODE-1", {"Name": "Jane"}, {"Seat": "A1", None: "Row 2"})

    payload = http_client_mock.post.call_args.kwargs["json"]
    assert payload == {
        **DEFAULT_TICKET_FIELDS,
        "barcodeValue": "BARCODE-1",
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
    tickets_service: TicketsService, http_client_mock: MagicMock
) -> None:
    http_client_mock.post.return_value = make_status_error_response()

    result = await tickets_service.create("VIP", "BARCODE-1", {}, {})

    assert isinstance(result, Err)
    assert isinstance(result.err_value, httpx.HTTPStatusError)


@pytest.mark.asyncio
async def test_create_returns_err_on_network_error(
    tickets_service: TicketsService, http_client_mock: MagicMock
) -> None:
    http_client_mock.post.side_effect = httpx.ConnectError("unreachable")

    result = await tickets_service.create("VIP", "BARCODE-1", {}, {})

    assert isinstance(result, Err)
    assert isinstance(result.err_value, httpx.ConnectError)


@pytest.mark.parametrize("body", [{"serialNumber": SERIAL}, {"applePass": PASS_DATA}])
@pytest.mark.asyncio
async def test_create_returns_err_when_response_is_missing_keys(
    tickets_service: TicketsService, http_client_mock: MagicMock, body: dict[str, str]
) -> None:
    http_client_mock.post.return_value = make_response(body)

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
    tickets_service: TicketsService, http_client_mock: MagicMock
) -> None:
    await tickets_service.update(SERIAL, None, None)

    http_client_mock.put.assert_awaited_once()
    kwargs = http_client_mock.put.call_args.kwargs
    assert kwargs["url"] == f"{PASSES_URL}/{SERIAL}"
    assert kwargs["headers"] == AUTH_HEADERS


@pytest.mark.asyncio
async def test_update_with_no_changes_sends_only_defaults(
    tickets_service: TicketsService, http_client_mock: MagicMock
) -> None:
    await tickets_service.update(SERIAL, None, None)

    assert http_client_mock.put.call_args.kwargs["json"] == DEFAULT_TICKET_FIELDS


@pytest.mark.asyncio
async def test_update_includes_only_provided_fields(
    tickets_service: TicketsService, http_client_mock: MagicMock
) -> None:
    await tickets_service.update(SERIAL, "VIP", "BARCODE-2", {"Name": "Jane"}, {"Seat": "A1"})

    assert http_client_mock.put.call_args.kwargs["json"] == {
        **DEFAULT_TICKET_FIELDS,
        "barcodeValue": "BARCODE-2",
        "headerFields": [{"label": "Ticket type", "value": "VIP"}],
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
    tickets_service: TicketsService, http_client_mock: MagicMock, kwargs: dict[str, None], expected_key: str
) -> None:
    all_optional = {"barcodeValue", "headerFields", "primaryFields", "secondaryFields"}
    params = {"ticket_type": None, "barcode_value": None, **kwargs}

    await tickets_service.update(SERIAL, **params)

    payload = http_client_mock.put.call_args.kwargs["json"]
    assert expected_key in payload
    assert all_optional - {expected_key} <= all_optional - set(payload)  # the others are absent


@pytest.mark.asyncio
async def test_update_empty_dict_is_sent_as_empty_list_not_skipped(
    tickets_service: TicketsService, http_client_mock: MagicMock
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
    tickets_service: TicketsService, http_client_mock: MagicMock
) -> None:
    http_client_mock.put.return_value = make_status_error_response()

    result = await tickets_service.update(SERIAL, None, None)

    assert isinstance(result, Err)
    assert isinstance(result.err_value, httpx.HTTPStatusError)


@pytest.mark.asyncio
async def test_update_returns_err_on_network_error(
    tickets_service: TicketsService, http_client_mock: MagicMock
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
    tickets_service: TicketsService, http_client_mock: MagicMock
) -> None:
    await tickets_service.delete(SERIAL)

    http_client_mock.delete.assert_awaited_once_with(
        url=f"{PASSES_URL}/{SERIAL}",
        headers={"Authorization": f"Bearer {WW_LIVE_KEY}"},
    )


@pytest.mark.asyncio
async def test_delete_returns_err_on_http_status_error(
    tickets_service: TicketsService, http_client_mock: MagicMock
) -> None:
    http_client_mock.delete.return_value = make_status_error_response()

    result = await tickets_service.delete(SERIAL)

    assert isinstance(result, Err)
    assert isinstance(result.err_value, httpx.HTTPStatusError)


@pytest.mark.asyncio
async def test_delete_returns_err_on_network_error(
    tickets_service: TicketsService, http_client_mock: MagicMock
) -> None:
    http_client_mock.delete.side_effect = httpx.ConnectError("unreachable")

    result = await tickets_service.delete(SERIAL)

    assert isinstance(result, Err)
    assert isinstance(result.err_value, httpx.ConnectError)
