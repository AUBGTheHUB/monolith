# Installs the node_modules in the project root
npm install
# Installs husky - pre-commit manager for .js, .css, .html
npm run prepare
# Installs gum - helps with creating interactive terminal user interfaces
make install-gum
# Enables the .venv folder to appear inside the project - currently ./services/py_api - poetry installs all the deps on this
poetry config virtualenvs.in-project true
# This makes sure we are using the current python version configured by pyenv. https://python-poetry.org/docs/managing-environments/
poetry config virtualenvs.prefer-active-python true
# Installs the node_modules inside ./services/web
make install-web
# Installs the backend dependencies
cd ./services/py-api/
poetry install

#git configuration:
git config --global --add safe.directory /IdeaProjects/monolith
