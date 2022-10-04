#!/bin/sh

if [ "$1" != "--post" ]; then
    sudo apt install curl
    curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/master/install.sh | bash

    echo "NVM_DIR=\"$HOME/.nvm\"" >> ~/.bashrc
    echo "[ -s \"\$NVM_DIR/nvm.sh\" ] && \. \"\$NVM_DIR/nvm.sh\"" >> ~/.bashrc
    echo "[ -s \"\$NVM_DIR/bash_completion\" ] && \. \"\$NVM_DIR/bash_completion\"" >> ~/.bashrc

    wget -O go.tar.gz https://go.dev/dl/go1.19.1.linux-amd64.tar.gz

    rm -rf /usr/local/go && tar -C $HOME -xzf go.tar.gz
    rm -rf go.tar.gz

    echo "export PATH=\$PATH:/$HOME/go/bin" >> ~/.bashrc

    git clone git@github.com:AUBGTheHUB/spa-website-2022.git $HOME/go/src/spa-website-2022
    chsh -s /bin/bash
    
    echo "REBOOT WSL!"
    exec $SHELL

else
    sudo apt install make
    . ~/.nvm/nvm.sh
    nvm install --lts
    cd $HOME/go/src/spa-website-2022

    make install-hooks
    make install-web

    echo "alias spa=\"cd ${PWD}\"" >> $HOME/.bashrc
fi
