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
echo -e  "\n\As per the latest updates, docker-compose is loading an environment file from the root of the project.\n"
echo -e  "This environment file should be called '.env' and should have the following contents - https://pastebin.com/dN0XLuR3\n"
echo -e  "You will need to ask a member with Principal permissions on Discord to give you the password\n\n"
echo -e  "Initialize SSL certs by running 'certbot certonly' (option 1)${NC}\n"
