#!/bin/bash

echo "🚀 Starting environment setup..."

OS_TYPE="$(uname)"
SHELL_CONFIG="$HOME/.bashrc"
[[ "$SHELL" == */zsh ]] && SHELL_CONFIG="$HOME/.zshrc"

# --- 1. Linux / WSL2 Block (Ubuntu-based) ---
if [[ "$OS_TYPE" == "Linux" ]]; then
    echo "🐧 Detected Linux/WSL2. Bundling system installations..."

    # 1a. Add External Repositories (Gum & Node)
    sudo mkdir -p /etc/apt/keyrings
    curl -fsSL https://repo.charm.sh/apt/gpg.key | sudo gpg --dearmor -o /etc/apt/keyrings/charm.gpg
    echo "deb [signed-by=/etc/apt/keyrings/charm.gpg] https://repo.charm.sh/apt/ * *" | sudo tee /etc/apt/sources.list.d/charm.list
    curl -fsSL https://deb.nodesource.com/setup_20.x | sudo -E bash -

    # 1b. Install everything in one apt command
    sudo apt-get update && sudo apt-get install -y \
        make build-essential libssl-dev zlib1g-dev libbz2-dev \
        libreadline-dev libsqlite3-dev wget curl git libffi-dev \
        liblzma-dev tk-dev libncursesw5-dev xz-utils gum nodejs

    # 1c. Install User-space tools (Pyenv & Poetry)
    [[ ! -d "$HOME/.pyenv" ]] && curl https://pyenv.run | bash
    [[ ! -f "$HOME/.local/share/pypoetry" ]] && curl -sSL https://install.python-poetry.org | python3 -

# --- 2. MacOS Block ---
elif [[ "$OS_TYPE" == "Darwin" ]]; then
    echo "🍎 Detected macOS. Using Homebrew..."
    if ! command -v brew &> /dev/null; then
        /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
    fi
    brew install gum pyenv poetry node
fi
# --- 3. Cross-Platform Configuration (Applies to both) ---

SHELL_CONFIG="$HOME/.bashrc"
[[ "$SHELL" == */zsh ]] && SHELL_CONFIG="$HOME/.zshrc"

# Ensure PATHs are in the config file
sed -i '' '/pyenv/d' "$SHELL_CONFIG" 2>/dev/null || true # Cleanup old entries on Mac
echo 'export PYENV_ROOT="$HOME/.pyenv"' >> "$SHELL_CONFIG"
echo 'export PATH="$PYENV_ROOT/bin:$HOME/.local/bin:$PATH"' >> "$SHELL_CONFIG"
echo 'eval "$(pyenv init -)"' >> "$SHELL_CONFIG"

# Activate for the current session
export PYENV_ROOT="$HOME/.pyenv"
export PATH="$PYENV_ROOT/bin:$HOME/.local/bin:$PATH"
eval "$(pyenv init -)"

# --- 4. Python Setup ---
echo "🐍 Installing Python 3.12.9..."
pyenv install 3.12.9 -s
pyenv global 3.12.9

# --- 5. Project Dependency Installation ---
echo "📦 Installing root dependencies..."
npm install

echo "📂 Navigating to Python API directory: ./services/py-api"
if [ -d "services/py-api" ]; then
    cd services/py-api
    poetry config virtualenvs.create true
    poetry config virtualenvs.in-project true
    poetry install
    cd ../..
else
    echo "⚠️  Warning: services/py-api not found. Skipping poetry install."
fi

# --- 6. Health Check ---
echo -e "\n🩺 --- HEALTH CHECK ---"

# Node Check
if command -v node &> /dev/null; then
    echo "✅ Node: $(node -v) at $(which node)"
else
    echo "❌ Node: Not found"
fi

# Python Check
ACTIVE_PY=$(python --version 2>&1)
if [[ "$ACTIVE_PY" == *"3.12.9"* ]]; then
    echo "✅ Python: $ACTIVE_PY (Correct via pyenv)"
else
    echo "❌ Python: Expected 3.12.9, found $ACTIVE_PY"
fi

# Poetry Check
if command -v poetry &> /dev/null; then
    echo "✅ Poetry: $(poetry --version)"
else
    echo "❌ Poetry: Not found"
fi

# Virtualenv Check
if [ -d "services/py-api/.venv" ]; then
    echo "✅ Venv: Created locally in services/py-api/.venv"
else
    echo "❌ Venv: Local .venv folder not found in services/py-api/"
fi

echo -e "-----------------------\n"
echo "🎉 Setup complete! Run 'source $SHELL_CONFIG' to finish."
