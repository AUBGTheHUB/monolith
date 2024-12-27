import pytest
from unittest.mock import AsyncMock
from fastapi import HTTPException
from src.service.verification_service import VerificationService


@pytest.mark.asyncio
async def test_verify_random_participant_success() -> None:
    # Mock HackathonService
    hackathon_service_mock = AsyncMock()
    hackathon_service_mock.check_capacity_register_random_participant_case.return_value = True

    service = VerificationService(hackathon_service_mock)

    # Call the service
    await service.verify_random_participant("test_id", "")

    # Verify the capacity check was called
    hackathon_service_mock.check_capacity_register_random_participant_case.assert_awaited_once()


@pytest.mark.asyncio
async def test_verify_random_participant_capacity_full() -> None:
    # Mock HackathonService
    hackathon_service_mock = AsyncMock()
    hackathon_service_mock.check_capacity_register_random_participant_case.return_value = False

    service = VerificationService(hackathon_service_mock)

    # Call the service and expect an exception
    with pytest.raises(HTTPException) as excinfo:
        await service.verify_random_participant("test_id", "")

    assert excinfo.value.status_code == 409
    assert excinfo.value.detail == "The hackathon capacity is full."
