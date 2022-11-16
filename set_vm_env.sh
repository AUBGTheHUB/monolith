#!/bin/sh

#   IMPORTANT! 
#  
#   This script is used for initializing VM environments
#   which are running the manage_app.py script
#      

yes | apt install python3-pip
yes | apt install docker-compose

pip install schedule
