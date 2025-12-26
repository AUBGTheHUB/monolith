from datetime import datetime, timedelta
from datetime import timezone

from fastapi import BackgroundTasks
from structlog.stdlib import get_logger

from result import Err, is_err, Result, Ok
from typing import Tuple
from src.database.model.hackathon.participant_model import Participant, UpdateParticipantParams
from src.database.model.hackathon.team_model import Team
from src.database.repository.hackathon.participants_repository import ParticipantsRepository
from src.database.repository.hackathon.teams_repository import TeamsRepository
from src.environment import is_test_env, is_local_env, DOMAIN
from src.exception import (
    ParticipantNotFoundError,
    TeamNotFoundError,
    ParticipantAlreadyVerifiedError,
    EmailRateLimitExceededError,
)
from src.service.constants import (
    FRONTEND_PORT,
    PARTICIPANTS_VERIFICATION_ROUTE,
    PARTICIPANTS_REGISTRATION_ROUTE,
    RATE_LIMIT_SECONDS,
)
from src.service.jwt_utils.codec import JwtUtility
from src.service.jwt_utils.schemas import JwtParticipantVerificationData, JwtParticipantInviteRegistrationData
from src.service.mail_service.mail_clients.base_mail_client import MailClient
from src.service.mail_service.utils import (
    load_email_registration_confirmation_html_template,
    load_email_verify_participant_html_template,
)

LOG = get_logger()


class HackathonMailService:
    """
    Service layer responsible for sending verification and successful registration emails to hackathon participants
    """

    _SENDER_EMAIL = "no-reply@thehub-aubg.com"

    def __init__(
        self,
        client: MailClient,
        jwt_utility: JwtUtility,
        participant_repo: ParticipantsRepository,
        teams_repo: TeamsRepository,
    ) -> None:
        self._client = client
        self._jwt_utility = jwt_utility
        self._participant_repo = participant_repo
        self._teams_repo = teams_repo

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

        err = self.send_participant_verification_email(
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
            err = self.send_participant_successful_registration_email(
                participant=participant, background_tasks=background_tasks
            )
            if err is not None:
                return err

            return None

        if not participant.is_admin:
            # When dealing with invite_link participants we no invite_link should be present in the email
            err = self.send_participant_successful_registration_email(
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

        err = self.send_participant_successful_registration_email(
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

    def send_participant_verification_email(
        self,
        participant: Participant,
        verification_link: str,
        background_tasks: BackgroundTasks,
        team_name: str | None = None,
    ) -> Err[ValueError] | None:
        """
        Sends a verification email to admin and random participants via FastAPI BackgroundTasks

        Args:
            participant: The participant who should receive the email. Admin or random participant only, invite_link
                    participants are automatically verified.
            verification_link: The generated email verification link with appended JWT token.
            background_tasks: This is passed initially from the routes as part of the FastAPI Dependency Injection
                system. It is auto-wired for us. We use background tasks as we want to send an email only once we
                have returned a response. In this way we are able to keep our response times sub-second as we don't
                wait for the email to be sent, which could take more than 2 seconds.
            team_name: Should be passed only when sending admin verification emails. If passed it will show up in the
             verification email as "Hello {participant.name}, from team {team_name}", otherwise it will be only
             "Hello {participant.name}".
        Returns:
            Err[ValueError] if there was an error generating the email body
        """
        try:
            body_html = load_email_verify_participant_html_template(participant.name, team_name, verification_link)
        except ValueError as e:
            LOG.exception(
                "Error loading the HTML template for verification email",
                err=e,
                participant=participant,
                team_name=team_name,
            )
            return Err(e)

        LOG.info("Sending verification email...", participant=participant.dump_as_json(), team_name=team_name)

        background_tasks.add_task(
            self._client.send_email,
            sender=self._SENDER_EMAIL,
            receiver=participant.email,
            subject="Confirm Your Participation in HackAUBG 7.0",
            body_content=body_html,
            content_type="html",
        )

        return None

    def send_participant_successful_registration_email(
        self,
        participant: Participant,
        background_tasks: BackgroundTasks,
        invite_link: str | None = None,
        team_name: str | None = None,
    ) -> Err[ValueError] | None:
        """
        Sends an email confirming the successful registration of a participant.

        Args:
            participant: The participant who should receive the email. Could be admin, random or invite_link participant.
            invite_link: The hackathon participants registration endpoint with appended JWT token. Should be passed
             only when sending emails to admin participants, as they are responsible for sharing the link with teammates.
            background_tasks: This is passed initially from the routes as part of the FastAPI Dependency Injection
             system. It is auto-wired for us. We use background tasks as we want to send an email only once we
             have returned a response. In this way we are able to keep our response times sub-second as we don't
             wait for the email to be sent, which could take more than 2 seconds.
            team_name: Should be passed only when sending emails to admin or invite_link participants. If passed it will
             show up in the confirmation email as "Hello {participant.name}, from team {team_name}", otherwise it will
             be only "Hello {participant.name}".
        Returns:
            Err[ValueError] if there was an error generating the email body
        """

        try:
            body_html = load_email_registration_confirmation_html_template(participant.name, team_name, invite_link)
        except ValueError as e:
            LOG.exception(
                "Error loading the HTML template for successful registration email",
                err=e,
                participant=participant,
                team_name=team_name,
            )
            return Err(e)

        LOG.info(
            "Sending successful registration email...", participant=participant.dump_as_json(), team_name=team_name
        )

        background_tasks.add_task(
            self._client.send_email,
            sender=self._SENDER_EMAIL,
            receiver=participant.email,
            subject="Welcome Aboard! See You at HackAUBG 7.0",
            body_content=body_html,
            content_type="html",
        )

        return None
