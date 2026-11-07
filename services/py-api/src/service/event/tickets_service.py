from dataclasses import dataclass

from httpx import AsyncClient
from result import Err, Result, Ok
from structlog.stdlib import get_logger
from typing_extensions import Any

from src.environment import WW_LIVE_KEY

WW_API_URL = "https://api.walletwallet.dev/api"
WW_PASSES_URL = "/passes"
DEFAULT_TICKET_FIELDS = {
    "barcodeFormat": "QR",
    "barcodeAltText": "",
    "logoText": "The Hub",
    "description": "Play Con",
    "organizationName": "The Hub",
}

LOG = get_logger()


@dataclass(kw_only=True)
class TicketField:
    label: str | None = None
    value: str
    changeMessage: str | None = None

    def get_as_json(self) -> dict[str, str]:
        if self.label is not None:
            if self.changeMessage is not None:
                return {"label": self.label, "value": self.value, "changeMessage": self.changeMessage}

            return {"label": self.label, "value": self.value}

        if self.changeMessage is not None:
            return {"value": self.value, "changeMessage": self.changeMessage}

        return {"value": self.value}


class TicketsService:
    def __init__(self, http_client: AsyncClient):
        self._http_client = http_client

    def _format_fields(self, fields: dict[str | None, str]) -> list[TicketField]:
        return [TicketField(label=key, value=value) for (key, value) in fields.items()]

    async def create(
        self,
        ticket_type: str,
        barcode_value: str,
        primary_fields: dict[str | None, str],
        secondary_fields: dict[str | None, str],
    ) -> Result[tuple[str, str, str], Exception]:
        header_fields: list[TicketField] = [
            TicketField(label="Ticket Type", value=ticket_type),
        ]
        ticket: dict[str, Any] = {
            **DEFAULT_TICKET_FIELDS,
            "barcodeValue": barcode_value,
            "headerFields": [field.get_as_json() for field in header_fields],
            "primaryFields": [field.get_as_json() for field in self._format_fields(primary_fields)],
            "secondaryFields": [field.get_as_json() for field in self._format_fields(secondary_fields)],
        }

        try:
            response = await self._http_client.post(
                url=f"{WW_API_URL}{WW_PASSES_URL}",
                headers={"Content-Type": "application/json", "Authorization": f"Bearer {WW_LIVE_KEY}"},
                json=ticket,
            )
            response.raise_for_status()
            data = response.json()
            pass_data: str = data["applePass"]
            google_url: str = data["googleSaveUrl"]

            return Ok((pass_data, str(data["serialNumber"]), google_url))

        except Exception as e:
            LOG.error("There was an error when creating ticket", error=e)
            return Err(e)

    async def update(
        self,
        ticket_serial_number: str,
        ticket_type: str | None,
        barcode_value: str | None,
        primary_fields: dict[str | None, str] | None = None,
        secondary_fields: dict[str | None, str] | None = None,
    ) -> Result[None, Exception]:
        ticket: dict[str, Any] = {**DEFAULT_TICKET_FIELDS}

        if barcode_value is not None:
            ticket["barcodeValue"] = barcode_value

        if ticket_type is not None:
            header_fields: dict[str | None, str] = {
                "Ticket Type": ticket_type,
            }
            ticket["headerFields"] = [field.get_as_json() for field in self._format_fields(header_fields)]

        if primary_fields is not None:
            ticket["primaryFields"] = [field.get_as_json() for field in self._format_fields(primary_fields)]

        if secondary_fields is not None:
            ticket["secondaryFields"] = [field.get_as_json() for field in self._format_fields(secondary_fields)]

        try:
            response = await self._http_client.put(
                url=f"{WW_API_URL}{WW_PASSES_URL}/{ticket_serial_number}",
                headers={"Content-Type": "application/json", "Authorization": f"Bearer {WW_LIVE_KEY}"},
                json=ticket,
            )
            response.raise_for_status()

            return Ok(None)

        except Exception as e:
            LOG.error("There was an error when updating ticket", error=e)
            return Err(e)

    async def delete(self, ticket_serial_number: str) -> Result[None, Exception]:
        try:
            response = await self._http_client.delete(
                url=f"{WW_API_URL}{WW_PASSES_URL}/{ticket_serial_number}",
                headers={"Authorization": f"Bearer {WW_LIVE_KEY}"},
            )
            response.raise_for_status()

            return Ok(None)

        except Exception as e:
            LOG.error("There was an error when deleting ticket", error=e)
            return Err(e)
