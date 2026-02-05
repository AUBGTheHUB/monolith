#!/bin/bash

echo "🚀 Starting environment setup..."

OS_TYPE="$(uname)"
# Detect Linux distribution
DISTRO=$( [ -f /etc/os-release ] && grep -Po '(?<=^ID=)\w+' /etc/os-release || echo "unknown" )
SHELL_CONFIG="$HOME/.bashrc"
[[ "$SHELL" == */zsh ]] && SHELL_CONFIG="$HOME/.zshrc"

# --- 1. Linux / WSL2 Block ---
if [[ "$OS_TYPE" == "Linux" ]]; then

    # 1a. Ubuntu/Debian Logic
    if [[ "$DISTRO" == "ubuntu" || "$DISTRO" == "debian" ]]; then
        echo "🐧 Detected Ubuntu/Debian. Bundling system installations..."
        sudo mkdir -p /etc/apt/keyrings
        curl -fsSL https://repo.charm.sh/apt/gpg.key | sudo gpg --dearmor -o /etc/apt/keyrings/charm.gpg
        echo "deb [signed-by=/etc/apt/keyrings/charm.gpg] https://repo.charm.sh/apt/ * *" | sudo tee /etc/apt/sources.list.d/charm.list
        curl -fsSL https://deb.nodesource.com/setup_20.x | sudo -E bash -

        sudo apt-get update && sudo apt-get install -y \
            make build-essential libssl-dev zlib1g-dev libbz2-dev \
            libreadline-dev libsqlite3-dev wget curl git libffi-dev \
            liblzma-dev tk-dev libncursesw5-dev xz-utils gum nodejs

    # 1b. Fedora Logic
    elif [[ "$DISTRO" == "fedora" ]]; then
        echo "🎩 Detected Fedora. Bundling system installations..."
        # Add Gum repo for Fedora
        echo '[charm]
        name=Charm
        baseurl=https://repo.charm.sh/yum/
        enabled=1
        gpgcheck=1
        gpgkey=https://repo.charm.sh/yum/gpg.key' | sudo tee /etc/yum.repos.d/charm.repo

        sudo dnf groupinstall -y "Development Tools"
        sudo dnf install -y \
            zlib-devel bzip2-devel readline-devel sqlite-devel \
            openssl-devel xz-devel libffi-devel findutils \
            gum nodejs
    fi

    # 1c. User-space tools (Shared Linux)
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

# --- 3. Cross-Platform Configuration ---

# Clean up existing pyenv lines to avoid duplicates (Portable sed logic)
if [[ "$OS_TYPE" == "Darwin" ]]; then
    sed -i '' '/pyenv/d' "$SHELL_CONFIG" 2>/dev/null || true
else
    sed -i '/pyenv/d' "$SHELL_CONFIG" 2>/dev/null || true
fi

{
    echo 'export PYENV_ROOT="$HOME/.pyenv"'
    echo 'export PATH="$PYENV_ROOT/bin:$HOME/.local/bin:$PATH"'
    echo 'eval "$(pyenv init -)"'
} >> "$SHELL_CONFIG"

# Activate for the current session
export PYENV_ROOT="$HOME/.pyenv"
export PATH="$PYENV_ROOT/bin:$HOME/.local/bin:$PATH"
eval "$(pyenv init -)"

# --- 4. Python Setup ---
echo "🐍 Installing Python 3.12.9..."
pyenv install 3.12.9 -s
pyenv global 3.12.9

# --- 5. Project Dependency Installation ---
# [Remaining logic unchanged...]
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
