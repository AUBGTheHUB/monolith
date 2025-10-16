FROM --platform=linux/amd64 mcr.microsoft.com/devcontainers/base:jammy

# Use bash as the shell
SHELL ["/bin/bash", "--login", "-i", "-c"]

# ------------------------------------------------------------
# Root setup: install system dependencies only
# ------------------------------------------------------------
USER root

RUN apt-get update -y && apt-get install -y --no-install-recommends \
    make wget curl git build-essential \
    zlib1g-dev libssl-dev libbz2-dev libreadline-dev libsqlite3-dev \
    libncursesw5-dev xz-utils tk-dev libxml2-dev libxmlsec1-dev \
    libffi-dev liblzma-dev ca-certificates \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# ------------------------------------------------------------
# Switch to vscode user for development environment setup
# ------------------------------------------------------------
USER vscode
WORKDIR /home/vscode

# Ensure proper ownership for installed tools
ENV HOME=/home/vscode
ENV NVM_DIR="$HOME/.nvm"
ENV PYENV_ROOT="$HOME/.pyenv"
ENV PATH="$PYENV_ROOT/bin:$NVM_DIR/versions/node/$(bash -lc 'nvm version --lts')/bin:$HOME/go/bin:$PATH"

# ------------------------------------------------------------
# Install NVM and latest LTS Node.js
# ------------------------------------------------------------
RUN curl -fsSL https://raw.githubusercontent.com/nvm-sh/nvm/v0.40.1/install.sh | bash && \
    source "$NVM_DIR/nvm.sh" && \
    nvm install --lts && \
    nvm alias default lts/* && \
    echo 'export NVM_DIR="$HOME/.nvm"' >> ~/.bashrc && \
    echo '[ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh"' >> ~/.bashrc

# ------------------------------------------------------------
# Install Go (1.23.1)
# ------------------------------------------------------------
RUN wget -O /tmp/go.tar.gz https://go.dev/dl/go1.23.1.linux-amd64.tar.gz && \
    tar -C "$HOME" -xzf /tmp/go.tar.gz && rm /tmp/go.tar.gz && \
    echo 'export PATH="$PATH:$HOME/go/bin"' >> ~/.bashrc

# ------------------------------------------------------------
# Install pyenv and Python 3.12.9
# ------------------------------------------------------------
RUN git clone https://github.com/pyenv/pyenv.git "$PYENV_ROOT" && \
    echo 'export PYENV_ROOT="$HOME/.pyenv"' >> ~/.bashrc && \
    echo 'command -v pyenv >/dev/null || export PATH="$PYENV_ROOT/bin:$PATH"' >> ~/.bashrc && \
    echo 'eval "$(pyenv init -)"' >> ~/.bashrc && \
    bash -lc 'pyenv install 3.12.9 && pyenv global 3.12.9'

# ------------------------------------------------------------
# Install pipx and Poetry via pipx
# ------------------------------------------------------------
RUN sudo apt-get update -y && sudo apt-get install -y pipx && \
    pipx ensurepath && \
    bash -lc 'pipx install poetry'

# ------------------------------------------------------------
# Final cleanup and environment
# ------------------------------------------------------------
RUN echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc

WORKDIR /
