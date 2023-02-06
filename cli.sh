#!/bin/bash

current_directory=${PWD##*/} 

if [[ $current_directory != "spa-website-2022" ]]
then
    echo "Run this script from the root of the SPA project"
    exit 1
fi

if ! hash gum &> /dev/null
then
    echo "GUM could not be found, running installation script"
    make install-gum
fi

gum style --border normal --margin "1" --padding "1 2" --border-foreground 212 "Hello, there! Welcome to The Hub's $(gum style --foreground 212 'SPA project')."

echo -e "What would you like to do?"

START="Develop"
DEPLOY="Deploy"

ACTIONS=$(gum choose --cursor-prefix "[ ] " --selected-prefix "[✓] " --no-limit "$START" "$DEPLOY" )

if [ $ACTIONS == $START ]; then
    clear
    echo -e "What instance do you want to spin up?"

    LOCAL_CLIENT="Client (requests towards local api)"
    DEPLOYED_CLIENT="Client (requests towards deployed api)"
    LOCAL_API="Run Api"
    ACTIONS=$(gum choose --cursor-prefix "[ ] " --selected-prefix "[✓] " --no-limit "$LOCAL_CLIENT" "$DEPLOYED_CLIENT" "$LOCAL_API")

    clear

    if [ "$ACTIONS" == "$LOCAL_CLIENT" ]; then 
        make run-web
    elif [ "$ACTIONS" == "$DEPLOYED_CLIENT" ]; then
        make run-dev
    elif [ "$ACTIONS" == "$LOCAL_API" ]; then
        make run-api
    fi

elif [ "$ACTIONS" == "$DEPLOY" ]; then
    LOGIN_IN_VM="SSH into a Virtual Machine"
    DEPLOY_SPA="Deploy SPA on a Virtual Machine"

    ACTIONS=$(gum choose --cursor-prefix "[ ] " --selected-prefix "[✓] " --no-limit "$LOGIN_IN_VM" "$DEPLOY_SPA")

    if [ "$ACTIONS" == "$LOGIN_IN_VM" ]; then
    echo "What's the user of the $(gum style --foreground 212 "Virtual Machine") (in most cases it's $(gum style --foreground 212 "root")):"
    read USER 

    echo "What's the ip of the $(gum style --foreground 212 "Virtual Machine")":
    read IP 

    ssh "$USER@$IP";
    fi
fi