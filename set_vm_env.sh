#!/bin/sh

#   IMPORTANT! 
#  
#   This script is used for initializing VM environments
#   which are running the manage_app.py script
#      

yes | sudo apt install python3-pip
yes | sudo apt install docker-compose
yes | sudo snap install certbot --classic

pip install schedule

YELLOW='\033[1;33m'
NC='\033[0m'

echo -e  "\n\n${YELLOW}Set global shell environment variables in ~/.bashrc - https://pastebin.com/WyVVeUJ2\n"
echo -e  "Set API .env file in repo/packages/api/.env - https://pastebin.com/Y8NE96w4\n"
echo -e  "Set WEB .env.production file in repo/packages/web/.env.production - https://pastebin.com/qFXCqe6g\n"
echo -e  "Initialize SSL certs by running 'certbot certonly' (option 1)${NC}\n"
