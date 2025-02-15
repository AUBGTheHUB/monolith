from datetime import datetime, timedelta, timezone
from typing import Tuple, cast
from unittest.mock import Mock, MagicMock, AsyncMock

import pytest
from fastapi import BackgroundTasks
from motor.motor_asyncio import AsyncIOMotorClientSession, AsyncIOMotorClient
from typing_extensions import Protocol

from src.database.db_managers import MongoDatabaseManager
from src.database.model.participant_model import Participant
from src.database.model.team_model import Team
from src.database.repository.participants_repository import ParticipantsRepository
from src.database.repository.teams_repository import TeamsRepository
from src.database.transaction_managers import MongoTransactionManager
from src.server.schemas.jwt_schemas.schemas import JwtParticipantInviteRegistrationData, JwtParticipantVerificationData
from src.server.schemas.request_schemas.schemas import (
    AdminParticipantInputData,
    InviteLinkParticipantInputData,
    RandomParticipantInputData,
    ParticipantRequestBody,
)
from src.service.hackathon_service import HackathonService
from src.service.mail_service.hackathon_mail_service import HackathonMailService
from src.service.participants_registration_service import ParticipantRegistrationService
from src.service.participants_verification_service import ParticipantVerificationService
from tests.integration_tests.conftest import TEST_USER_EMAIL, TEST_USER_NAME, TEST_TEAM_NAME


def _create_typed_mock[T](class_type: T) -> T:
    """
    Helper function to create a type annotated MagicMock with a spec modeling the provided class_type.
    Args:
        class_type: the class to mock (type should be provided, not an instance)
    Returns:
        A MagickMock speced to the provided class. This MagickMock is cast to the actual class, for type checkers.
         During runtime the type is actually MagickMock, cast is used only for type checkers.
    """

    return cast(T, MagicMock(spec=class_type))


def _create_typed_async_mock[T](class_type: T) -> T:
    """
    Helper function to create a type annotated AsyncMock with a spec modeling the provided class_type.
    Args:
        class_type: the class to mock (type should be provided, not an instance)
    Returns:
        A AsyncMock speced to the provided class. This AsyncMock is cast to the actual class, for type checkers.
         During runtime the type is actually AsyncMock, cast is used only for type checkers.
    """

    return cast(T, AsyncMock(spec=class_type))


# ======================================
# Mocking Motor library classes start
# ======================================


class MotorDbClientMock(Protocol):
    """A Static Duck Type, modeling a Mocked AsyncIOMotorClient"""

    start_session: AsyncMock  # `start_session` is async
    # Add more methods if needed


@pytest.fixture
def db_client_mock() -> MotorDbClientMock:
    mock_client = _create_typed_mock(AsyncIOMotorClient)
    mock_client.start_session = AsyncMock()  # `start_session` is async
    # Add more methods if needed
    return cast(MotorDbClientMock, mock_client)


class MotorDbClientSessionMock(Protocol):
    """A Static Duck Type, modeling a Mocked AsyncIOMotorClientSession"""

    start_transaction: MagicMock  # `start_transaction` is not async
    commit_transaction: AsyncMock  # `commit_transaction` is async
    abort_transaction: AsyncMock  # `abort_transaction` is async
    end_session: AsyncMock  # `end_session` is async


@pytest.fixture
def db_client_session_mock() -> MotorDbClientSessionMock:
    mock_session = _create_typed_mock(AsyncIOMotorClientSession)

    mock_session.start_transaction = MagicMock()  # `start_transaction` is not async
    mock_session.commit_transaction = AsyncMock()  # `commit_transaction` is async
    mock_session.abort_transaction = AsyncMock()  # `abort_transaction` is async
    mock_session.end_session = AsyncMock()  # `end_session` is async

    return cast(MotorDbClientSessionMock, mock_session)


# ======================================
# Mocking Motor library classes end
# ======================================


# ======================================
# Mocking Repository layer classes end
# ======================================


@pytest.fixture
def db_manager_mock(db_client_session_mock: MotorDbClientSessionMock, db_client_mock: MotorDbClientMock) -> Mock:
    db_manager = _create_typed_mock(MongoDatabaseManager)
    # We use AsyncMock, as the original AsyncIOMotorClient class has async methods
    db_manager._client = db_client_mock
    db_manager.get_collection = Mock()
    db_manager.async_ping_db = AsyncMock()
    db_manager.close_all_connections = Mock()

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
    participant_repo.get_verified_random_participants_count = AsyncMock()

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
    team_repo.get_verified_registered_teams_count = AsyncMock()

    return team_repo


class HackathonServiceMock(Protocol):
    create_participant_and_team_in_transaction: AsyncMock
    check_capacity_register_admin_participant_case: AsyncMock
    check_capacity_register_random_participant_case: AsyncMock
    check_send_verification_email_rate_limit: AsyncMock
    create_random_participant: AsyncMock
    create_invite_link_participant: AsyncMock
    check_team_capacity: AsyncMock
    verify_random_participant: AsyncMock
    verify_admin_participant_and_team_in_transaction: AsyncMock
    delete_participant: AsyncMock
    delete_team: AsyncMock
    verify_admin_participant: AsyncMock
    send_verification_email: AsyncMock
    send_successful_registration_email: Mock


@pytest.fixture
def hackathon_service_mock() -> HackathonServiceMock:
    """This is a mock obj of HackathonService. To change the return values of its methods use:
    `hackathon_service_mock.method_name.return_value=some_return_value`"""

    hackathon_service = create_typed_mock(HackathonService)
    hackathon_service.create_participant_and_team_in_transaction = AsyncMock()
    hackathon_service.check_capacity_register_admin_participant_case = AsyncMock()
    hackathon_service.check_capacity_register_random_participant_case = AsyncMock()
    hackathon_service.check_send_verification_email_rate_limit = AsyncMock()
    hackathon_service.create_random_participant = AsyncMock()
    hackathon_service.create_invite_link_participant = AsyncMock()
    hackathon_service.check_team_capacity = AsyncMock()
    hackathon_service.verify_random_participant = AsyncMock()
    hackathon_service.verify_admin_participant_and_team_in_transaction = AsyncMock()
    hackathon_service.delete_participant = AsyncMock()
    hackathon_service.delete_team = AsyncMock()
    hackathon_service.verify_admin_participant = AsyncMock()
    hackathon_service.send_verification_email = AsyncMock()
    hackathon_service.send_successful_registration_email = Mock()

    return cast(HackathonServiceMock, hackathon_service)


test = hackathon_service_mock()


@pytest.fixture
def hackathon_mail_service_mock() -> Mock:
    """This is a mock obj of HackathonMailService. To change the return values of its methods use:
    `hackathon_mail_service_mock.method_name.return_value=some_return_value`"""

    mailing_service_mock = Mock(spec=HackathonMailService)
    mailing_service_mock.send_participant_verification_email = Mock()
    mailing_service_mock.send_participant_successful_registration_email = Mock()

    return mailing_service_mock


@pytest.fixture
def tx_manager_mock() -> Mock:
    """This is a mock obj of TransactionManager. To change the return values of its methods use:
    `tx_manager_mock.method_name.return_value=some_return_value`"""

    tx_manager = Mock(spec=MongoTransactionManager)
    tx_manager.with_transaction = AsyncMock()

    return tx_manager


@pytest.fixture
def background_tasks() -> MagicMock:
    mock_background_tasks = MagicMock(spec=BackgroundTasks)
    mock_background_tasks.add_task = MagicMock()
    return mock_background_tasks


@pytest.fixture
def participant_registration_service_mock() -> Mock:
    """This is a mock obj of ParticipantRegistrationService. To change the return values of its methods use:
    `p_reg_service.method_name.return_value=some_return_value`"""

    p_reg_service = Mock(spec=ParticipantRegistrationService)
    p_reg_service.register_admin_participant = AsyncMock()
    p_reg_service.register_random_participant = AsyncMock()
    p_reg_service.register_admin_participant = AsyncMock()

    return p_reg_service


@pytest.fixture
def participant_verification_service_mock() -> Mock:
    """This is a mock obj of ParticipantVerificationService."""
    p_verify_service = Mock(spec=ParticipantVerificationService)
    p_verify_service.verify_random_participant = AsyncMock()

    return p_verify_service


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
def mock_jwt_user_registration(
    mock_obj_id: str, thirty_sec_jwt_exp_limit: float
) -> JwtParticipantInviteRegistrationData:
    return JwtParticipantInviteRegistrationData(
        sub=mock_obj_id,
        team_id=mock_obj_id,
        exp=thirty_sec_jwt_exp_limit,
    )


@pytest.fixture
def mock_jwt_random_user_verification(
    mock_obj_id: str, thirty_sec_jwt_exp_limit: float
) -> JwtParticipantVerificationData:
    return JwtParticipantVerificationData(
        sub=mock_obj_id,
        is_admin=False,
        exp=thirty_sec_jwt_exp_limit,
    )


@pytest.fixture
def mock_jwt_admin_user_verification(
    mock_obj_id: str, thirty_sec_jwt_exp_limit: float
) -> JwtParticipantVerificationData:
    return JwtParticipantVerificationData(
        sub=mock_obj_id,
        is_admin=True,
        exp=thirty_sec_jwt_exp_limit,
    )


@pytest.fixture
def ten_sec_window() -> Tuple[datetime, datetime]:
    now = datetime.now()
    return now - timedelta(seconds=10), now + timedelta(seconds=10)


@pytest.fixture
def thirty_sec_jwt_exp_limit() -> float:
    return (datetime.now(tz=timezone.utc) + timedelta(seconds=30)).timestamp()
