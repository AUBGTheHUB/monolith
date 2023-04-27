#!/bin/sh

if [ "$1" != "--post" ]; then
    sudo apt install curl
    sudo apt install make
    curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/master/install.sh | bash

    echo "NVM_DIR=\"$HOME/.nvm\"" >> ~/.bashrc
    echo "[ -s \"\$NVM_DIR/nvm.sh\" ] && \. \"\$NVM_DIR/nvm.sh\"" >> ~/.bashrc
    echo "[ -s \"\$NVM_DIR/bash_completion\" ] && \. \"\$NVM_DIR/bash_completion\"" >> ~/.bashrc

    wget -O go.tar.gz https://go.dev/dl/go1.19.1.linux-amd64.tar.gz

    rm -rf /usr/local/go && tar -C $HOME -xzf go.tar.gz
    rm -rf go.tar.gz

    echo "export PATH=\$PATH:/$HOME/go/bin" >> ~/.bashrc

    git clone git@github.com:AUBGTheHUB/monolith.git $HOME/go/src/monolith
    chsh -s /bin/bash
    
    echo "REBOOT WSL!"
    exec $SHELL

else
    sudo apt install make
    . ~/.nvm/nvm.sh
    nvm install --lts
    cd $HOME/go/src/monolith

    make install-hooks
    make install-web
    make install-env
    make install-code-plugins
    make install-python

    echo "alias spa=\"cd ${PWD}\"" >> $HOME/.bashrc
fi
