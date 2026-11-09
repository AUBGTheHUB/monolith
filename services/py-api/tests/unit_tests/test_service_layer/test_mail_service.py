from typing import cast
from unittest.mock import patch

import pytest
from result import Err, Ok

from src.database.model.event.attendee_model import Attendee
from src.service.mail_service.mail_clients.base_mail_client import MailClient
from src.service.mail_service.mail_service import MailService
from tests.unit_tests.conftest import BackgroundTasksMock, MailClientMock

TEMPLATE_LOADER = "src.service.mail_service.mail_service.load_email_attendee_ticket_html_template"
UPDATE_TEMPLATE_LOADER = "src.service.mail_service.mail_service.load_email_updated_attendee_ticket_html_template"

PASS_DATA = "ZmFrZS1wYXNzLWJhc2U2NA=="
GOOGLE_URL = "https://pay.google.com/gp/v/save/fi3nofiwnf"
BODY = "<p>hi</p>"


@pytest.fixture
def mail_service(mail_client_mock: MailClientMock) -> MailService:
    return MailService(cast(MailClient, mail_client_mock))


@pytest.mark.asyncio
async def test_send_email_with_ticket_returns_ok(
    mail_service: MailService, attendee_mock: Attendee, background_tasks_mock: BackgroundTasksMock
) -> None:
    with patch(TEMPLATE_LOADER, return_value=BODY):
        result = await mail_service.send_email_with_ticket(attendee_mock, PASS_DATA, GOOGLE_URL, background_tasks_mock)

    assert isinstance(result, Ok)
    assert result.ok_value is None


@pytest.mark.asyncio
async def test_send_update_email_with_ticket_returns_ok(
    mail_service: MailService, attendee_mock: Attendee, background_tasks_mock: BackgroundTasksMock
) -> None:
    with patch(TEMPLATE_LOADER, return_value=BODY):
        result = await mail_service.send_update_email_with_ticket(attendee_mock, background_tasks_mock)

    assert isinstance(result, Ok)
    assert result.ok_value is None


@pytest.mark.asyncio
async def test_send_email_with_ticket_loads_template_with_attendee_name(
    mail_service: MailService, attendee_mock: Attendee, background_tasks_mock: BackgroundTasksMock
) -> None:
    with patch(TEMPLATE_LOADER, return_value=BODY) as loader:
        await mail_service.send_email_with_ticket(attendee_mock, PASS_DATA, GOOGLE_URL, background_tasks_mock)

    loader.assert_called_once_with(name=attendee_mock.name, google_url=GOOGLE_URL)


@pytest.mark.asyncio
async def test_send_email_with_ticket_queues_client_call_with_correct_arguments(
    mail_service: MailService,
    mail_client_mock: MailClientMock,
    attendee_mock: Attendee,
    background_tasks_mock: BackgroundTasksMock,
) -> None:
    with patch(TEMPLATE_LOADER, return_value=BODY):
        await mail_service.send_email_with_ticket(attendee_mock, PASS_DATA, GOOGLE_URL, background_tasks_mock)

    background_tasks_mock.add_task.assert_called_once_with(
        mail_client_mock.send_email_with_attachments,
        sender=MailService._SENDER_EMAIL,
        receiver=attendee_mock.email,
        subject="Welcome Aboard! See You at Play Con!",
        body_content=BODY,
        attachments=[
            {
                "filename": "Ticket.pkpass",
                "content": PASS_DATA,
                "content_type": "application/vnd.apple.pkpass",
            }
        ],
    )


@pytest.mark.asyncio
async def test_send_email_with_ticket_does_not_send_synchronously(
    mail_service: MailService,
    mail_client_mock: MailClientMock,
    attendee_mock: Attendee,
    background_tasks_mock: BackgroundTasksMock,
) -> None:
    with patch(TEMPLATE_LOADER, return_value=BODY):
        await mail_service.send_email_with_ticket(attendee_mock, PASS_DATA, GOOGLE_URL, background_tasks_mock)

    mail_client_mock.send_email_with_attachments.assert_not_awaited()


@pytest.mark.asyncio
async def test_send_email_with_ticket_passes_pass_data_through_undecoded(
    mail_service: MailService, attendee_mock: Attendee, background_tasks_mock: BackgroundTasksMock
) -> None:
    with patch(TEMPLATE_LOADER, return_value=BODY):
        await mail_service.send_email_with_ticket(attendee_mock, PASS_DATA, GOOGLE_URL, background_tasks_mock)

    attachment = background_tasks_mock.add_task.call_args.kwargs["attachments"][0]
    assert attachment["content"] is PASS_DATA


@pytest.mark.asyncio
async def test_send_email_with_ticket_queued_task_calls_client_when_run(
    mail_service: MailService,
    mail_client_mock: MailClientMock,
    attendee_mock: Attendee,
    background_tasks_mock: BackgroundTasksMock,
) -> None:
    with patch(TEMPLATE_LOADER, return_value=BODY):
        await mail_service.send_email_with_ticket(attendee_mock, PASS_DATA, GOOGLE_URL, background_tasks_mock)

    # The mock doesn't execute tasks, so run the queued one by hand
    queued = background_tasks_mock.add_task.call_args
    func, kwargs = queued.args[0], queued.kwargs
    await func(**kwargs)

    mail_client_mock.send_email_with_attachments.assert_awaited_once_with(**kwargs)


@pytest.mark.asyncio
async def test_send_email_with_ticket_returns_err_when_template_fails(
    mail_service: MailService, attendee_mock: Attendee, background_tasks_mock: BackgroundTasksMock
) -> None:
    error = ValueError("template not found")

    with patch(TEMPLATE_LOADER, side_effect=error):
        result = await mail_service.send_email_with_ticket(attendee_mock, PASS_DATA, GOOGLE_URL, background_tasks_mock)

    assert isinstance(result, Err)
    assert result.err_value is error


@pytest.mark.asyncio
async def test_send_email_with_ticket_queues_nothing_when_template_fails(
    mail_service: MailService,
    mail_client_mock: MailClientMock,
    attendee_mock: Attendee,
    background_tasks_mock: BackgroundTasksMock,
) -> None:
    with patch(TEMPLATE_LOADER, side_effect=ValueError("boom")):
        await mail_service.send_email_with_ticket(attendee_mock, PASS_DATA, GOOGLE_URL, background_tasks_mock)

    background_tasks_mock.add_task.assert_not_called()
    mail_client_mock.send_email_with_attachments.assert_not_awaited()
