#!/bin/sh

yes | sudo apt install docker-compose
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/master/install.sh | bash

wget -O go.tar.gz https://go.dev/dl/go1.19.1.linux-amd64.tar.gz

rm -rf /usr/local/go && tar -C $HOME -xzf go.tar.gz
rm -rf go.tar.gz

echo "export PATH=\$PATH:/$HOME/go/bin" >> ~/.bashrc

git clone https://github.com/AUBGTheHUB/spa-website-2022.git $HOME/go/src/spa-website-2022

exec $SHELL
