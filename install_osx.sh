#!/bin/sh
 
if [ "$1" != "--post" ]; then
 
	brew install nvm

    echo -e 'export NVM_DIR="$HOME/.nvm"
    [ -s "/usr/local/opt/nvm/nvm.sh" ] && \. "/usr/local/opt/nvm/nvm.sh"  # This loads nvm
    [ -s "/usr/local/opt/nvm/etc/bash_completion.d/nvm" ] && \. "/usr/local/opt/nvm/etc/bash_completion.d/nvm"  # This loads nvm bash_completion' >> ~/.zshrc

	brew install wget
 
	cd $HOME/Downloads
 
	if [[ $(uname -m) == 'arm64' ]]
	then
	    wget -O go.pkg https://go.dev/dl/go1.19.1.darwin-arm64.pkg 
	else
	    wget -O go.pkg https://go.dev/dl/go1.19.1.darwin-amd64.pkg
	fi
 
	sudo installer -verbose -pkg $HOME/Downloads/go.pkg -target $HOME
    echo "export PATH=$PATH:$HOME/go/bin" >> ~/.zshrc

	cd /usr/local/go/src

    sudo rm -rf $HOME/go
	sudo mv /usr/local/go $HOME
	sudo chmod -R 777 $HOME/go
    
    cd $HOME/go/src

	git clone git@github.com:AUBGTheHUB/monolith.git

    cd monolith

	chsh -s /bin/zsh # set zsh as default

    exec $SHELL 
 
else

	YELLOW='\033[1;33m'
	NC='\033[0m'

    echo -e "\n${YELLOW}If you are getting the following error: nvm command not found\n"
    echo -e "Please, log out and log in again - this is a common issue where another default shell is trying to execute instead of zsh\n"
    echo -e "The first step of the project intialization has already set up a new login shell\n${NC}"

	source $HOME/.nvm/nvm.sh
	nvm install --lts
	cd $HOME/go/src/monolith

	make install-hooks 
	make install-web
	make install-env
	make install-code-plugins
	make install-python

	echo "alias spa=\"cd ${PWD}\"" >> $HOME/.zshrc
fi
