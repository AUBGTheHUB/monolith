FROM mcr.microsoft.com/devcontainers/base:jammy

# --- GLOBAL ENVIRONMENT CONFIGURATION ---
# WHY: We define these paths early so they are available to all subsequent commands
# and every interactive terminal session you start.
#
# 1. PYENV_ROOT: Defines where pyenv will live (we want it in the user's home, not root).
# 2. NVM_DIR: Defines where NVM (Node Version Manager) stores its script and node versions.
# 3. PATH Modification (Crucial Order):
# - /home/vscode/.pyenv/shims: MUST be first. This allows pyenv to "intercept" the 'python' command.
# - /home/vscode/.local/bin: This is where 'pipx' puts tools like 'poetry'.
# - $PATH: Appends the existing system paths so standard Linux tools still work.
ENV PYENV_ROOT="/home/vscode/.pyenv" \
    NVM_DIR="/home/vscode/.nvm" \
    PATH="/home/vscode/.pyenv/shims:/home/vscode/.pyenv/bin:/home/vscode/.local/bin:$PATH"


# 1. SETUP THIRD-PARTY REPOSITORIES (CHARM/GUM)
# As [gum](https://github.com/charmbracelet/gum) is not in the standard Ubuntu repositories. We must manually trust
# their GPG key and add their server to our sources list.
#
#    - mkdir: Creates the keyring directory if it's missing.
#    - curl | gpg: Downloads the security key and converts it to a binary format apt understands.
#    - tee: Writes the repository URL to a new file in sources.list.d.
RUN  mkdir -p /etc/apt/keyrings \
    &&  curl -fsSL https://repo.charm.sh/apt/gpg.key | gpg --dearmor -o /etc/apt/keyrings/charm.gpg \
    && echo "deb [signed-by=/etc/apt/keyrings/charm.gpg] https://repo.charm.sh/apt/ * *" | tee /etc/apt/sources.list.d/charm.list

# 2. INSTALL SYSTEM COMPILERS & UTILITIES
# We need these libraries to compile Python from source (via pyenv).
# Without 'libssl-dev' or 'zlib1g-dev', Python would install but fail to run pip or SSL scripts.
# We use [Docker Cache Mounts](https://docs.docker.com/build/cache/optimize/#use-cache-mounts) (--mount=type=cache), as
# 'apt-get update' will download 30MB+ of package lists every time you build. This mount tells Docker to save those
# downloaded lists on our host machine. If we rebuild tomorrow, it reuses the cache instead of downloading again.
RUN --mount=type=cache,target=/var/cache/apt,sharing=locked \
    --mount=type=cache,target=/var/lib/apt/lists,sharing=locked \
    sudo apt-get update && sudo apt-get install -y --no-install-recommends \
    make build-essential zlib1g-dev libssl-dev libbz2-dev \
    libreadline-dev libsqlite3-dev curl libncursesw5-dev xz-utils \
    tk-dev libxml2-dev libxmlsec1-dev libffi-dev liblzma-dev \
    pipx git gum

WORKDIR /home/vscode/workspaces

# --- PYENV SETUP ---
RUN git clone https://github.com/pyenv/pyenv.git /home/vscode/.pyenv \
    && eval "$(pyenv init -)" \
    && pyenv install 3.12.9 \
    && pyenv global 3.12.9

# --- NVM (NODE) SETUP ---
# NVM allows easy switching of Node versions.

# - mkdir: Ensures the target directory exists.
# - install.sh: Official installer script from NVM.
# - . nvm.sh: "Sources" (activates) NVM immediately so we can use it in the next command.
# - .bashrc modification: Appends startup logic to your shell config so NVM works automatically when you open a new
# terminal in VS Code or Pycharm.
RUN mkdir -p $NVM_DIR \
    && curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.40.1/install.sh | bash \
    && . $NVM_DIR/nvm.sh \
    && nvm install --lts \
    && echo 'export NVM_DIR="/home/vscode/.nvm"' >> /home/vscode/.bashrc \
    && echo '[ -s "$NVM_DIR/nvm.sh" ] && . "$NVM_DIR/nvm.sh"' >> /home/vscode/.bashrc

# --- POETRY SETUP ---
# We use 'pipx' to install Poetry. 'pipx' creates a dedicated virtual environment just for Poetry.
# This prevents Poetry's own dependencies from conflicting with your project's dependencies.
RUN pipx install poetry
