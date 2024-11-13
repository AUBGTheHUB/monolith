def load_email_participant_html_template(participant_name, team_name, invite_link):
    if not participant_name:
        raise ValueError("participant_name must be provided.")

    template_path = "email_templates/email-participant.html"

    with open(template_path, "r", encoding="utf-8") as file:
        email_template = file.read()

    title_team = "block" if team_name else "none"
    title_no_team = "none" if team_name else "block"
    invite_link_visibility = "block" if invite_link else "none"

    return email_template.format(
        participantName=participant_name,
        teamName=team_name,
        inviteLink=invite_link,
        title_team=title_team,
        title_no_team=title_no_team,
        inviteLinkVisibility=invite_link_visibility,
    )


def load_email_verify_participant_html_template(participant_name, team_name, confirmation_link) -> None:
    if not participant_name or not confirmation_link:
        raise ValueError("Both participant_name and verify_link must be provided.")

    template_path = "email_templates/email-verify-participant.html"

    with open(template_path, "r", encoding="utf-8") as file:
        email_template = file.read()

    title_team = "block" if team_name else "none"
    title_no_team = "none" if team_name else "block"

    return email_template.format(
        participantName=participant_name,
        teamName=team_name,
        verifyLink=confirmation_link,
        title_team=title_team,
        title_no_team=title_no_team,
    )
