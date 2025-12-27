from typing import Final

MAX_NUMBER_OF_TEAM_MEMBERS: Final[int] = 6
"""Constraint for max number of participants in a given team"""

MAX_NUMBER_OF_VERIFIED_TEAMS_IN_HACKATHON: Final[int] = 16
"""Constraint for max number of verified teams in the hackathon. A team is verified when the admin participant who
created the team, verified their email. This const also includes the random teams, which are automatically created
and marked as verified, once the hackathon registration closes"""

REG_ADMIN_AND_RANDOM_SWITCH: Final[str] = "isRegTeamsFull"
"""This switch toggles the registration for the admin and random participants. It will disable the application
form in the frontend when it is set to `true` and it will enable it when it is set to `false`. If somebody tries to
register using the API endpoint they will get the `Max hackathon capacity has been reached` message.
"""

REG_ALL_PARTICIPANTS_SWITCH: Final[str] = "RegSwitch"
"""This switch toggles the registration for the all participants. It will disable the application for both
the front-end interface and the API endpoint. If somebody tries to register through the API endpoint they will get
the `Registration is closed` message.
"""

RATE_LIMIT_SECONDS: Final[int] = 90
"""Number of seconds before a participant is allowed to resend their verification email, if they didn't get one."""

PARTICIPANTS_VERIFICATION_ROUTE = "/hackathon/verification"
"""The front-end route for email verification"""

PARTICIPANTS_REGISTRATION_ROUTE = "/hackathon/registration"
"""The front-end route for hackathon registration"""

FRONTEND_PORT = 3000
"""The port on which the frontend is running"""