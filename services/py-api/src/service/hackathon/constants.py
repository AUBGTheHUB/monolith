from typing import Final

MAX_NUMBER_OF_TEAM_MEMBERS: Final[int] = 6
"""Constraint for max number of participants in a given team"""

MAX_NUMBER_OF_VERIFIED_TEAMS_IN_HACKATHON: Final[int] = 16
"""Constraint for max number of verified teams in the hackathon. A team is verified when the admin participant who
created the team, verified their email. This const also includes the random teams, which are automatically created
and marked as verified, once the hackathon registration closes"""

RATE_LIMIT_SECONDS: Final[int] = 90
"""Number of seconds before a participant is allowed to resend their verification email, if they didn't get one."""

PARTICIPANTS_VERIFICATION_ROUTE = "/hackathon/verification"
"""The front-end route for email verification"""

PARTICIPANTS_REGISTRATION_ROUTE = "/hackathon/registration"
"""The front-end route for hackathon registration"""

FRONTEND_PORT = 3000
"""The port on which the frontend is running"""
