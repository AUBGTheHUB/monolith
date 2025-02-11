from abc import ABC, abstractmethod
from typing import Literal

from src.database.model.participant_model import Participant


class MailService(ABC):
    @abstractmethod
    async def send_email(
        self, participant_email: str, subject: str, body_content: str, content_type: Literal["text", "html"] = "text"
    ) -> None:
        """
        Sends an email to the specified receiver with the provided subject and body content.
        Supports both text and HTML bodies.
        :param participant_email: Email of participant
        :param subject: Email subject line
        :param body_content: Body of the email, could be html or just plain text, must be specified in content_type
        :param content_type: Defines the type of the email body, could be "html" (for html body) or "text" (for a plain text body)
        """
        raise NotImplementedError()

    @abstractmethod
    async def send_participant_successful_registration_email(
        self,
        participant: Participant,
        invite_link: str | None = None,
        team_name: str | None = None,
    ) -> None:
        """
        Sends a confirmation email to a participant, confirming their acceptance into the event.
        The email will include details such as the participant's name, team name (if applicable),
        and a verification link. Both text and HTML versions of the email body can be provided.

        :param participant: Participant object.
        :param team_name: The name of the participant's team (if applicable).
        :param invite_link: The invite link for the participant (To invite other team members).
        """
        raise NotImplementedError()

    @abstractmethod
    async def send_participant_verification_email(
        self,
        participant: Participant,
        confirmation_link: str,
        team_name: str | None = None,
    ) -> None:
        """
        Sends a verification email to a participant, informing them that they need to verify their application
        to the event. The email will include details such as the participant's name, team name (if applicable),
        and a verification link for confirming their participation. Both text and HTML versions of the email body
        can be provided.

        :param participant: Participant object.
        :param team_name: The name of the participant's team (if applicable).
        :param confirmation_link: The verification link for the participant.
        """
        raise NotImplementedError()
