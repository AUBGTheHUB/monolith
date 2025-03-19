from src.environment import load_env, ENV
from src.logger.logger_factory import configure_app_logger

load_env()

# This should be done before calling LOG = get_logger(), which we use in almost
# every file, in order for the logger to function properly. Otherwise, it uses the default logging config.
configure_app_logger(ENV)

from src.app_factory import create_app
from src.server.server_config import start

# This app is not created in the main guard as uvicorn's run method expects the app passed as an import string to
# enable 'reload' or 'workers'. Also, we need it to create the AsyncTestClient.
app = create_app()

# https://realpython.com/if-name-main-python/
if __name__ == "__main__":
    start()
