
FROM --platform=linux/amd64 mcr.microsoft.com/devcontainers/base:jammy

#Set bash as default shell:
SHELL ["/bin/bash", "--login", "-i", "-c"]

USER root
WORKDIR /workspaces

RUN apt -y update
RUN apt install -y make wget

# Initialize nvm
RUN wget -qO- https://raw.githubusercontent.com/nvm-sh/nvm/v0.40.1/install.sh | bash
RUN source /root/.bashrc && nvm install --lts

# Initialize go
RUN wget -O go.tar.gz https://go.dev/dl/go1.23.1.linux-amd64.tar.gz
RUN rm -rf /usr/local/go && tar -C $HOME -xzf go.tar.gz
RUN rm -rf go.tar.gz
RUN echo "export PATH=$PATH:$HOME/go/bin" >> $HOME/.bashrc

# Install pyenv and its dependencies
RUN apt install -y \
    build-essential \
    zlib1g-dev \
    libssl-dev \
    libbz2-dev \
    libreadline-dev \
    libsqlite3-dev \
    curl \
    libncursesw5-dev \
    xz-utils \
    tk-dev \
    libxml2-dev \
    libxmlsec1-dev \
    libffi-dev \
    liblzma-dev
RUN git clone https://github.com/pyenv/pyenv.git ~/.pyenv
RUN echo 'export PYENV_ROOT="$HOME/.pyenv"' >> ~/.bashrc
RUN echo 'command -v pyenv >/dev/null || export PATH="$PYENV_ROOT/bin:$PATH"' >> ~/.bashrc
RUN echo 'eval "$(pyenv init -)"' >> ~/.bashrc
RUN source ~/.bashrc

# Install python and set the version globally
RUN pyenv install 3.12.9
RUN pyenv global 3.12.9

# Install pipx and poetry
RUN apt install -y pipx
RUN pipx ensurepath
RUN pipx install poetry
