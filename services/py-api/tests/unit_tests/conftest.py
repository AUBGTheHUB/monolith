# mypy: disable_error_code=method-assign
# This is because we have TypedMocks which mypy thinks are the actual classes

from datetime import datetime, timedelta, timezone
from typing import Tuple, cast
from unittest.mock import Mock, MagicMock, AsyncMock

import pytest
from fastapi import BackgroundTasks
from motor.motor_asyncio import (
    AsyncIOMotorClientSession,
    AsyncIOMotorClient,
    AsyncIOMotorDatabase,
    AsyncIOMotorCollection,
)
from src.database.model.hackathon.participant_model import Participant
from src.database.model.hackathon.team_model import Team
from src.database.mongo.db_manager import MongoDatabaseManager
from src.database.repository.hackathon.participants_repository import ParticipantsRepository
from src.service.hackathon.hackathon_service import HackathonService
from src.service.hackathon.participants_registration_service import ParticipantRegistrationService
from src.service.hackathon.participants_verification_service import ParticipantVerificationService
from src.service.jwt_utils.schemas import JwtParticipantInviteRegistrationData, JwtParticipantVerificationData
from typing_extensions import Protocol

from src.server.schemas.request_schemas.schemas import (
    AdminParticipantInputData,
    InviteLinkParticipantInputData,
    RandomParticipantInputData,
    ParticipantRequestBody,
)

from tests.integration_tests.conftest import TEST_USER_EMAIL, TEST_USER_NAME, TEST_TEAM_NAME


def _create_typed_mock[T](class_type: T) -> T:
    """
    Helper function to create a type annotated MagicMock with a spec modeling the provided class_type.

    Args:
        class_type: the class to mock (type should be provided, not an instance)

    Returns:
        A MagickMock speced to the provided class. This MagickMock is cast to the actual class, for autocompletion of
         its methods when mocking them. During runtime the type is actually MagickMock, cast is used only for type
         checkers.
    """

    return cast(T, MagicMock(spec=class_type))


def _create_typed_async_mock[T](class_type: T) -> T:
    """
    Helper function to create a type annotated AsyncMock with a spec modeling the provided class_type.

    Args:
        class_type: the class to mock (type should be provided, not an instance)

    Returns:
       A AsyncMock speced to the provided class. This AsyncMock is cast to the actual class, for autocompletion of
        its methods when mocking them. During runtime the type is actually AsyncMock, cast is used only for type
        checkers.
    """

    return cast(T, AsyncMock(spec=class_type))


# ===============================
# Mocking FastAPI objects start
# ===============================


class BackgroundTasksMock(Protocol):
    """A Static Duck Type, modeling fastapi.BackgroundTasks

    Should not be initialized directly by application developers to create a BackgroundTasksMock instance. It is
    used just for type hinting purposes.
    """

    add_task: Mock


@pytest.fixture
def background_tasks_mock() -> BackgroundTasksMock:
    mock_background_tasks = _create_typed_mock(BackgroundTasks)
    mock_background_tasks.add_task = Mock()

    return cast(BackgroundTasksMock, mock_background_tasks)


# ===============================
# Mocking FastAPI objects end
# ===============================

# ======================================
# Mocking Motor library classes start
# ======================================


class MotorCollectionMock(Protocol):
    """A Static Duck Type, modeling a Mocked AsyncIOMotorCollection

    Should not be initialized directly by application developers to create a MotorCollectionMock instance. It is
    used just for type hinting purposes.
    """

    insert_one: AsyncMock
    find_one_and_update: AsyncMock
    find_one_and_delete: AsyncMock
    find_one: AsyncMock
    count_documents: AsyncMock
    # Add more methods if needed


@pytest.fixture
def motor_collection_mock() -> MotorCollectionMock:
    """Mock object for AsyncIOMotorCollection.

    For mocking purposes, you can modify the return values of its methods::

        motor_collection_mock.method_name.return_value = some_value

    To simulate raising exceptions, set the side effects::

        motor_collection_mock.method_name.side_effect = SomeException()

    Returns:
        A mocked AsyncIOMotorCollection
    """

    mock_collection = _create_typed_mock(AsyncIOMotorCollection)

    mock_collection.insert_one = AsyncMock()
    mock_collection.find_one_and_update = AsyncMock()
    mock_collection.find_one_and_delete = AsyncMock()
    mock_collection.find_one = AsyncMock()
    mock_collection.count_documents = AsyncMock()

    return cast(MotorCollectionMock, mock_collection)


class MotorDatabaseMock(Protocol):
    """A Static Duck Type, modeling a Mocked AsyncIOMotorClient

    Should not be initialized directly by application developers to create a MotorDatabaseMock instance. It is
    used just for type hinting purposes.
    """

    command: AsyncMock
    get_collection: MotorCollectionMock
    # Add more methods if needed


@pytest.fixture
def motor_database_mock(motor_collection_mock: MotorCollectionMock) -> MotorDatabaseMock:
    """Mock object for AsyncIOMotorClient.

    For mocking purposes, you can modify the return values of its methods::

        motor_db_client_mock.method_name.return_value = some_value

    To simulate raising exceptions, set the side effects::

        motor_db_client_mock.method_name.side_effect = SomeException()

    Returns:
        A mocked AsyncIOMotorDatabase
    """
    mock_db = _create_typed_mock(AsyncIOMotorDatabase)

    mock_db.command = AsyncMock()
    # make get_collection return a motor_database_mock
    mock_db.get_collection = Mock(return_value=motor_database_mock)
    # Add more methods if needed

    return cast(MotorDatabaseMock, mock_db)


class MotorDbClientSessionMock(Protocol):
    """A Static Duck Type, modeling a Mocked AsyncIOMotorClientSession

    Should not be initialized directly by application developers to create a MotorDbClientSessionMock instance. It is
    used just for type hinting purposes.
    """

    start_transaction: MagicMock
    commit_transaction: AsyncMock
    abort_transaction: AsyncMock
    end_session: AsyncMock


@pytest.fixture
def motor_db_session_mock() -> MotorDbClientSessionMock:
    """Mock object for AsyncIOMotorClientSession.

    For mocking purposes, you can modify the return values of its methods::

        motor_db_session_mock.method_name.return_value = some_value

    To simulate raising exceptions, set the side effects::

        motor_db_session_mock.method_name.side_effect = SomeException()

    Returns:
        A mocked AsyncIOMotorClientSession
    """

    mock_session = _create_typed_mock(AsyncIOMotorClientSession)

    mock_session.start_transaction = MagicMock()
    mock_session.commit_transaction = AsyncMock()
    mock_session.abort_transaction = AsyncMock()
    mock_session.end_session = AsyncMock()

    return cast(MotorDbClientSessionMock, mock_session)


class MotorDbClientMock(Protocol):
    """A Static Duck Type, modeling a Mocked AsyncIOMotorClient

    Should not be initialized directly by application developers to create a MotorDbClientMock instance. It is
    used just for type hinting purposes.
    """

    start_session: AsyncMock
    get_database: MotorDatabaseMock
    # Add more methods if needed


@pytest.fixture
def motor_db_client_mock(
    motor_database_mock: MotorDatabaseMock, motor_db_session_mock: MotorDbClientSessionMock
) -> MotorDbClientMock:
    """Mock object for AsyncIOMotorClient.

    For mocking purposes, you can modify the return values of its methods::

        motor_db_client_mock.method_name.return_value = some_value

    To simulate raising exceptions, set the side effects::

        motor_db_client_mock.method_name.side_effect = SomeException()

    Returns:
        A mocked AsyncIOMotorClient
    """
    mock_client = _create_typed_mock(AsyncIOMotorClient)

    mock_client.start_session = AsyncMock(return_value=motor_db_session_mock)
    # make get_database return a motor_database_mock
    mock_client.get_database = Mock(return_value=motor_database_mock)
    # Add more methods if needed

    return cast(MotorDbClientMock, mock_client)


# ======================================
# Mocking Motor library classes end
# ======================================


# ======================================
# Mocking Repository layer classes start
# ======================================


class MongoDbManagerMock(Protocol):
    """A Static Duck Type, modeling a Mocked MongoDatabaseManager

    Should not be initialized directly by application developers to create a MongoDbManagerMock instance. It is
    used just for type hinting purposes.
    """

    get_collection: Mock
    async_ping_db: AsyncMock
    close_all_connections: Mock


@pytest.fixture
def mongo_db_manager_mock(motor_collection_mock: MotorCollectionMock) -> MongoDbManagerMock:
    """Mock object for MongoDatabaseManager.

    For mocking purposes, you can modify the return values of its methods::

        mongo_db_manager_mock.method_name.return_value = some_value

    To simulate raising exceptions, set the side effects::

        mongo_db_manager_mock.method_name.side_effect = SomeException()

    Returns:
        A mocked MongoDatabaseManager
    """

    mock_db_manager = _create_typed_mock(MongoDatabaseManager)
    mock_db_manager.get_collection = Mock()
    mock_db_manager.async_ping_db = AsyncMock()

    mock_db_manager.async_ping_db = AsyncMock()
    # make get_collection return a motor_collection_mock
    mock_db_manager.get_collection = Mock(return_value=motor_collection_mock)
    mock_db_manager.close_all_connections = Mock()

    return cast(MongoDbManagerMock, mock_db_manager)


class ParticipantRepoMock(Protocol):
    """A Static Duck Type, modeling a Mocked ParticipantsRepository

    Should not be initialized directly by application developers to create a ParticipantRepoMock instance. It is
    used just for type hinting purposes.
    """

    fetch_by_id: AsyncMock
    fetch_all: AsyncMock
    update: AsyncMock
    bulk_update: AsyncMock
    create: AsyncMock
    delete: AsyncMock
    get_number_registered_teammates: AsyncMock
    get_verified_random_participants: AsyncMock
    get_verified_random_participants_count: AsyncMock


@pytest.fixture
def participant_repo_mock() -> ParticipantRepoMock:
    """Mock object for ParticipantsRepository.

    For mocking purposes, you can modify the return values of its methods::

        participant_repo_mock.method_name.return_value = some_value

    To simulate raising exceptions, set the side effects::

        participant_repo_mock.method_name.side_effect = SomeException()

    Returns:
        A mocked ParticipantsRepository
    """

    participant_repo = _create_typed_mock(ParticipantsRepository)

    participant_repo.fetch_by_id = AsyncMock()
    participant_repo.fetch_all = AsyncMock()
    participant_repo.update = AsyncMock()
    participant_repo.bulk_update = AsyncMock()
    participant_repo.create = AsyncMock()
    participant_repo.delete = AsyncMock()
    participant_repo.get_number_registered_teammates = AsyncMock()
    participant_repo.get_verified_random_participants_count = AsyncMock()
    participant_repo.get_verified_random_participants = AsyncMock()
    return cast(ParticipantRepoMock, participant_repo)


class TeamRepoMock(Protocol):
    """A Static Duck Type, modeling a Mocked TeamsRepository

    Should not be initialized directly by application developers to create a TeamRepoMock instance. It is
    used just for type hinting purposes.
    """

    fetch_by_id: AsyncMock
    fetch_by_team_name: AsyncMock
    fetch_all: AsyncMock
    update: AsyncMock
    create: AsyncMock
    delete: AsyncMock
    get_verified_registered_teams_count: AsyncMock


@pytest.fixture
def team_repo_mock() -> TeamRepoMock:
    """Mock object for TeamsRepository.

    For mocking purposes, you can modify the return values of its methods::

        team_repo_mock.method_name.return_value = some_value

    To simulate raising exceptions, set the side effects::

        team_repo_mock.method_name.side_effect = SomeException()

    Returns:
        A mocked TeamsRepository
    """

    team_repo = _create_typed_mock(TeamsRepository)

    team_repo.fetch_by_id = AsyncMock()
    team_repo.fetch_by_team_name = AsyncMock()
    team_repo.fetch_all = AsyncMock()
    team_repo.update = AsyncMock()
    team_repo.create = AsyncMock()
    team_repo.delete = AsyncMock()
    team_repo.get_verified_registered_teams_count = AsyncMock()

    return cast(TeamRepoMock, team_repo)


# ======================================
# Mocking Repository layer classes end
# ======================================


# ======================================
# Mocking Service layer classes start
# ======================================


class HackathonServiceMock(Protocol):
    """A Static Duck Type, modeling a Mocked HackathonService

    Should not be initialized directly by application developers to create a HackathonServiceMock instance. It is
    used just for type hinting purposes.
    """

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
    """Mock object for HackathonService.

    For mocking purposes, you can modify the return values of its methods::

        mongo_db_manager_mock.method_name.return_value = some_value

    To simulate raising exceptions, set the side effects::

        mongo_db_manager_mock.method_name.side_effect = SomeException()

    Returns:
        A mocked HackathonService
    """

    hackathon_service = _create_typed_mock(HackathonService)
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
    hackathon_service.send_verification_email = AsyncMock()
    hackathon_service.send_successful_registration_email = Mock()

    return cast(HackathonServiceMock, hackathon_service)


class ParticipantRegistrationServiceMock(Protocol):
    """A Static Duck Type, modeling a Mocked ParticipantRegistrationService

    Should not be initialized directly by application developers to create a ParticipantRegistrationMock instance. It is
    used just for type hinting purposes.
    """

    register_admin_participant: AsyncMock
    register_random_participant: AsyncMock
    register_invite_link_participant: AsyncMock


@pytest.fixture
def participant_registration_service_mock() -> ParticipantRegistrationServiceMock:
    """Mock object for ParticipantRegistrationService.

    For mocking purposes, you can modify the return values of its methods::

        mongo_db_manager_mock.method_name.return_value = some_value

    To simulate raising exceptions, set the side effects::

        mongo_db_manager_mock.method_name.side_effect = SomeException()

    Returns:
        A mocked ParticipantRegistrationService
    """
    service = _create_typed_mock(ParticipantRegistrationService)
    service.register_admin_participant = AsyncMock()
    service.register_random_participant = AsyncMock()
    service.register_invite_link_participant = AsyncMock()

    return cast(ParticipantRegistrationServiceMock, service)


class ParticipantVerificationServiceMock(Protocol):
    """A Static Duck Type, modeling a Mocked ParticipantVerificationService

    Should not be initialized directly by application developers to create a ParticipantVerificationServiceMock
    instance. It is used just for type hinting purposes.
    """

    verify_random_participant: AsyncMock
    verify_admin_participant: AsyncMock
    resend_verification_email: AsyncMock


@pytest.fixture
def participant_verification_service_mock() -> ParticipantVerificationServiceMock:
    """Mock object for ParticipantVerificationService.

    For mocking purposes, you can modify the return values of its methods::

        participant_verification_service_mock.method_name.return_value = some_value

    To simulate raising exceptions, set the side effects::

        participant_verification_service_mock.method_name.side_effect = SomeException()

    Returns:
        A mocked ParticipantVerificationService
    """

    service = _create_typed_mock(ParticipantVerificationService)
    service.verify_random_participant = AsyncMock()
    service.verify_admin_participant = AsyncMock()
    service.resend_verification_email = AsyncMock()

    return cast(ParticipantVerificationServiceMock, service)


#
#
# @pytest.fixture
# def hackathon_mail_service_mock() -> Mock:
#     """This is a mock obj of HackathonMailService. To change the return values of its methods use:
#     `hackathon_mail_service_mock.method_name.return_value=some_return_value`"""
#
#     mailing_service_mock = Mock(spec=HackathonMailService)
#     mailing_service_mock.send_participant_verification_email = Mock()
#     mailing_service_mock.send_participant_successful_registration_email = Mock()
#
#     return mailing_service_mock
#
#
#


# =================================================
# Helper functions for creating test objects start
# =================================================


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
def five_sec_window() -> Tuple[datetime, datetime]:
    now = datetime.now()
    return now - timedelta(seconds=5), now + timedelta(seconds=5)


@pytest.fixture
def thirty_sec_jwt_exp_limit() -> int:
    return int((datetime.now(tz=timezone.utc) + timedelta(seconds=30)).timestamp())


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
def mock_jwt_random_user_verification_data(
    mock_obj_id: str, thirty_sec_jwt_exp_limit: int
) -> JwtParticipantVerificationData:
    return JwtParticipantVerificationData(
        sub=mock_obj_id,
        is_admin=False,
        exp=thirty_sec_jwt_exp_limit,
    )


@pytest.fixture
def mock_jwt_admin_user_verification_data(
    mock_obj_id: str, thirty_sec_jwt_exp_limit: int
) -> JwtParticipantVerificationData:
    return JwtParticipantVerificationData(
        sub=mock_obj_id,
        is_admin=True,
        exp=thirty_sec_jwt_exp_limit,
    )


@pytest.fixture
def mock_jwt_token() -> str:
    return "mock_jwt_token"


# =================================================
# Helper functions for creating test objects end
# =================================================
