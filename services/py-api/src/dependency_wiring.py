"""Here we do our Manual Dependency Wiring (building the object dependency graph)

A graphical representation of this graph looks something like this:

```
                          Repositories -> DbManagers -> DbClients
                         /
Routes -> Handlers -> Services -> OtherServices -> OtherComponents
                         \
                          MailServices ->  MailClients
```

* Note: -> Means accepts (e.g. Routes -> Handlers, means Routes accept handlers as dependencies)
"""

from src.database.db_clients import mongo_db_client_provider
from src.database.db_manager import (
    FEATURE_SWITCH_COLLECTION,
    PARTICIPANTS_COLLECTION,
    TEAMS_COLLECTION,
    mongo_db_manager_provider,
)
from src.database.repository.feature_switch_repository import feature_switch_repo_provider
from src.database.repository.participants_repository import participants_repo_provider
from src.database.repository.teams_repository import teams_repo_provider
from src.database.transaction_manager import mongo_tx_manager_provider

from src.server.handlers.feature_switch_handler import feature_switch_handlers_provider
from src.server.handlers.hackathon_handlers import hackathon_management_handlers_provider
from src.server.handlers.participants_handlers import participant_handlers_provider
from src.server.handlers.utility_hanlders import utility_handlers_provider
from src.server.handlers.verification_handlers import verification_handlers_provider
from src.service.feature_switch_service import feature_switch_service_provider
from src.service.hackathon_service import hackathon_service_provider
from src.service.mail_service.hackathon_mail_service import hackathon_mail_service_provider
from src.service.mail_service.mail_clients.mail_client_factory import mail_client_factory, MailClients
from src.service.participants_registration_service import participant_reg_service_provider
from src.service.participants_verification_service import participant_verification_service_provider
from src.utils import JwtUtility

# ===============================
# Database layer wiring start
# ===============================
_mongo_db_client = mongo_db_client_provider()

_mongo_db_manager = mongo_db_manager_provider(client=_mongo_db_client)
_mongo_tx_manager = mongo_tx_manager_provider(client=_mongo_db_client)

_participants_repo = participants_repo_provider(db_manager=_mongo_db_manager, collection_name=PARTICIPANTS_COLLECTION)
_teams_repo = teams_repo_provider(db_manager=_mongo_db_manager, collection_name=TEAMS_COLLECTION)
_feature_switch_repo_repo = feature_switch_repo_provider(
    db_manager=_mongo_db_manager, collection_name=FEATURE_SWITCH_COLLECTION
)

# ===============================
# Database layer wiring end
# ===============================


# ===============================
# Service layer wiring start
# ===============================

# Could be changed with another client if needed
_mail_client = mail_client_factory(mail_client_type=MailClients.RESEND)
_hackathon_mail_service = hackathon_mail_service_provider(client=_mail_client)

_hackathon_service = hackathon_service_provider(
    p_repo=_participants_repo,
    t_repo=_teams_repo,
    fs_repo=_feature_switch_repo_repo,
    tx_manager=_mongo_tx_manager,
    mail_service=_hackathon_mail_service,
    jwt_utility=JwtUtility(),
)

_participant_reg_service = participant_reg_service_provider(hackathon_service=_hackathon_service)
_participant_verification_service = participant_verification_service_provider(hackathon_service=_hackathon_service)

_feature_switch_service = feature_switch_service_provider(repository=_feature_switch_repo_repo)

# ===============================
# Service layer wiring end
# ===============================

# ===============================
# Handlers layer wiring start
# ===============================

# These Dependencies are public as they are imported in the `routes/routes_dependencies.py`
# For every handler we should create a function to be passed to the ``fastapi.Depends`` in the
# `routes/routes_dependencies.py` file

FEATURE_SWITCH_HANDLERS = feature_switch_handlers_provider(service=_feature_switch_service)
HACKATHON_MANAGEMENT_HANDLERS = hackathon_management_handlers_provider(service=_hackathon_service)
PARTICIPANT_HANDLERS = participant_handlers_provider(service=_participant_reg_service)
UTILITY_HANDLERS = utility_handlers_provider(db_manger=_mongo_db_manager)
VERIFICATION_HANDLERS = verification_handlers_provider(service=_participant_verification_service)

# ===============================
# Handlers layer wiring end
# ===============================
