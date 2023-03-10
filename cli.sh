#!/bin/bash

current_directory=${PWD##*/} 

set_vm_ip () {
    if [[ ! -z "${HUB_VM}" ]]; then
        echo "Do you wish to use the currently saved Virtual Machine IP?"
        USE_DEFAULT=$(gum choose --limit 1 "yes" "no")
        if [ "$USE_DEFAULT" == "yes" ]; then
            VM_IP=$HUB_VM
            return
        fi
    fi

    echo "What's the user of the $(gum style --foreground 212 "Virtual Machine") (in most cases it's $(gum style --foreground 212 "root")):"
    read USER

    echo "What's the IP of the $(gum style --foreground 212 "Virtual Machine"):"
    read IP

    VM_IP="$USER@$IP"
}

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

ACTIONS=$(gum choose --cursor-prefix "[ ] " --no-limit "$START" "$DEPLOY" )

if [ $ACTIONS == $START ]; then
    clear
    echo -e "What instance do you want to spin up?"

    LOCAL_CLIENT="Client (requests towards local api)"
    DEPLOYED_CLIENT="Client (requests towards deployed api)"
    LOCAL_API="Run Api"
    ACTIONS=$(gum choose --cursor-prefix "[ ] " --no-limit "$LOCAL_CLIENT" "$DEPLOYED_CLIENT" "$LOCAL_API")

    clear

    if [ "$ACTIONS" == "$LOCAL_CLIENT" ]; then 
        make run-web
    elif [ "$ACTIONS" == "$DEPLOYED_CLIENT" ]; then
        make run-dev
    elif [ "$ACTIONS" == "$LOCAL_API" ]; then
        make reload-api
    fi

elif [ "$ACTIONS" == "$DEPLOY" ]; then
    LOGIN_IN_VM="SSH into a Virtual Machine"
    SET_VM_ENV="Set up Virtual Machine for Deployment"
    VM_IP=""

    ACTIONS=$(gum choose --cursor-prefix "[ ] " --no-limit "$LOGIN_IN_VM" "$SET_VM_ENV")

    if [ "$ACTIONS" == "$LOGIN_IN_VM" ]; then
        set_vm_ip
        ssh $VM_IP
    
    elif [ "$ACTIONS" == "$SET_VM_ENV" ]; then
        set_vm_ip
        ssh -t $VM_IP "curl https://raw.githubusercontent.com/AUBGTheHUB/spa-website-2022/%23167-Gum-Managing-Tool/set_vm_env.sh | bash"
    fi
fi