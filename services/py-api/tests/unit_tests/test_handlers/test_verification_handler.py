import pytest
from fastapi.testclient import TestClient
from unittest.mock import AsyncMock
from jose import jwt
from fastapi import FastAPI
from src.server.handlers.verification_handler import router
from src.service.verification_service import VerificationService

SECRET_KEY = "your-secret-key"
ALGORITHM = "HS256"


@pytest.fixture
def mock_service() -> AsyncMock:
    service = AsyncMock(VerificationService)
    return service


@pytest.fixture
def test_client(mock_service: AsyncMock) -> TestClient:
    app = FastAPI()
    app.include_router(router, prefix="/hackathon")
    app.dependency_overrides[VerificationService] = lambda: mock_service
    return TestClient(app)


def test_verify_participant_success(test_client: TestClient, mock_service: AsyncMock) -> None:
    # Use your exact payload for the test
    payload = {"sub": "673b6acfb866606f24095456", "is_admin": False, "team_id": "", "exp": 1735641475.917655}
    jwt_token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

    # Mock service behavior
    mock_service.verify_random_participant.return_value = True

    # Make the request
    response = test_client.get(f"/hackathon/participants/verify?jwt_token={jwt_token}")

    # Verify response
    assert response.status_code == 200
    assert response.json() == {"message": "Verification successful, participant is now verified."}


def test_verify_participant_invalid_token(test_client: TestClient) -> None:
    # Provide an invalid JWT token
    invalid_jwt_token = "invalid.jwt.token"

    # Make the request
    response = test_client.get(f"/hackathon/participants/verify?jwt_token={invalid_jwt_token}")

    # Verify response
    assert response.status_code == 401
    assert response.json() == {"detail": "Invalid or expired token."}


def test_verify_participant_invalid_payload(test_client: TestClient, mock_service: AsyncMock) -> None:
    # Provide a JWT with invalid payload (e.g., missing is_admin field)
    invalid_payload = {"sub": "673b6acfb866606f24095456", "team_id": "", "exp": 1735641475.917655}
    jwt_token = jwt.encode(invalid_payload, SECRET_KEY, algorithm=ALGORITHM)

    # Make the request
    response = test_client.get(f"/hackathon/participants/verify?jwt_token={jwt_token}")

    # Verify response
    assert response.status_code == 400
    assert response.json() == {"detail": "Invalid token payload for this operation."}
