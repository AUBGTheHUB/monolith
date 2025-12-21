#!/bin/bash

# Manually load NVM because non-interactive shells ignore .bashrc
export NVM_DIR="$HOME/.nvm"
[ -s "$NVM_DIR/nvm.sh" ] && . "$NVM_DIR/nvm.sh"

export PYENV_ROOT="$HOME/.pyenv"
export PATH="$PYENV_ROOT/bin:$PATH"
if command -v pyenv 1>/dev/null 2>&1; then
  eval "$(pyenv init -)"
fi

#linux devcontainer ownership workaround (when ran as root ownership of files is not $USER):
git config --global --add safe.directory /workspaces/monolith

# Installs the node_modules in the project root
npm install

# Installs husky - pre-commit manager for .js, .css, .html
npm run prepare

# Enables the .venv folder to appear inside the project - currently ./services/py_api - poetry installs all the deps on this
# This makes sure we are using the current python version configured by pyenv. https://python-poetry.org/docs/managing-environments/
poetry config virtualenvs.create true
poetry config virtualenvs.in-project true

# Installs the node_modules inside ./services/web
make install-web

# Installs the backend dependencies
cd ./services/py-api/
poetry install
