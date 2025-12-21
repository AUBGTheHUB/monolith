FROM mcr.microsoft.com/devcontainers/base:jammy

# Set global environments immediately
# We add Pyenv and local bin (for pipx/poetry) to the path
ENV PYENV_ROOT="/home/vscode/.pyenv" \
    NVM_DIR="/home/vscode/.nvm" \
    PATH="/home/vscode/.pyenv/shims:/home/vscode/.pyenv/bin:/home/vscode/.local/bin:$PATH"

# --- ROOT OPERATIONS ---
# Run all system installs as root to avoid 'sudo' overhead
USER root

# 1. Add Charm (Gum) Keyring & Sources
# We do this before the main apt-get install so gum can be installed in the same transaction
RUN mkdir -p /etc/apt/keyrings \
    && curl -fsSL https://repo.charm.sh/apt/gpg.key | gpg --dearmor -o /etc/apt/keyrings/charm.gpg \
    && echo "deb [signed-by=/etc/apt/keyrings/charm.gpg] https://repo.charm.sh/apt/ * *" | tee /etc/apt/sources.list.d/charm.list

# 2. Install System Dependencies & Gum
# OPTIMIZATION: Use cache mounts to speed up apt-get on rebuilds
RUN --mount=type=cache,target=/var/cache/apt,sharing=locked \
    --mount=type=cache,target=/var/lib/apt/lists,sharing=locked \
    apt-get update && apt-get install -y --no-install-recommends \
    make build-essential zlib1g-dev libssl-dev libbz2-dev \
    libreadline-dev libsqlite3-dev curl libncursesw5-dev xz-utils \
    tk-dev libxml2-dev libxmlsec1-dev libffi-dev liblzma-dev \
    pipx git gum \
    && chown -R vscode:vscode /home/vscode

# --- USER OPERATIONS ---
USER vscode
WORKDIR /home/vscode/workspaces

# --- PYENV CONFIGURATION ---
# Clone and Install Python 3.12.9
RUN git clone https://github.com/pyenv/pyenv.git ~/.pyenv \
    && eval "$(pyenv init -)" \
    && pyenv install 3.12.9 \
    && pyenv global 3.12.9

# --- NVM CONFIGURATION ---
# Install NVM and Node
RUN mkdir -p $NVM_DIR \
    && curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.40.1/install.sh | bash \
    && . $NVM_DIR/nvm.sh \
    && nvm install --lts \
    # Add NVM load to bashrc for interactive shells
    && echo 'export NVM_DIR="/home/vscode/.nvm"' >> ~/.bashrc \
    && echo '[ -s "$NVM_DIR/nvm.sh" ] && . "$NVM_DIR/nvm.sh"' >> ~/.bashrc

# --- POETRY CONFIGURATION ---
# pipx is already installed in the root step.
# PATH is already set in the ENV block at the top.
RUN pipx install poetry