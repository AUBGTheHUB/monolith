from abc import ABC, abstractmethod
from typing import Optional


class MailService(ABC):
    @abstractmethod
    async def send_email(
        self, receiver: str, subject: str, body_text: Optional[str] = None, body_html: Optional[str] = None
    ) -> None:
        """
        Sends an email to the specified receiver with the provided subject and body content.
        Supports both text and HTML bodies.
        :param receiver: Recipient's email address
        :param subject: Email subject line
        :param body_text: Plain text version of the email body
        :param body_html: HTML version of the email body
        """

    @abstractmethod
    async def send_participant_successful_confirmation_email(
        self,
        receiver: str,
        subject: str,
        participant: str,
        team_name: str,
        invite_link: str,
        body_text: Optional[str] = None,
        body_html: Optional[str] = None,
    ) -> None:
        """
        Sends a confirmation email to a participant, confirming their acceptance into the event.
        The email will include details such as the participant's name, team name (if applicable),
        and a verification link. Both text and HTML versions of the email body can be provided.

        Parameters:
            receiver (str): The email address of the recipient.
            subject (str): The subject line of the email.
            participant (str): The name of the participant.
            team_name (str): The name of the participant's team (if applicable).
            invite_link (str): The invite link for the participant (To invite other team members).
            body_text (Optional[str]): The plain text version of the email body (optional).
            body_html (Optional[str]): The HTML version of the email body (optional).
        """

    @abstractmethod
    async def send_participant_confirmation_email(
        self,
        receiver: str,
        subject: str,
        participant: str,
        team_name: str,
        confirmation_link: str,
        body_text: Optional[str] = None,
        body_html: Optional[str] = None,
    ) -> None:
        """
        Sends a confirmation email to a participant, informing them that they need to confirm their application
        to the event. The email will include details such as the participant's name, team name (if applicable),
        and a verification link for confirming their participation. Both text and HTML versions of the email body
        can be provided.

        Parameters:
            receiver (str): The email address of the recipient.
            subject (str): The subject line of the email.
            participant (str): The name of the participant.
            team_name (str): The name of the participant's team (if applicable).
            confirmation_link (str): The verification link for the participant.
            body_text (Optional[str]): The plain text version of the email body (optional).
            body_html (Optional[str]): The HTML version of the email body (optional).
        """
