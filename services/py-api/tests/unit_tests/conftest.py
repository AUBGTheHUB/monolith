from datetime import datetime, timedelta
from typing import Tuple, Optional

import pytest
from unittest.mock import Mock, MagicMock, AsyncMock

from motor.motor_asyncio import AsyncIOMotorClientSession
from result import Err

from src.database.db_manager import DatabaseManager
from src.database.model.participant_model import Participant
from src.database.model.team_model import Team
from src.database.repository.participants_repository import ParticipantsRepository
from src.database.repository.teams_repository import TeamsRepository
from src.database.transaction_manager import TransactionManager
from src.server.schemas.jwt_schemas.jwt_user_data_schema import JwtUserData
from src.server.schemas.request_schemas.schemas import (
    AdminParticipantInputData,
    InviteLinkParticipantInputData,
    RandomParticipantInputData,
    ParticipantRequestBody,
)
from src.service.hackathon_service import HackathonService
from src.service.participants_registration_service import ParticipantRegistrationService
from tests.integration_tests.test_jwt_utility import sufficient_expiration_time
from tests.integration_tests.conftest import TEST_USER_EMAIL, TEST_USER_NAME, TEST_TEAM_NAME


@pytest.fixture
def db_client_session_mock() -> MagicMock:
    mock_session = MagicMock(spec=AsyncIOMotorClientSession)

    mock_session.start_transaction = MagicMock()
    # We use AsyncMock, as the original AsyncIOMotorClient class has async methods
    mock_session.commit_transaction = AsyncMock()  # `commit_transaction` is async
    mock_session.abort_transaction = AsyncMock()  # `abort_transaction` is async
    mock_session.end_session = AsyncMock()  # `end_session` is async

    return mock_session


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

    return db_manager


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
    participant_repo.get_number_registered_teammates = AsyncMock()

    return participant_repo


@pytest.fixture
def team_repo_mock() -> Mock:
    """This is a mock obj of TeamsRepository. To change the return values of its methods use:
    `team_repo_mock.method_name.return_value=some_return_value`"""

    team_repo = Mock(spec=TeamsRepository)

    team_repo.fetch_by_id = AsyncMock()
    team_repo.fetch_by_team_name = AsyncMock()
    team_repo.fetch_all = AsyncMock()
    team_repo.update = AsyncMock()
    team_repo.create = AsyncMock()
    team_repo.delete = AsyncMock()

    return team_repo


@pytest.fixture
def hackathon_service_mock() -> Mock:
    """This is a mock obj of HackathonService. To change the return values of its methods use:
    `hackathon_service_mock.method_name.return_value=some_return_value`"""

    hackathon_service = Mock(spec=HackathonService)

    hackathon_service.create_participant_and_team_in_transaction = AsyncMock()
    hackathon_service.check_capacity_register_admin_participant_case = AsyncMock()
    hackathon_service.delete_participant = AsyncMock()
    hackathon_service.delete_team = AsyncMock()

    return hackathon_service


@pytest.fixture
def tx_manager_mock() -> Mock:
    """This is a mock obj of TransactionManager. To change the return values of its methods use:
    `tx_manager_mock.method_name.return_value=some_return_value`"""

    tx_manager = Mock(spec=TransactionManager)
    tx_manager.with_transaction = AsyncMock()

    return tx_manager


@pytest.fixture
def participant_registration_service_mock() -> Mock:
    """This is a mock obj of ParticipantRegistrationService. To change the return values of its methods use:
    `p_reg_service.method_name.return_value=some_return_value`"""

    p_reg_service = Mock(spec=ParticipantRegistrationService)
    p_reg_service.register_admin_participant.return_value = AsyncMock()

    return p_reg_service


@pytest.fixture
def mock_participant_request_body_admin_case(mock_normal_team: Team) -> ParticipantRequestBody:
    return ParticipantRequestBody(
        registration_info=AdminParticipantInputData(
            registration_type="admin",
            name=TEST_USER_NAME,
            email=TEST_USER_EMAIL,
            is_admin=True,
            team_name=mock_normal_team.name,
        )
    )


@pytest.fixture
def mock_participant_request_body_invite_link_case(mock_normal_team: Team) -> ParticipantRequestBody:
    return ParticipantRequestBody(
        registration_info=InviteLinkParticipantInputData(
            registration_type="invite_link",
            name=TEST_USER_NAME,
            email=TEST_USER_EMAIL,
            is_admin=False,
            team_name=mock_normal_team.name,
        )
    )


@pytest.fixture
def mock_participant_request_body_random_case(mock_normal_team: Team) -> ParticipantRequestBody:
    return ParticipantRequestBody(
        registration_info=RandomParticipantInputData(
            registration_type="random",
            name=TEST_USER_NAME,
            email=TEST_USER_EMAIL,
        )
    )


@pytest.fixture
def mock_admin_case_input_data(mock_normal_team: Team) -> AdminParticipantInputData:
    return AdminParticipantInputData(
        registration_type="admin",
        name=TEST_USER_NAME,
        email=TEST_USER_EMAIL,
        is_admin=True,
        team_name=mock_normal_team.name,
    )


@pytest.fixture
def mock_invite_link_case_input_data(mock_normal_team: Team) -> InviteLinkParticipantInputData:
    return InviteLinkParticipantInputData(
        registration_type="invite_link",
        name=TEST_USER_NAME,
        email=TEST_USER_EMAIL,
        is_admin=False,
        team_name=mock_normal_team.name,
    )


@pytest.fixture
def mock_random_case_input_data() -> RandomParticipantInputData:
    return RandomParticipantInputData(registration_type="random", name=TEST_USER_NAME, email=TEST_USER_EMAIL)


@pytest.fixture
def mock_normal_team() -> Team:
    return Team(name=TEST_TEAM_NAME)


@pytest.fixture
def mock_admin_participant(mock_normal_team: Team) -> Participant:
    return Participant(name=TEST_USER_NAME, email=TEST_USER_EMAIL, is_admin=True, team_id=mock_normal_team.id)


@pytest.fixture
def mock_invite_participant(mock_normal_team: Team) -> Participant:
    return Participant(
        name=TEST_USER_NAME, email=TEST_USER_EMAIL, is_admin=False, email_verified=True, team_id=mock_normal_team.id
    )


@pytest.fixture
def mock_random_participant() -> Participant:
    return Participant(name=TEST_USER_NAME, email=TEST_USER_EMAIL, is_admin=False, team_id=None)


@pytest.fixture
def mock_obj_id() -> str:
    return "507f1f77bcf86cd799439011"


@pytest.fixture
def mock_jwt_user_data(mock_obj_id: str) -> JwtUserData:
    return JwtUserData(
        sub=mock_obj_id,
        is_admin=False,
        team_name=TEST_TEAM_NAME,
        team_id=mock_obj_id,
        is_invite=True,
        exp=sufficient_expiration_time,
    )


@pytest.fixture
def ten_sec_window() -> Tuple[datetime, datetime]:
    now = datetime.now()
    return now - timedelta(seconds=10), now + timedelta(seconds=10)
