# mypy: disable_error_code=method-assign
# This is because we have TypedMocks which mypy thinks are the actual classes

from datetime import datetime, timedelta, timezone
from os import environ
from typing import Any, cast
from unittest.mock import AsyncMock, MagicMock, Mock

"""Mock AWS Credentials for testing moto."""
environ["AWS_ACCESS_KEY_ID"] = "test-key"
environ["AWS_SECRET_ACCESS_KEY"] = "test-key"
environ["AWS_DEFAULT_REGION"] = "us-east-2"
environ["AWS_S3_DEFAULT_BUCKET"] = "dabucket"

import pytest
from fastapi import BackgroundTasks
from motor.motor_asyncio import (
    AsyncIOMotorClient,
    AsyncIOMotorClientSession,
    AsyncIOMotorCollection,
    AsyncIOMotorCursor,
    AsyncIOMotorDatabase,
)
from typing_extensions import Protocol

from src.database.model.admin.past_event_model import PastEvent
from src.database.model.admin.sponsor_model import Sponsor
from src.database.model.hackathon.participant_model import Participant
from src.database.model.hackathon.team_model import Team
from src.database.mongo.db_manager import MongoDatabaseManager
from src.database.mongo.transaction_manager import MongoTransactionManager
from src.database.repository.admin.past_events_repository import PastEventsRepository
from src.database.repository.admin.sponsors_repository import SponsorsRepository
from src.database.repository.feature_switch_repository import FeatureSwitchRepository
from src.database.repository.hackathon.participants_repository import ParticipantsRepository
from src.database.repository.hackathon.teams_repository import TeamsRepository
from src.server.schemas.request_schemas.hackathon.schemas import (
    AdminParticipantInputData,
    InviteLinkParticipantInputData,
    ParticipantRequestBody,
    RandomParticipantInputData,
    ResendEmailParticipantData,
)
from src.service.hackathon.admin_team_service import AdminTeamService
from src.service.hackathon.hackathon_mail_service import HackathonMailService
from src.service.hackathon.hackathon_utility_service import HackathonUtilityService
from src.service.hackathon.participant_service import ParticipantService
from src.service.hackathon.registration_service import RegistrationService
from src.service.hackathon.team_service import TeamService
from src.service.hackathon.verification_service import VerificationService
from src.service.utility.aws_service import AwsService
from src.service.utility.image_storing.image_storing_service import ImageStoringService
from src.service.jwt_utils.codec import JwtUtility
from src.service.jwt_utils.schemas import JwtParticipantInviteRegistrationData, JwtParticipantVerificationData

from src.service.admin.past_events_service import PastEventsService
from src.service.admin.sponsors_service import SponsorsService

from tests.integration_tests.conftest import (
    TEST_ALLOWED_AGE,
    TEST_LOCATION,
    TEST_TEAM_NAME,
    TEST_UNIVERSITY_NAME,
    TEST_USER_EMAIL,
    TEST_USER_NAME,
)


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


class MotorDbCursorMock(Protocol):
    to_list: AsyncMock


@pytest.fixture
def db_cursor_mock() -> MotorDbCursorMock:
    db_cursor_mock = _create_typed_mock(AsyncIOMotorCursor)
    db_cursor_mock.to_list = AsyncMock()

    return cast(MotorDbCursorMock, db_cursor_mock)


class MongoTransactionManagerMock(Protocol):
    with_transaction: AsyncMock


@pytest.fixture
def tx_manager_mock() -> MongoTransactionManagerMock:
    """This is a mock obj of TransactionManager. To change the return values of its methods use:
    `tx_manager_mock.method_name.return_value=some_return_value`"""

    tx_manager_mock = _create_typed_mock(MongoTransactionManager)
    tx_manager_mock.with_transaction = AsyncMock()

    return cast(MongoTransactionManagerMock, tx_manager_mock)


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


class FeatureSwitchRepoMock(Protocol):
    get_feature_switch: AsyncMock
    create: AsyncMock
    delete: AsyncMock
    fetch_all: AsyncMock
    fetch_by_id: AsyncMock
    update: AsyncMock
    update_by_name: AsyncMock


@pytest.fixture
def feature_switch_repo_mock() -> FeatureSwitchRepoMock:
    """This is a mock obj of FeatureSwitchRepository. To change the return values of its methods use:
    `feature_switch_repo_mock.method_name.return_value=some_return_value`"""

    feature_switch_repo = _create_typed_mock(FeatureSwitchRepository)

    feature_switch_repo.get_feature_switch = AsyncMock()
    feature_switch_repo.create = AsyncMock()
    feature_switch_repo.delete = AsyncMock()
    feature_switch_repo.fetch_all = AsyncMock()
    feature_switch_repo.fetch_by_id = AsyncMock()
    feature_switch_repo.update = AsyncMock()
    feature_switch_repo.update_by_name = AsyncMock()

    return cast(FeatureSwitchRepoMock, feature_switch_repo)


class PastEventsRepoMock(Protocol):
    fetch_by_id: AsyncMock
    fetch_all: AsyncMock
    update: AsyncMock
    create: AsyncMock
    delete: AsyncMock


@pytest.fixture
def past_events_repo_mock() -> PastEventsRepoMock:
    past_events_repo = _create_typed_mock(PastEventsRepository)

    past_events_repo.fetch_by_id = AsyncMock()
    past_events_repo.fetch_all = AsyncMock()
    past_events_repo.update = AsyncMock()
    past_events_repo.create = AsyncMock()
    past_events_repo.delete = AsyncMock()

    return cast(PastEventsRepoMock, past_events_repo)


class SponsorsRepoMock(Protocol):
    fetch_by_id: AsyncMock
    fetch_all: AsyncMock
    update: AsyncMock
    create: AsyncMock
    delete: AsyncMock


@pytest.fixture
def sponsors_repo_mock() -> SponsorsRepoMock:
    sponsors_repo = _create_typed_mock(SponsorsRepository)

    sponsors_repo.fetch_by_id = AsyncMock()
    sponsors_repo.fetch_all = AsyncMock()
    sponsors_repo.update = AsyncMock()
    sponsors_repo.create = AsyncMock()
    sponsors_repo.delete = AsyncMock()

    return cast(SponsorsRepoMock, sponsors_repo)


# ======================================
# Mocking Repository layer classes end
# ======================================


# ======================================
# Mocking Service layer classes start
# ======================================


class PastEventsServiceMock(Protocol):
    get_all: AsyncMock
    get: AsyncMock
    create: AsyncMock
    update: AsyncMock
    delete: AsyncMock


@pytest.fixture
def past_events_service_mock() -> PastEventsServiceMock:
    service = _create_typed_mock(PastEventsService)

    service.get_all = _create_typed_async_mock(PastEventsService.get_all)
    service.get = AsyncMock()
    service.create = AsyncMock()
    service.update = AsyncMock()
    service.delete = AsyncMock()

    return cast(PastEventsServiceMock, service)


class SponsorsServiceMock(Protocol):
    get_all: AsyncMock
    get: AsyncMock
    create: AsyncMock
    update: AsyncMock
    delete: AsyncMock


@pytest.fixture
def sponsors_service_mock() -> SponsorsServiceMock:
    service = _create_typed_mock(SponsorsService)

    service.get_all = _create_typed_async_mock(SponsorsService.get_all)
    service.get = AsyncMock()
    service.create = AsyncMock()
    service.update = AsyncMock()
    service.delete = AsyncMock()

    return cast(SponsorsServiceMock, service)


class AwsServiceMock(Protocol):
    get_s3_client: Mock
    upload_file: Mock


@pytest.fixture
def aws_service_mock() -> AwsServiceMock:
    service = _create_typed_mock(AwsService)

    service.get_s3_client = Mock()
    service.upload_file = Mock()

    return cast(AwsServiceMock, service)


class ImageStoringServiceMock(Protocol):
    upload_image: AsyncMock
    compress_image: Mock


@pytest.fixture
def image_storing_service_mock() -> ImageStoringServiceMock:
    service = _create_typed_mock(ImageStoringService)

    service.upload_image = _create_typed_async_mock(ImageStoringService.upload_image)
    service.compress_image = Mock()

    return cast(ImageStoringServiceMock, service)


class HackathonUtilityServiceMock(Protocol):
    """A Static Duck Type, modeling a Mocked HackathonService

    Should not be initialized directly by application developers to create a HackathonServiceMock instance. It is
    used just for type hinting purposes.
    """

    check_capacity_register_admin_participant_case: AsyncMock
    check_capacity_register_random_participant_case: AsyncMock


@pytest.fixture
def hackathon_utility_service_mock() -> HackathonUtilityServiceMock:
    """Mock object for HackathonService.

    For mocking purposes, you can modify the return values of its methods::

        mongo_db_manager_mock.method_name.return_value = some_value

    To simulate raising exceptions, set the side effects::

        mongo_db_manager_mock.method_name.side_effect = SomeException()

    Returns:
        A mocked HackathonService
    """

    hackathon_service = _create_typed_mock(HackathonUtilityService)
    hackathon_service.check_capacity_register_admin_participant_case = AsyncMock()
    hackathon_service.check_capacity_register_random_participant_case = AsyncMock()

    return cast(HackathonUtilityServiceMock, hackathon_service)


class ParticipantServiceMock(Protocol):
    """A Static Duck Type, modeling a Mocked ParticipantService

    Should not be initialized directly by application developers to create a ParticipantServiceMock instance. It is
    used just for type hinting purposes.
    """

    create_random_participant: AsyncMock
    create_invite_link_participant: AsyncMock
    delete_participant: AsyncMock
    send_verification_email: AsyncMock
    send_successful_registration_email: AsyncMock
    check_send_verification_email_rate_limit: AsyncMock
    verify_random_participant: AsyncMock


@pytest.fixture
def participant_service_mock() -> ParticipantServiceMock:
    """Mock object for ParticipantService.

    Returns:
        A mocked ParticipantService
    """
    participant_service = _create_typed_mock(ParticipantService)
    participant_service.create_random_participant = AsyncMock()
    participant_service.create_invite_link_participant = AsyncMock()
    participant_service.delete_participant = AsyncMock()
    participant_service.verify_random_participant = AsyncMock()
    participant_service.send_verification_email = AsyncMock()
    participant_service.send_successful_registration_email = Mock()
    participant_service.check_send_verification_email_rate_limit = AsyncMock()
    return cast(ParticipantServiceMock, participant_service)


class TeamServiceMock(Protocol):
    """A Static Duck Type, modeling a Mocked TeamService

    Should not be initialized directly by application developers to create a ParticipantServiceMock instance. It is
    used just for type hinting purposes.
    """

    check_team_capacity: AsyncMock
    delete_team: AsyncMock


@pytest.fixture
def team_service_mock() -> TeamServiceMock:
    """Mock object for TeamService.

    Returns:
        A mocked TeamService
    """
    team_service = _create_typed_mock(TeamService)
    team_service.delete_team = AsyncMock()
    team_service.check_team_capacity = _create_typed_mock(TeamService.check_team_capacity)
    return cast(TeamServiceMock, team_service)


class AdminTeamServiceMock(Protocol):
    """A Static Duck Type, modeling a Mocked HackathonService

    Should not be initialized directly by application developers to create a HackathonServiceMock instance. It is
    used just for type hinting purposes.
    """

    create_participant_and_team_in_transaction: AsyncMock
    verify_admin_participant_and_team_in_transaction: AsyncMock


@pytest.fixture
def admin_team_service_mock() -> AdminTeamServiceMock:
    """Mock object for AdminTeamService.

    Returns:
        A mocked AdminTeamService
    """

    admin_team_service = _create_typed_mock(AdminTeamService)
    admin_team_service.verify_admin_participant_and_team_in_transaction = AsyncMock()
    admin_team_service.create_participant_and_team_in_transaction = AsyncMock()
    return cast(AdminTeamServiceMock, admin_team_service)


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
    service = _create_typed_mock(RegistrationService)
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

    service = _create_typed_mock(VerificationService)
    service.verify_random_participant = AsyncMock()
    service.verify_admin_participant = AsyncMock()
    service.resend_verification_email = AsyncMock()

    return cast(ParticipantVerificationServiceMock, service)


class HackathonMailServiceMock(Protocol):
    send_participant_verification_email = AsyncMock
    send_participant_successful_registration_email = AsyncMock


@pytest.fixture
def hackathon_mail_service_mock() -> HackathonMailServiceMock:
    """This is a mock obj of HackathonMailService. To change the return values of its methods use:
    `hackathon_mail_service_mock.method_name.return_value=some_return_value`"""

    hakcathon_mail_service_mock = _create_typed_mock(HackathonMailService)

    hakcathon_mail_service_mock.send_participant_verification_email = Mock()
    hakcathon_mail_service_mock.send_participant_successful_registration_email = Mock()

    return cast(HackathonMailServiceMock, hakcathon_mail_service_mock)


# =================================================
# Helper functions for creating test objects start
# =================================================


@pytest.fixture
def jwt_utility_mock() -> JwtUtility:
    return JwtUtility()


@pytest.fixture
def participant_request_body_admin_case_mock(unverified_team_mock: Team) -> ParticipantRequestBody:
    return ParticipantRequestBody(
        registration_info=AdminParticipantInputData(
            registration_type="admin",
            name=TEST_USER_NAME,
            email=TEST_USER_EMAIL,
            is_admin=True,
            team_name=unverified_team_mock.name,
            university=TEST_UNIVERSITY_NAME,
            location=TEST_LOCATION,
            age=TEST_ALLOWED_AGE,
            has_participated_in_hackathons=True,
            has_participated_in_hackaubg=True,
            has_internship_interest=True,
            has_previous_coding_experience=True,
            share_info_with_sponsors=True,
        )
    )


@pytest.fixture
def participant_request_body_invite_link_case_mock(unverified_team_mock: Team) -> ParticipantRequestBody:
    return ParticipantRequestBody(
        registration_info=InviteLinkParticipantInputData(
            registration_type="invite_link",
            name=TEST_USER_NAME,
            email=TEST_USER_EMAIL,
            is_admin=False,
            team_name=unverified_team_mock.name,
            university=TEST_UNIVERSITY_NAME,
            location=TEST_LOCATION,
            age=TEST_ALLOWED_AGE,
            has_participated_in_hackathons=True,
            has_participated_in_hackaubg=True,
            has_internship_interest=True,
            has_previous_coding_experience=True,
            share_info_with_sponsors=True,
        )
    )


@pytest.fixture
def participant_request_body_random_case_mock(unverified_team_mock: Team) -> ParticipantRequestBody:
    return ParticipantRequestBody(
        registration_info=RandomParticipantInputData(
            registration_type="random",
            name=TEST_USER_NAME,
            email=TEST_USER_EMAIL,
            university=TEST_UNIVERSITY_NAME,
            location=TEST_LOCATION,
            age=TEST_ALLOWED_AGE,
            has_participated_in_hackathons=True,
            has_participated_in_hackaubg=True,
            has_internship_interest=True,
            has_previous_coding_experience=True,
            share_info_with_sponsors=True,
        )
    )


@pytest.fixture
def admin_case_input_data_mock(unverified_team_mock: Team) -> AdminParticipantInputData:
    return AdminParticipantInputData(
        registration_type="admin",
        name=TEST_USER_NAME,
        email=TEST_USER_EMAIL,
        is_admin=True,
        team_name=unverified_team_mock.name,
        university=TEST_UNIVERSITY_NAME,
        location=TEST_LOCATION,
        age=TEST_ALLOWED_AGE,
        has_participated_in_hackathons=True,
        has_participated_in_hackaubg=True,
        has_internship_interest=True,
        has_previous_coding_experience=True,
        share_info_with_sponsors=True,
    )


@pytest.fixture
def invite_link_case_input_data_mock(unverified_team_mock: Team) -> InviteLinkParticipantInputData:
    return InviteLinkParticipantInputData(
        registration_type="invite_link",
        name=TEST_USER_NAME,
        email=TEST_USER_EMAIL,
        is_admin=False,
        team_name=unverified_team_mock.name,
        university=TEST_UNIVERSITY_NAME,
        location=TEST_LOCATION,
        age=TEST_ALLOWED_AGE,
        has_participated_in_hackathons=True,
        has_participated_in_hackaubg=True,
        has_internship_interest=True,
        has_previous_coding_experience=True,
        share_info_with_sponsors=True,
    )


@pytest.fixture
def random_case_input_data_mock() -> RandomParticipantInputData:
    return RandomParticipantInputData(
        registration_type="random",
        name=TEST_USER_NAME,
        email=TEST_USER_EMAIL,
        university=TEST_UNIVERSITY_NAME,
        location=TEST_LOCATION,
        age=TEST_ALLOWED_AGE,
        has_participated_in_hackathons=True,
        has_participated_in_hackaubg=True,
        has_internship_interest=True,
        has_previous_coding_experience=True,
        share_info_with_sponsors=True,
    )


@pytest.fixture
def unverified_team_mock(obj_id_mock: str) -> Team:
    return Team(id=obj_id_mock, name=TEST_TEAM_NAME)


@pytest.fixture
def verified_team_mock(obj_id_mock: str) -> Team:
    return Team(id=obj_id_mock, name=TEST_TEAM_NAME, is_verified=True)


@pytest.fixture
def unverified_team_dump_no_id_mock(unverified_team_mock: Team) -> dict[str, Any]:
    """
    This method is used when trying to mock the MongoDB operations in the database layers
    """
    mock_unverified_team_db_document = unverified_team_mock.dump_as_mongo_db_document()
    mock_unverified_team_db_document.pop("_id")
    return mock_unverified_team_db_document


@pytest.fixture
def verified_team_dump_no_id_mock(verified_team_mock: Team) -> dict[str, Any]:
    """
    This method is used when trying to mock the MongoDB operations in the database layers
    """
    mock_verified_team_db_document = verified_team_mock.dump_as_mongo_db_document()
    mock_verified_team_db_document.pop("_id")
    return mock_verified_team_db_document


@pytest.fixture
def past_event_mock(obj_id_mock: str) -> PastEvent:
    return PastEvent(id=obj_id_mock, title="t", cover_picture="https://url.com")


@pytest.fixture
def past_event_dump_no_id_mock(past_event_mock: PastEvent) -> dict[str, Any]:
    document = past_event_mock.dump_as_mongo_db_document()
    document.pop("_id")
    return document


@pytest.fixture
def sponsor_mock(obj_id_mock: str) -> Sponsor:
    return Sponsor(
        id=obj_id_mock,
        name="Coca-Cola",
        tier="GOLD",
        website_url="https://coca-cola.com/",
        logo_url="https://eu.aws.com/coca-cola.jpg",
    )


@pytest.fixture
def sponsor_no_id_mock(sponsor_mock: Sponsor) -> dict[str, Any]:
    document = sponsor_mock.dump_as_mongo_db_document()
    document.pop("_id")
    return document


@pytest.fixture
def admin_participant_mock(unverified_team_mock: Team, obj_id_mock: str) -> Participant:
    return Participant(
        id=obj_id_mock,
        name=TEST_USER_NAME,
        email=TEST_USER_EMAIL,
        is_admin=True,
        team_id=unverified_team_mock.id,
        university=TEST_UNIVERSITY_NAME,
        location=TEST_LOCATION,
        age=TEST_ALLOWED_AGE,
        has_participated_in_hackathons=True,
        has_participated_in_hackaubg=True,
        has_internship_interest=True,
        has_previous_coding_experience=True,
        share_info_with_sponsors=True,
    )


@pytest.fixture
def verified_admin_participant_mock(admin_participant_mock: Participant) -> Participant:
    admin_participant_mock.email_verified = True
    return admin_participant_mock


@pytest.fixture
def admin_participant_dump_no_id_mock(admin_participant_mock: Participant) -> dict[str, Any]:
    mock_admin_participant_mongo_db_document = admin_participant_mock.dump_as_mongo_db_document()
    # Remove the id here
    mock_admin_participant_mongo_db_document.pop("_id")
    return mock_admin_participant_mongo_db_document


@pytest.fixture
def admin_participant_dump_verified_mock(admin_participant_mock: Participant) -> dict[str, Any]:
    admin_participant_mock.email_verified = True
    mock_admin_participant_mongo_db_document = admin_participant_mock.dump_as_mongo_db_document()
    # Remove the id here
    mock_admin_participant_mongo_db_document.pop("_id")
    return mock_admin_participant_mongo_db_document


@pytest.fixture
def invite_participant_mock(unverified_team_mock: Team, obj_id_mock: str) -> Participant:
    return Participant(
        id=obj_id_mock,
        name=TEST_USER_NAME,
        email=TEST_USER_EMAIL,
        is_admin=False,
        email_verified=True,
        team_id=unverified_team_mock.id,
        university=TEST_UNIVERSITY_NAME,
        location=TEST_LOCATION,
        age=TEST_ALLOWED_AGE,
        has_participated_in_hackathons=True,
        has_participated_in_hackaubg=True,
        has_internship_interest=True,
        has_previous_coding_experience=True,
        share_info_with_sponsors=True,
    )


@pytest.fixture
def verified_invite_participant_mock(invite_participant_mock: Participant) -> Participant:
    invite_participant_mock.email_verified = True
    return invite_participant_mock


@pytest.fixture
def invite_participant_dump_no_id_mock(invite_participant_mock: Participant) -> dict[str, Any]:
    mock_invite_participant_mongo_db_document = invite_participant_mock.dump_as_mongo_db_document()
    # Remove the id here
    mock_invite_participant_mongo_db_document.pop("_id")
    return mock_invite_participant_mongo_db_document


@pytest.fixture
def invite_participant_dump_verified_mock(invite_participant_mock: Participant) -> dict[str, Any]:
    invite_participant_mock.email_verified = True
    mock_invite_participant_mongo_db_document = invite_participant_mock.dump_as_mongo_db_document()
    # Remove the id here
    mock_invite_participant_mongo_db_document.pop("_id")
    return mock_invite_participant_mongo_db_document


@pytest.fixture
def random_participant_mock(obj_id_mock: str) -> Participant:
    return Participant(
        id=obj_id_mock,
        name=TEST_USER_NAME,
        email=TEST_USER_EMAIL,
        is_admin=False,
        team_id=None,
        university=TEST_UNIVERSITY_NAME,
        location=TEST_LOCATION,
        age=TEST_ALLOWED_AGE,
        has_participated_in_hackathons=True,
        has_participated_in_hackaubg=True,
        has_internship_interest=True,
        has_previous_coding_experience=True,
        share_info_with_sponsors=True,
    )


@pytest.fixture
def verified_random_participant_mock(random_participant_mock: Participant) -> Participant:
    random_participant_mock.email_verified = True
    return random_participant_mock


@pytest.fixture
def random_participant_dump_no_id_mock(random_participant_mock: Participant) -> dict[str, Any]:
    mock_random_participant_mongo_db_document = random_participant_mock.dump_as_mongo_db_document()
    # Remove the id here
    mock_random_participant_mongo_db_document.pop("_id")
    return mock_random_participant_mongo_db_document


@pytest.fixture
def random_participant_dump_verified_mock(random_participant_mock: Participant) -> dict[str, Any]:
    random_participant_mock.email_verified = True
    mock_random_participant_mongo_db_document = random_participant_mock.dump_as_mongo_db_document()
    # Remove the id here
    mock_random_participant_mongo_db_document.pop("_id")
    return mock_random_participant_mongo_db_document


@pytest.fixture
def obj_id_mock() -> str:
    return "507f1f77bcf86cd799439011"


@pytest.fixture
def jwt_user_registration_mock(obj_id_mock: str, thirty_sec_jwt_exp_limit: int) -> JwtParticipantInviteRegistrationData:
    return JwtParticipantInviteRegistrationData(
        sub=obj_id_mock,
        team_id=obj_id_mock,
        team_name=TEST_USER_NAME,
        exp=thirty_sec_jwt_exp_limit,
    )


@pytest.fixture
def jwt_random_user_verification_mock(
    obj_id_mock: str, thirty_sec_jwt_exp_limit: int
) -> JwtParticipantVerificationData:
    return JwtParticipantVerificationData(
        sub=obj_id_mock,
        is_admin=False,
        exp=thirty_sec_jwt_exp_limit,
    )


@pytest.fixture
def jwt_admin_user_verification_mock(obj_id_mock: str, thirty_sec_jwt_exp_limit: int) -> JwtParticipantVerificationData:
    return JwtParticipantVerificationData(
        sub=obj_id_mock,
        is_admin=True,
        exp=thirty_sec_jwt_exp_limit,
    )


@pytest.fixture
def ten_sec_window() -> tuple[datetime, datetime]:
    now = datetime.now()
    return now - timedelta(seconds=10), now + timedelta(seconds=10)


@pytest.fixture
def thirty_sec_jwt_exp_limit() -> int:
    return int((datetime.now(tz=timezone.utc) + timedelta(seconds=30)).timestamp())


@pytest.fixture
def resend_verification_email_data_mock(obj_id_mock: str) -> ResendEmailParticipantData:
    return ResendEmailParticipantData(participant_id=obj_id_mock)


# =================================================
# Helper functions for creating test objects end
# =================================================
