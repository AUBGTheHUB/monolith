#/bin/sh

/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

brew install nvm

cd ~/Downloads

if [[ $(uname -m) == 'arm64' ]]
then
    curl https://go.dev/dl/go1.19.1.darwin-arm64.pkg
    installer -pkg go1.19.1.darwin-arm64.pkg -target $HOME
else
    curl https://go.dev/dl/go1.19.1.darwin-amd64.pkg
    installer -pkg go1.19.1.darwin-amd64.pkg -target $HOME
fi

nvm install --lts

echo "export PATH=$PATH:$HOME/go/bin" >> ~/.zshrc

