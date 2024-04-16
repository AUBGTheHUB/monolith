from enum import Enum
from typing import Any, Dict

from py_api.functionality.hackathon.jwt_base import JWTFunctionality
from py_api.services.mailer import send_mail


class TemplateNames(Enum):
    VERIFICATION = "verification"
    CONFIRMATION = "confirmation"


class MailingFunctionality:
    TEMPLATES = {
        "verification": {
            "subject": "Verify your email",
            "template_path": 'resources/email_templates/email-verify-participant.html',
        },
        "confirmation": {
            "subject": "Welcome to HackAUBG 6.0",
            "template_path": 'resources/email_templates/email-participant.html',
        },
    }

    @classmethod
    def get_template(cls, template_name: str) -> Dict[str, Any]:
        return cls.TEMPLATES[template_name]

    @classmethod
    def generate_email_body(
            cls, template_path: str, participant_name: str, has_invite_link: bool, jwt_token: str, is_admin: bool = False,
            team_name: str | None = None,
    ) -> str:
        email_link = JWTFunctionality.get_email_link(
            jwt_token=jwt_token, for_frontend=True, is_invite=has_invite_link,
        )

        html_content = cls.read_html_template(template_path)
        html_content = html_content.replace("{verifyLink}", email_link)
        html_content = html_content.replace(
            "{participantName}", participant_name,
        )

        if team_name:
            html_content = (
                html_content
                .replace("{title_no_team}", "none")
                .replace("{title_team}", "inital")
                .replace("{inviteLink}", email_link)
                .replace("{teamName}", team_name)
            )

            if is_admin is False:
                html_content = html_content.replace(
                    "{inviteLinkVisibility}", "none",
                )
            else:
                html_content = html_content.replace(
                    "{inviteLinkVisibility}", "block",
                )
        else:
            html_content = (
                html_content
                .replace("{title_no_team}", "inital")
                .replace("{title_team}", "none")
                .replace("{inviteLinkVisibility}", "none")
            )

        return html_content

    @classmethod
    async def send_verification_email(
            cls, email: str, jwt_token: str, participant_name: str, team_name: str | None = None,
    ) -> None:
        template = cls.get_template(TemplateNames.VERIFICATION.value)

        body_html = cls.generate_email_body(
            template["template_path"], jwt_token=jwt_token, team_name=team_name,
            participant_name=participant_name, has_invite_link=False,
        )

        await send_mail(email, template["subject"], body_html)

    @classmethod
    async def send_confirmation_email(
            cls, email: str, jwt_token: str, participant_name: str, team_name: str | None = None,
            is_admin: bool = False,
    ) -> None:
        template = cls.get_template(TemplateNames.CONFIRMATION.value)

        body_html = cls.generate_email_body(
            template["template_path"], jwt_token=jwt_token, team_name=team_name,
            participant_name=participant_name, has_invite_link=True, is_admin=is_admin,
        )

        await send_mail(email, template["subject"], body_html)

    @classmethod
    def read_html_template(cls, template_path: str) -> str:
        with open(template_path, 'r') as file:
            return file.read()
