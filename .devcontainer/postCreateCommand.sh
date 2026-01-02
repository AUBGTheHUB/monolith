#!/bin/bash

# --- SHELL ENVIRONMENT---
# This script runs in a "non-interactive" shell, as it is executed by Docker.
# Unlike your normal terminal, non-interactive shells do not load ~/.bashrc.
# Without these lines, the script cannot find 'npm', 'node', or 'python'.
# We must manually "source" (load) the NVM and Pyenv scripts here so the commands below work.

# Load NVM (Node Version Manager)
export NVM_DIR="/usr/local/share/nvm"
[ -s "$NVM_DIR/nvm.sh" ] && . "$NVM_DIR/nvm.sh"

# Load Pyenv (Python Version Manager)
export PYENV_ROOT="/usr/local/share/pyenv"
export PATH="$PYENV_ROOT/bin:$HOME/.local/bin:$PATH"
eval "$(pyenv init -)"


# Docker "mounts" the code from Windows/Mac into Linux.
# Linux sees these files as owned by a generic ID, but the container user is different.
# Git's security features block commands in folders with "dubious ownership" to prevent attacks.
# This command forces Git to trust this specific directory so you can commit/push code.
git config --global --add safe.directory /home/vscode/workspaces/monolith

# --- PROJECT SETUP ---
# Install global JavaScript tools (like Prettier, ESLint) defined in the root package.json
npm install

# Set up Husky (Git Hooks). This ensures linters run automatically when you commit code.
npm run prepare

# Enables the .venv folder to appear inside the project - currently ./services/py_api - poetry installs all the deps on this
poetry config virtualenvs.in-project true
# This makes sure we are using the current python version configured by pyenv. https://python-poetry.org/docs/managing-environments/
poetry config virtualenvs.prefer-active-python true

# Installs the node_modules inside ./services/web
make install-web

# Installs the backend dependencies
cd ./services/py-api/
poetry install
