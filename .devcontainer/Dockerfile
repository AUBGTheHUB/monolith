FROM mcr.microsoft.com/devcontainers/base:jammy

# --- GLOBAL ENVIRONMENT CONFIGURATION ---
# Install tools to /usr/local/share so they survive the home directory volume mount
ENV PYENV_ROOT="/usr/local/share/pyenv" \
    NVM_DIR="/usr/local/share/nvm" \
    PIPX_HOME="/usr/local/share/pipx" \
    PIPX_BIN_DIR="/usr/local/bin" \
    PATH="/usr/local/share/pyenv/shims:/usr/local/share/pyenv/bin:/usr/local/bin:$PATH"

# 1. SETUP THIRD-PARTY REPOSITORIES (CHARM/GUM)
RUN mkdir -p /etc/apt/keyrings \
    && curl -fsSL https://repo.charm.sh/apt/gpg.key | gpg --dearmor -o /etc/apt/keyrings/charm.gpg \
    && echo "deb [signed-by=/etc/apt/keyrings/charm.gpg] https://repo.charm.sh/apt/ * *" | tee /etc/apt/sources.list.d/charm.list

# 2. INSTALL SYSTEM COMPILERS & UTILITIES
RUN --mount=type=cache,target=/var/cache/apt,sharing=locked \
    --mount=type=cache,target=/var/lib/apt/lists,sharing=locked \
    apt-get update && apt-get install -y --no-install-recommends \
    make build-essential zlib1g-dev libssl-dev libbz2-dev \
    libreadline-dev libsqlite3-dev curl libncursesw5-dev xz-utils \
    tk-dev libxml2-dev libxmlsec1-dev libffi-dev liblzma-dev \
    pipx git gum

# --- PYENV SETUP (Global) ---
# Clone to global directory and set permissions for vscode user (UID 1000)
RUN git clone https://github.com/pyenv/pyenv.git $PYENV_ROOT \
    && cd $PYENV_ROOT && src/configure && make -C src \
    && chmod -R g+rwx $PYENV_ROOT \
    && chown -R vscode:vscode $PYENV_ROOT

# Install Python 3.12.9 globally using pyenv
RUN $PYENV_ROOT/bin/pyenv install 3.12.9 \
    && $PYENV_ROOT/bin/pyenv global 3.12.9

# --- NVM (NODE) SETUP (Global) ---
# Create directory, install NVM, and fix permissions
RUN mkdir -p $NVM_DIR \
    && curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.40.1/install.sh | bash \
    && . $NVM_DIR/nvm.sh \
    && nvm install --lts \
    && chmod -R g+rwx $NVM_DIR \
    && chown -R vscode:vscode $NVM_DIR

# --- POETRY SETUP (Global via pipx) ---
# PIPX_HOME and PIPX_BIN_DIR are set in ENV above to global locations
RUN pipx install poetry

# --- FINAL USER SWITCH ---
USER vscode
WORKDIR /home/vscode/workspaces

# Ensure .bashrc loads the global configurations
RUN echo 'export PYENV_ROOT="/usr/local/share/pyenv"' >> /home/vscode/.bashrc \
    && echo 'export PATH="$PYENV_ROOT/bin:$PATH"' >> /home/vscode/.bashrc \
    && echo 'eval "$(pyenv init -)"' >> /home/vscode/.bashrc \
    && echo 'export NVM_DIR="/usr/local/share/nvm"' >> /home/vscode/.bashrc \
    && echo '[ -s "$NVM_DIR/nvm.sh" ] && . "$NVM_DIR/nvm.sh"' >> /home/vscode/.bashrc