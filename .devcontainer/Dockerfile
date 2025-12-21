FROM mcr.microsoft.com/devcontainers/base:jammy

SHELL ["/bin/bash", "-c"]
USER root
WORKDIR /home/vscode/workspaces
RUN chown -R vscode:vscode /home/vscode/workspaces

# Install System Dependencies
RUN apt-get update && apt-get install -y \
    make wget build-essential zlib1g-dev libssl-dev libbz2-dev \
    libreadline-dev libsqlite3-dev curl libncursesw5-dev xz-utils \
    tk-dev libxml2-dev libxmlsec1-dev libffi-dev liblzma-dev \
    pipx git

# --- GO CONFIGURATION ---
# We set the PATH variable in the Image Metadata.
# Docker loads this automatically for every command. No sourcing needed.
USER vscode
ENV PATH="$PATH:/home/vscode/go/bin"

RUN wget -O go.tar.gz https://go.dev/dl/go1.23.1.linux-amd64.tar.gz \
    && tar -C /home/vscode/workspaces -xzf go.tar.gz \
    && rm -fr ./go.tar.gz

# --- PYENV CONFIGURATION ---
# Set these variables globally so pyenv works immediately
ENV PYENV_ROOT="/home/vscode/.pyenv"
ENV PATH="$PYENV_ROOT/bin:$PATH"

RUN git clone https://github.com/pyenv/pyenv.git ~/.pyenv

# Initialize and install Python in one go
# We use eval here just for this specific RUN command
RUN eval "$(pyenv init -)" \
    && pyenv install 3.12.9 \
    && pyenv global 3.12.9

# --- NVM CONFIGURATION (The Hybrid Way) ---
ENV NVM_DIR="/home/vscode/.nvm"
ENV PATH="$NVM_DIR/bin:$PATH"
# Install NVM and Node
# Since NVM is a shell function, we source it manually JUST for this command using "&& ."
RUN mkdir -p $NVM_DIR \
    && wget -qO- https://raw.githubusercontent.com/nvm-sh/nvm/v0.40.1/install.sh | bash \
    && . $NVM_DIR/nvm.sh \
    && nvm install --lts

## We still add it to bashrc so it's there when YOU log in manually later
#RUN echo 'export NVM_DIR="/home/vscode/.nvm"' >> /home/vscode/.bashrc \
#    && echo '[ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh"' >> /home/vscode/.bashrc

# --- POETRY ---
RUN pipx install poetry
