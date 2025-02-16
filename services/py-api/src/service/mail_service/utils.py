from os.path import dirname, join


def load_email_registration_confirmation_html_template(
    participant_name: str, team_name: str | None, invite_link: str | None
) -> str:
    base_dir = dirname(__file__)
    template_path = join(base_dir, "email_templates", "email-registration-confirmation.html")

    with open(template_path, "r", encoding="utf-8") as file:
        email_template = file.read()

    title_team = "block" if team_name else "none"
    title_no_team = "none" if team_name else "block"
    invite_link_visibility = "block" if invite_link else "none"

    return email_template.format(
        participant_name=participant_name,
        team_name=team_name,
        invite_link=invite_link,
        title_team=title_team,
        title_no_team=title_no_team,
        invite_link_visibility=invite_link_visibility,
    )


def load_email_verify_participant_html_template(
    participant_name: str, team_name: str | None, verification_link: str
) -> str:
    base_dir = dirname(__file__)
    template_path = join(base_dir, "email_templates", "email-verify-participant.html")
    with open(template_path, "r", encoding="utf-8") as file:
        email_template = file.read()

    title_team = "block" if team_name else "none"
    title_no_team = "none" if team_name else "block"

    return email_template.format(
        participant_name=participant_name,
        team_name=team_name,
        verification_link=verification_link,
        title_team=title_team,
        title_no_team=title_no_team,
    )
