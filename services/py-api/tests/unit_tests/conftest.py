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
from src.service.hackathon_service import HackathonService
from src.service.participants_registration_service import ParticipantRegistrationService


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
    """This is a mock obj of ParticipantsRepository. To change the return values of its methods use:
    `participant_repo_mock.method_name.return_value=some_return_value`"""

    participant_repo = Mock(spec=ParticipantsRepository)

    participant_repo.fetch_by_id = AsyncMock()
    participant_repo.fetch_all = AsyncMock()
    participant_repo.update = AsyncMock()
    participant_repo.create = AsyncMock()
    participant_repo.delete = AsyncMock()

    yield participant_repo

    participant_repo.reset_mock()


@pytest.fixture
def team_repo_mock() -> Mock:
    """This is a mock obj of TeamsRepository. To change the return values of its methods use:
    `team_repo_mock.method_name.return_value=some_return_value`"""

    team_repo = Mock(spec=TeamsRepository)

    team_repo.fetch_by_id = AsyncMock()
    team_repo.fetch_all = AsyncMock()
    team_repo.update = AsyncMock()
    team_repo.create = AsyncMock()
    team_repo.delete = AsyncMock()

    yield team_repo

    team_repo.reset_mock()


@pytest.fixture
def hackathon_service_mock() -> Mock:
    """This is a mock obj of HackathonService. To change the return values of its methods use:
    `hackathon_service_mock.method_name.return_value=some_return_value`"""

    hackathon_service = Mock(spec=HackathonService)

    hackathon_service.create_participant_and_team_in_transaction = AsyncMock()
    hackathon_service.check_capacity_register_admin_participant_case = AsyncMock()

    yield hackathon_service

    hackathon_service.reset_mock()


@pytest.fixture
def tx_manager_mock() -> Mock:
    """This is a mock obj of TransactionManager. To change the return values of its methods use:
    `tx_manager_mock.method_name.return_value=some_return_value`"""

    tx_manager = Mock(spec=TransactionManager)
    tx_manager.with_transaction = AsyncMock()

    yield tx_manager

    tx_manager.reset_mock()


@pytest.fixture
def participant_registration_service_mock() -> Mock:
    """This is a mock obj of ParticipantRegistrationService. To change the return values of its methods use:
    `p_reg_service.method_name.return_value=some_return_value`"""

    p_reg_service = Mock(spec=ParticipantRegistrationService)
    p_reg_service.register_admin_participant.return_value = AsyncMock()

    yield p_reg_service

    p_reg_service.reset_mock()


@pytest.fixture
def mock_input_data() -> ParticipantRequestBody:
    return ParticipantRequestBody(name="Test User", email="test@example.com", team_name="Test Team", is_admin=True)


@pytest.fixture
def response_mock() -> MagicMock:
    resp = MagicMock(spec=Response)

    yield resp

    resp.reset_mock()


@pytest.fixture
def ten_sec_window() -> Tuple[datetime, datetime]:
    now = datetime.now()
    return now - timedelta(seconds=10), now + timedelta(seconds=10)
