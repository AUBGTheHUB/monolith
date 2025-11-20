#
#FROM --platform=linux/amd64 mcr.microsoft.com/devcontainers/base:jammy
#
##Set bash as default shell:
#SHELL ["/bin/bash", "--login", "-i", "-c"]
#
#USER root
#WORKDIR /workspaces
#
#RUN apt -y update
#RUN apt install -y make wget
#
## Initialize nvm
#RUN wget -qO- https://raw.githubusercontent.com/nvm-sh/nvm/v0.40.1/install.sh | bash
#RUN source /root/.bashrc && nvm install --lts
#
## Initialize go
#RUN wget -O go.tar.gz https://go.dev/dl/go1.23.1.linux-amd64.tar.gz
#RUN rm -rf /usr/local/go && tar -C $HOME -xzf go.tar.gz
#RUN rm -rf go.tar.gz
#RUN echo "export PATH=$PATH:$HOME/go/bin" >> $HOME/.bashrc
#
## Install pyenv and its dependencies
#RUN apt install -y \
#    build-essential \
#    zlib1g-dev \
#    libssl-dev \
#    libbz2-dev \
#    libreadline-dev \
#    libsqlite3-dev \
#    curl \
#    libncursesw5-dev \
#    xz-utils \
#    tk-dev \
#    libxml2-dev \
#    libxmlsec1-dev \
#    libffi-dev \
#    liblzma-dev
#RUN git clone https://github.com/pyenv/pyenv.git ~/.pyenv
#RUN echo 'export PYENV_ROOT="$HOME/.pyenv"' >> ~/.bashrc
#RUN echo 'command -v pyenv >/dev/null || export PATH="$PYENV_ROOT/bin:$PATH"' >> ~/.bashrc
#RUN echo 'eval "$(pyenv init -)"' >> ~/.bashrc
#RUN source ~/.bashrc
#
## Install python and set the version globally
#RUN pyenv install 3.12.9
#RUN pyenv global 3.12.9
#
## Install pipx and poetry
#RUN apt install -y pipx
#RUN pipx ensurepath
#RUN pipx install poetry

FROM mcr.microsoft.com/devcontainers/base:jammy

USER root
WORKDIR /workspaces

# Install System Dependencies
RUN apt-get update && apt-get install -y \
    make wget build-essential zlib1g-dev libssl-dev libbz2-dev \
    libreadline-dev libsqlite3-dev curl libncursesw5-dev xz-utils \
    tk-dev libxml2-dev libxmlsec1-dev libffi-dev liblzma-dev \
    pipx git

# --- GO CONFIGURATION ---
# We set the PATH variable in the Image Metadata.
# Docker loads this automatically for every command. No sourcing needed.
ENV PATH="$PATH:/root/go/bin"

RUN wget -O go.tar.gz https://go.dev/dl/go1.23.1.linux-amd64.tar.gz \
    && rm -rf /usr/local/go && tar -C /root -xzf go.tar.gz \
    && rm go.tar.gz

# --- PYENV CONFIGURATION ---
# Set these variables globally so pyenv works immediately
ENV PYENV_ROOT="/root/.pyenv"
ENV PATH="$PYENV_ROOT/bin:$PATH"

RUN git clone https://github.com/pyenv/pyenv.git ~/.pyenv

# Initialize and install Python in one go
# We use eval here just for this specific RUN command
RUN eval "$(pyenv init -)" \
    && pyenv install 3.12.9 \
    && pyenv global 3.12.9

# --- NVM CONFIGURATION (The Hybrid Way) ---
ENV NVM_DIR="/root/.nvm"

# Install NVM and Node
# Since NVM is a shell function, we source it manually JUST for this command using "&& ."
RUN mkdir -p $NVM_DIR \
    && wget -qO- https://raw.githubusercontent.com/nvm-sh/nvm/v0.40.1/install.sh | bash \
    && . $NVM_DIR/nvm.sh \
    && nvm install --lts

# We still add it to bashrc so it's there when YOU log in manually later
RUN echo 'export NVM_DIR="/root/.nvm"' >> /root/.bashrc \
    && echo '[ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh"' >> /root/.bashrc

# --- POETRY ---
RUN pipx ensurepath && pipx install poetry
