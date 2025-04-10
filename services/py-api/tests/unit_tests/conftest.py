from datetime import datetime, timedelta, timezone
from typing import Tuple, Optional, Any, Dict

from fastapi import BackgroundTasks
import pytest
from unittest.mock import Mock, MagicMock, AsyncMock

from motor.motor_asyncio import AsyncIOMotorClientSession
from result import Err

from src.database.db_manager import DatabaseManager
from src.database.model.participant_model import Participant
from src.database.model.team_model import Team
from src.database.repository.feature_switch_repository import FeatureSwitchRepository
from src.database.repository.participants_repository import ParticipantsRepository
from src.database.repository.teams_repository import TeamsRepository
from src.database.transaction_manager import TransactionManager
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
from tests.integration_tests.conftest import (
    TEST_USER_EMAIL,
    TEST_USER_NAME,
    TEST_TEAM_NAME,
    TEST_UNIVERSITY_NAME,
    TEST_ALLOWED_AGE,
    TEST_LOCATION,
)


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


@pytest.fixture
def feature_switch_repo_mock() -> Mock:
    """This is a mock obj of FeatureSwitchRepository. To change the return values of its methods use:
    `feature_switch_repo_mock.method_name.return_value=some_return_value`"""

    feature_switch_repo = Mock(spec=FeatureSwitchRepository)

    feature_switch_repo.fetch_by_id = AsyncMock()
    feature_switch_repo.fetch_by_team_name = AsyncMock()
    feature_switch_repo.fetch_all = AsyncMock()
    feature_switch_repo.update = AsyncMock()
    feature_switch_repo.create = AsyncMock()
    feature_switch_repo.delete = AsyncMock()
    feature_switch_repo.get_feature_switch = AsyncMock()
    feature_switch_repo.set_feature_switch = AsyncMock()

    return feature_switch_repo


@pytest.fixture
def hackathon_service_mock() -> HackathonService:
    """This is a mock obj of HackathonService. To change the return values of its methods use:
    `hackathon_service_mock.method_name.return_value=some_return_value`"""

    hackathon_service = Mock(spec=HackathonService)

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

    return hackathon_service


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

    tx_manager = Mock(spec=TransactionManager)
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
def mock_participant_request_body_admin_case(mock_unverified_team: Team) -> ParticipantRequestBody:
    return ParticipantRequestBody(
        registration_info=AdminParticipantInputData(
            registration_type="admin",
            name=TEST_USER_NAME,
            email=TEST_USER_EMAIL,
            is_admin=True,
            team_name=mock_unverified_team.name,
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
def mock_participant_request_body_invite_link_case(mock_unverified_team: Team) -> ParticipantRequestBody:
    return ParticipantRequestBody(
        registration_info=InviteLinkParticipantInputData(
            registration_type="invite_link",
            name=TEST_USER_NAME,
            email=TEST_USER_EMAIL,
            is_admin=False,
            team_name=mock_unverified_team.name,
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
def mock_participant_request_body_random_case(mock_unverified_team: Team) -> ParticipantRequestBody:
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
def mock_admin_case_input_data(mock_unverified_team: Team) -> AdminParticipantInputData:
    return AdminParticipantInputData(
        registration_type="admin",
        name=TEST_USER_NAME,
        email=TEST_USER_EMAIL,
        is_admin=True,
        team_name=mock_unverified_team.name,
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
def mock_invite_link_case_input_data(mock_unverified_team: Team) -> InviteLinkParticipantInputData:
    return InviteLinkParticipantInputData(
        registration_type="invite_link",
        name=TEST_USER_NAME,
        email=TEST_USER_EMAIL,
        is_admin=False,
        team_name=mock_unverified_team.name,
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
def mock_random_case_input_data() -> RandomParticipantInputData:
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
def mock_unverified_team(mock_obj_id: str) -> Team:
    return Team(id=mock_obj_id, name=TEST_TEAM_NAME)


@pytest.fixture
def mock_verified_team(mock_obj_id: str) -> Team:
    return Team(id=mock_obj_id, name=TEST_TEAM_NAME, is_verified=True)


@pytest.fixture
def mock_unverified_team_dump_no_id(mock_unverified_team: Team) -> Dict[str, Any]:
    """
    This method is used when trying to mock the MongoDB operations in the database layers
    """
    mock_unverified_team_db_document = mock_unverified_team.dump_as_mongo_db_document()
    mock_unverified_team_db_document.pop("_id")
    return mock_unverified_team_db_document


@pytest.fixture
def mock_verified_team_dump_no_id(mock_verified_team: Team) -> Dict[str, Any]:
    """
    This method is used when trying to mock the MongoDB operations in the database layers
    """
    mock_verified_team_db_document = mock_verified_team.dump_as_mongo_db_document()
    mock_verified_team_db_document.pop("_id")
    return mock_verified_team_db_document


@pytest.fixture
def mock_admin_participant(mock_unverified_team: Team, mock_obj_id: str) -> Participant:
    return Participant(
        id=mock_obj_id,
        name=TEST_USER_NAME,
        email=TEST_USER_EMAIL,
        is_admin=True,
        team_id=mock_unverified_team.id,
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
def mock_verified_admin_participant(mock_admin_participant: Participant) -> Participant:
    mock_admin_participant.email_verified = True
    return mock_admin_participant


@pytest.fixture
def mock_admin_participant_dump_no_id(mock_admin_participant: Participant) -> Dict[str, Any]:
    mock_admin_participant_mongo_db_document = mock_admin_participant.dump_as_mongo_db_document()
    # Remove the id here
    mock_admin_participant_mongo_db_document.pop("_id")
    return mock_admin_participant_mongo_db_document


@pytest.fixture
def mock_admin_participant_dump_verified(mock_admin_participant: Participant) -> Dict[str, Any]:
    mock_admin_participant.email_verified = True
    mock_admin_participant_mongo_db_document = mock_admin_participant.dump_as_mongo_db_document()
    # Remove the id here
    mock_admin_participant_mongo_db_document.pop("_id")
    return mock_admin_participant_mongo_db_document


@pytest.fixture
def mock_invite_participant(mock_unverified_team: Team, mock_obj_id: str) -> Participant:
    return Participant(
        id=mock_obj_id,
        name=TEST_USER_NAME,
        email=TEST_USER_EMAIL,
        is_admin=False,
        email_verified=True,
        team_id=mock_unverified_team.id,
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
def mock_verified_invite_participant(mock_invite_participant: Participant) -> Participant:
    mock_invite_participant.email_verified = True
    return mock_invite_participant


@pytest.fixture
def mock_invite_participant_dump_no_id(mock_invite_participant: Participant) -> Dict[str, Any]:
    mock_invite_participant_mongo_db_document = mock_invite_participant.dump_as_mongo_db_document()
    # Remove the id here
    mock_invite_participant_mongo_db_document.pop("_id")
    return mock_invite_participant_mongo_db_document


@pytest.fixture
def mock_invite_participant_dump_verified(mock_invite_participant: Participant) -> Dict[str, Any]:
    mock_invite_participant.email_verified = True
    mock_invite_participant_mongo_db_document = mock_invite_participant.dump_as_mongo_db_document()
    # Remove the id here
    mock_invite_participant_mongo_db_document.pop("_id")
    return mock_invite_participant_mongo_db_document


@pytest.fixture
def mock_random_participant(mock_obj_id: str) -> Participant:
    return Participant(
        id=mock_obj_id,
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
def mock_verified_random_participant(mock_random_participant: Participant) -> Participant:
    mock_random_participant.email_verified = True
    return mock_random_participant


@pytest.fixture
def mock_random_participant_dump_no_id(mock_random_participant: Participant) -> Dict[str, Any]:
    mock_random_participant_mongo_db_document = mock_random_participant.dump_as_mongo_db_document()
    # Remove the id here
    mock_random_participant_mongo_db_document.pop("_id")
    return mock_random_participant_mongo_db_document


@pytest.fixture
def mock_random_participant_dump_verified(mock_random_participant: Participant) -> Dict[str, Any]:
    mock_random_participant.email_verified = True
    mock_random_participant_mongo_db_document = mock_random_participant.dump_as_mongo_db_document()
    # Remove the id here
    mock_random_participant_mongo_db_document.pop("_id")
    return mock_random_participant_mongo_db_document


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
        team_name=TEST_USER_NAME,
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
