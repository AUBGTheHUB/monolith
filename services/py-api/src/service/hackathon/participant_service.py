from datetime import datetime, timedelta
from datetime import timezone

from fastapi import BackgroundTasks
from typing import Tuple, List

from result import Err, is_err, Ok, Result
from structlog.stdlib import get_logger

from src.database.model.base_model import SerializableObjectId
from src.database.model.hackathon.participant_model import Participant, UpdateParticipantParams
from src.database.model.hackathon.team_model import Team
from src.database.repository.hackathon.participants_repository import ParticipantsRepository
from src.database.repository.hackathon.teams_repository import TeamsRepository
from src.environment import is_local_env, DOMAIN, is_test_env
from src.exception import (
    DuplicateEmailError,
    TeamNameMissmatchError,
    TeamNotFoundError,
    ParticipantNotFoundError,
    ParticipantAlreadyVerifiedError,
    EmailRateLimitExceededError,
)
from src.server.schemas.request_schemas.schemas import (
    RandomParticipantInputData,
    InviteLinkParticipantInputData,
)
from src.service.hackathon.constants import (
    FRONTEND_PORT,
    PARTICIPANTS_VERIFICATION_ROUTE,
    PARTICIPANTS_REGISTRATION_ROUTE,
    RATE_LIMIT_SECONDS,
)
from src.service.hackathon.hackathon_mail_service import HackathonMailService
from src.service.jwt_utils.codec import JwtUtility
from src.service.jwt_utils.schemas import JwtParticipantInviteRegistrationData, JwtParticipantVerificationData

LOG = get_logger()


class ParticipantService:
    """Mid-level service layer designed to hold logic related to participants"""

    def __init__(
        self,
        participants_repo: ParticipantsRepository,
        teams_repo: TeamsRepository,
        jwt_utility: JwtUtility,
        hackathon_mail_service: HackathonMailService,
    ) -> None:
        self._participant_repo = participants_repo
        self._teams_repo = teams_repo
        self._jwt_utility = jwt_utility
        self._hackathon_mail_service = hackathon_mail_service

    async def retrieve_and_categorize_random_participants(
        self,
    ) -> Result[Tuple[List[Participant], List[Participant]], Exception]:
        programming_oriented = []
        non_programming_oriented = []
        # Fetch all the verified random participants
        result = await self._participant_repo.get_verified_random_participants()

        # Return the result to the upper layer in case of an Exception
        if is_err(result):
            return result

        # Group the into categories programming oriented, non-programming oriented
        for participant in result.ok_value:
            if participant.programming_level == "I am not participating as a programmer":
                non_programming_oriented.append(participant)
            else:
                programming_oriented.append(participant)

        return Ok((programming_oriented, non_programming_oriented))

    async def create_random_participant(
        self, input_data: RandomParticipantInputData
    ) -> Result[Tuple[Participant, None], DuplicateEmailError | Exception]:

        result = await self._participant_repo.create(
            Participant(**input_data.model_dump(), is_admin=False, team_id=None)
        )
        if is_err(result):
            return result

        # As when first created, the random participant is not assigned to a team we return the team as None
        return Ok((result.ok_value, None))

    async def create_invite_link_participant(
        self, input_data: InviteLinkParticipantInputData, decoded_jwt_token: JwtParticipantInviteRegistrationData
    ) -> Result[Tuple[Participant, Team], DuplicateEmailError | TeamNotFoundError | TeamNameMissmatchError | Exception]:

        # Check if team still exists - Returns an error when it doesn't
        team_result = await self._teams_repo.fetch_by_id(decoded_jwt_token.team_id)
        if is_err(team_result):
            return team_result

        # Check if the team_name from the token is consistent with the team_name from the request body
        # A missmatch could occur if the frontend passes something different
        if input_data.team_name != team_result.ok_value.name:
            return Err(TeamNameMissmatchError())

        participant_result = await self._participant_repo.create(
            Participant(
                **input_data.model_dump(),
                team_id=SerializableObjectId(decoded_jwt_token.team_id),
                email_verified=True,
            )
        )
        if is_err(participant_result):
            return participant_result

        # Return the new participant
        return Ok((participant_result.ok_value, team_result.ok_value))

    async def delete_participant(
        self, participant_id: str
    ) -> Result[Participant, ParticipantNotFoundError | Exception]:
        return await self._participant_repo.delete(obj_id=participant_id)

    async def verify_random_participant(
        self, jwt_data: JwtParticipantVerificationData
    ) -> Result[Tuple[Participant, None], ParticipantNotFoundError | ParticipantAlreadyVerifiedError | Exception]:

        # This step is taken to ensure that we are not verifying an already verified participant
        result = await self._participant_repo.fetch_by_id(jwt_data.sub)

        if is_err(result):
            return result

        if result.ok_value.email_verified:
            return Err(ParticipantAlreadyVerifiedError())

        # Updates the random participant if it exists
        result = await self._participant_repo.update(
            obj_id=jwt_data.sub, obj_fields=UpdateParticipantParams(email_verified=True)
        )

        if is_err(result):
            return result

        # As when first created, the random participant is not assigned to a team we return the team as None
        return Ok((result.ok_value, None))

    async def send_verification_email(
        self, participant: Participant, background_tasks: BackgroundTasks, team: Team | None = None
    ) -> Result[Participant, ParticipantNotFoundError | ValueError | Exception] | None:
        """
        Sends a verification email to admin and random participants and adds a timestamp when the last verification
        email has been sent, for rate-limiting purposes
        Args:
            participant: the participant who should receive the email. Admin or random participant only, invite_link
                participants are automatically verified.
            team: The team which the admin participant created. Should be passed only when sending emails to admin
             participants, as random teams are created only after hackathon registration closes.
            background_tasks: This is passed initially from the routes as part of the FastAPI Dependency Injection
                system. It is auto-wired for us. We use background tasks as we want to send an email only once we
                have returned a response. In this way we are able to keep our response times sub-second as we don't
                wait for the email to be sent, which could take more than 2 seconds.
        Returns:
            * The updated Participant document (last_sent_verification_email and updated_at fields)

            * An Err if adding of the updating the participant document last_sent_verification_email property fails, or
            sending the verification emails fails.

            * None if we are in Test env, and we should not send emails
        """

        # Don't send emails when we are running tests
        if is_test_env():
            return None

        # Build the payload for the Jwt token
        expiration = int((datetime.now(timezone.utc) + timedelta(hours=24)).timestamp())
        payload = JwtParticipantVerificationData(sub=str(participant.id), is_admin=participant.is_admin, exp=expiration)

        # Create the Jwt Token
        jwt_token = self._jwt_utility.encode_data(data=payload)

        # Append the Jwt to the endpoint
        if is_local_env():
            verification_link = (
                f"http://{DOMAIN}:{FRONTEND_PORT}{PARTICIPANTS_VERIFICATION_ROUTE}?jwt_token={jwt_token}"
            )
        else:
            verification_link = f"https://{DOMAIN}{PARTICIPANTS_VERIFICATION_ROUTE}?jwt_token={jwt_token}"

        # Update the last_sent_verification_email field for rate-limiting purposes
        result = await self._participant_repo.update(
            obj_id=str(participant.id), obj_fields=UpdateParticipantParams(last_sent_verification_email=datetime.now())
        )

        # If the update fails, do not send the email and return the error (could happen if the participant is deleted
        # from the DB before it is updated, highly unlikely in PROD env)
        if is_err(result):
            return result

        err = self._hackathon_mail_service.send_participant_verification_email(
            participant=result.ok_value,
            verification_link=verification_link,
            background_tasks=background_tasks,
            team_name=team.name if team else None,
        )

        if err is not None:
            return err

        # Return the updated participant
        return result

    def send_successful_registration_email(
        self, participant: Participant, background_tasks: BackgroundTasks, team: Team | None = None
    ) -> Err[ValueError] | None:
        """
        Sends an email confirming the successful registration of a participant.
        Args:
            participant: The participant who should receive the email. Could be admin, random or invite_link
             participant.
            team: The team which the admin participant created. Should be passed only when sending emails to admin or
             invite_link participants.
            background_tasks: This is passed initially from the routes as part of the FastAPI Dependency Injection
             system. It is auto-wired for us. We use background tasks as we want to send an email only once we have
             returned a response. In this way we are able to keep our response times sub-second as we don't wait for
             the email to be sent, which could take more than 2 seconds.
        Returns:
            An Err if sending the successful registration email fails
        """
        # Don't send emails when we are running tests
        if is_test_env():
            return None

        if team is None:
            # When dealing with random participants we no team_name and invite_link should be present in the email
            err = self._hackathon_mail_service.send_participant_successful_registration_email(
                participant=participant, background_tasks=background_tasks
            )
            if err is not None:
                return err

            return None

        if not participant.is_admin:
            # When dealing with invite_link participants we no invite_link should be present in the email
            err = self._hackathon_mail_service.send_participant_successful_registration_email(
                participant=participant, team_name=team.name, background_tasks=background_tasks
            )
            if err is not None:
                return err

            return None

        # Build the payload for the Jwt token
        expiration = int((datetime.now(timezone.utc) + timedelta(days=15)).timestamp())
        payload = JwtParticipantInviteRegistrationData(
            sub=str(participant.id), team_id=str(team.id), team_name=team.name, exp=expiration
        )

        # Create the Jwt Token
        jwt_token = self._jwt_utility.encode_data(data=payload)

        # Append the Jwt to the endpoint
        if is_local_env():
            invite_link = f"http://{DOMAIN}:{FRONTEND_PORT}{PARTICIPANTS_REGISTRATION_ROUTE}?jwt_token={jwt_token}"
        else:
            invite_link = f"https://{DOMAIN}{PARTICIPANTS_REGISTRATION_ROUTE}?jwt_token={jwt_token}"

        err = self._hackathon_mail_service.send_participant_successful_registration_email(
            participant=participant, background_tasks=background_tasks, invite_link=invite_link, team_name=team.name
        )
        if err is not None:
            return err

        return None

    async def check_send_verification_email_rate_limit(self, participant_id: str) -> Result[
        Tuple[Participant, Team],
        ParticipantNotFoundError
        | TeamNotFoundError
        | ParticipantAlreadyVerifiedError
        | EmailRateLimitExceededError
        | Exception,
    ]:
        """Check if the verification email rate limit has been reached

        Returns:
            * A Tuple[Participant, Team] if the participant has not exceeded their email sending rate
            * A ParticipantNotFoundError if the participant resending the email is not found in the Database
            * A TeamNotFoundError if the team of the participant is not found in the Database
            * A ParticipantAlreadyVerifiedError if the participant has already been verified
            * An EmailRateLimitExceededError if the participant has exceeded their email sending rate
            * An Exception if some unexpected error occurred
        """

        participant = await self._participant_repo.fetch_by_id(obj_id=participant_id)

        # If there was an error fetching the participant return that error as it is as it will be handled further up by
        # the handler
        if is_err(participant):
            return participant

        # Check if the participant is already verified before sending another verification email
        if participant.ok_value.email_verified:
            return Err(ParticipantAlreadyVerifiedError())

        # We fetch the team so that we take advantage of the team info we have to pass to the mailing service
        team = (
            await self._teams_repo.fetch_by_id(obj_id=str(participant.ok_value.team_id))
            if participant.ok_value.is_admin
            else Ok(None)
        )

        # If there was an error fetching the team return that error as it is as it will be handled further up by the
        # handler
        if is_err(team):
            return team

        # The last_sent_mail field is None when there has not been any email sent previously
        if participant.ok_value.last_sent_verification_email is None:
            return Ok((participant.ok_value, team.ok_value))

        # Calculate the rate limit
        is_within_rate_limit = datetime.now() - participant.ok_value.last_sent_verification_email >= timedelta(
            seconds=RATE_LIMIT_SECONDS
        )

        # If it is not within the rate limit raise an error
        if not is_within_rate_limit:
            remaining_time = (
                RATE_LIMIT_SECONDS - (datetime.now() - participant.ok_value.last_sent_verification_email).seconds
            )

            return Err(EmailRateLimitExceededError(seconds_to_retry_after=remaining_time))

        return Ok((participant.ok_value, team.ok_value))
