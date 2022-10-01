#!/bin/sh
 
if [ "$1" != "--post" ]; then
 
	/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
 
	brew install nvm
 
	brew install wget
 
	cd $HOME/Downloads
 
	if [[ $(uname -m) == 'arm64' ]]
	then
	    wget -O go.pkg https://go.dev/dl/go1.19.1.darwin-arm64.pkg 
	else
	    wget -O go.pkg https://go.dev/dl/go1.19.1.darwin-amd64.pkg
	fi
 
	sudo installer -verbose -pkg $HOME/Downloads/go.pkg -target $HOME
    	echo "export PATH=$PATH:/usr/local/go/bin" >> ~/.zshrc

    	cd /usr/local/go/src
    
	git clone git@github.com:AUBGTheHUB/spa-website-2022.git

    	cd spa-website-2022

    	exec $SHELL
 
else
    	nvm install --lts
	cd /usr/local/go/src/spa-website-2022

	make install-hooks 
	make install-web

	echo "alias spa = \"cd ${PWD}\"" >> $HOME/.zshrc
fi
