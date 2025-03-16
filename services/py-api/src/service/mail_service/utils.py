from os.path import dirname, join


def load_email_registration_confirmation_html_template(
    participant_name: str, team_name: str | None, invite_link: str | None
) -> str:
    base_dir = dirname(__file__)
    template_path = join(base_dir, "email_templates", "email-registration-confirmation.html")

    with open(template_path, "r", encoding="utf-8") as file:
        email_template = file.read()

    # Construct the participant greeting based on the registration case
    participant_greeting = f"{participant_name}" if team_name is None else f"{participant_name} from team {team_name}"

    # The invite_link_statement is constructed similarly
    invite_link_statement = "" if invite_link is None else f"Invite your teammates using this link: {invite_link}"

    return email_template.format(
        participant_greeting=participant_greeting,
        invite_link_statement=invite_link_statement,
    )


def load_email_verify_participant_html_template(
    participant_name: str, team_name: str | None, verification_link: str
) -> str:
    base_dir = dirname(__file__)
    template_path = join(base_dir, "email_templates", "email-verify-participant.html")
    with open(template_path, "r", encoding="utf-8") as file:
        email_template = file.read()

    # Construct the participant greeting based on the registration case
    participant_greeting = f"{participant_name}" if team_name is None else f"{participant_name} from team {team_name}"

    return email_template.format(
        participant_greeting=participant_greeting,
        verification_link=verification_link,
    )
