from datetime import datetime, timedelta
from typing import Tuple, Optional

import pytest
from unittest.mock import Mock, MagicMock, AsyncMock

from motor.motor_asyncio import AsyncIOMotorClientSession
from result import Err
from starlette.responses import Response

from src.database.db_manager import DatabaseManager
from src.database.repository.participants_repository import ParticipantsRepository
from src.database.repository.teams_repository import TeamsRepository
from src.database.transaction_manager import TransactionManager
from src.server.schemas.request_schemas.schemas import ParticipantRequestBody


@pytest.fixture
def db_client_session_mock() -> MagicMock:
    mock_session = MagicMock(spec=AsyncIOMotorClientSession)
    # We use AsyncMock, as the original AsyncIOMotorClient class has async methods
    mock_session.start_transaction = MagicMock()
    mock_session.commit_transaction = AsyncMock()  # `commit_transaction` is async
    mock_session.abort_transaction = AsyncMock()  # `abort_transaction` is async
    mock_session.end_session = AsyncMock()  # `end_session` is async
    # https://docs.pytest.org/en/stable/how-to/fixtures.html#yield-fixtures-recommended
    yield mock_session

    mock_session.reset_mock()


@pytest.fixture
def db_manager_mock(db_client_session_mock: Mock) -> Mock:
    db_manager = Mock(spec=DatabaseManager)
    # We use AsyncMock, as the original AsyncIOMotorClient class has async methods
    db_manager.client = AsyncMock()
    db_manager.get_collection.return_value = AsyncMock()
    db_manager.client.start_session.return_value = db_client_session_mock
    db_manager.async_ping_db = AsyncMock(return_value=None)

    # Handle close_all_connections with a conditional side effect for uninitialized client
    def close_side_effect() -> Optional[Err[str]]:
        if db_manager.client:
            return None
        else:
            return Err("The database client is not initialized!")

    db_manager.close_all_connections.side_effect = close_side_effect

    yield db_manager

    db_manager.reset_mock()


@pytest.fixture
def participant_repo_mock() -> Mock:
    participant_repo = Mock(spec=ParticipantsRepository)

    participant_repo.fetch_by_id = AsyncMock()
    participant_repo.fetch_all = AsyncMock()
    participant_repo.update = AsyncMock()
    participant_repo.create = AsyncMock()
    participant_repo.delete = AsyncMock()

    return participant_repo


@pytest.fixture
def team_repo_mock() -> Mock:
    team_repo = Mock(spec=TeamsRepository)

    team_repo.fetch_by_id = AsyncMock()
    team_repo.fetch_all = AsyncMock()
    team_repo.update = AsyncMock()
    team_repo.create = AsyncMock()
    team_repo.delete = AsyncMock()

    return team_repo


@pytest.fixture
def tx_manager_mock() -> Mock:
    tx_manager = Mock(spec=TransactionManager)
    tx_manager.with_transaction = AsyncMock()

    yield tx_manager

    tx_manager.reset_mock()


@pytest.fixture
def mock_input_data() -> ParticipantRequestBody:
    return ParticipantRequestBody(name="Test User", email="test@example.com", team_name="Test Team", is_admin=True)


@pytest.fixture
def response_mock() -> MagicMock:
    return MagicMock(spec=Response)


@pytest.fixture
def ten_sec_window() -> Tuple[datetime, datetime]:
    now = datetime.now()
    return now - timedelta(seconds=10), now + timedelta(seconds=10)
