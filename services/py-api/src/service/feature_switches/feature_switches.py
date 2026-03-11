from typing import Final

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
