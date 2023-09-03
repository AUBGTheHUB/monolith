#!/bin/bash

current_directory=${PWD##*/}

set_vm_ip () {
    if [[ $HUB_VM ]]; then
        echo "A default $(gum style --foreground 212 "public ip") has been previously set up. Do you wish to $(gum style --foreground 212 "reuse") it?"
        USE_DEFAULT=$(gum choose --limit 1 "yes" "no")
        if [ "$USE_DEFAULT" == "yes" ]; then
            VM_IP=$HUB_VM
            return
        fi
    fi

    echo "What's the $(gum style --foreground 212 "user") of the $(gum style --foreground 212 "Virtual Machine") (in most cases it's $(gum style --foreground 212 "root")):"
    read USER

    echo "What's the $(gum style --foreground 212 "public ip") of the $(gum style --foreground 212 "Virtual Machine"):"
    read IP

    VM_IP="$USER@$IP"

    echo "Would you like to remember the $(gum style --foreground 212 "Virtual Machine")?"
    USE_DEFAULT=$(gum choose --limit 1 "yes" "no")
    if [ $USE_DEFAULT == "yes" ]; then
        echo "export HUB_VM=\"$VM_IP\"" >> ~/.bashrc
    fi
}

if [[ $current_directory != "spa-website-2022" && $current_directory != "monolith" ]]
then
    echo "Run this script from the root of the monolith"
    exit 1
fi

if ! hash gum &> /dev/null
then
    echo "GUM could not be found, running installation script"
    make install-gum
fi

gum style --border normal --margin "1" --padding "1 2" --border-foreground 212 "Hello, there! Welcome to The Hub's $(gum style --foreground 212 'monolith')."

echo -e "What would you like to do?"

START="Develop"
DEPLOY="Deploy"

ACTIONS=$(gum choose --limit 1 "$START" "$DEPLOY" )

if [ $ACTIONS == $START ]; then
    clear
    echo -e "What instance do you want to spin up?"

    WEB_CLIENT="Admin Panel"
    DEV_CLIENT="Admin Panel (dev.thehub-aubg.com)"
    PROD_CLIENT="Admin Panel (thehub-aubg.com)"
    LOCAL_API="Golang backend"
    LOCAL_PY_API="Python backend"
    LOCAL_RUST_API="Rust backend"
    NGINX="Reverse Proxy"
    ACTIONS=$(gum choose --limit 1 "$WEB_CLIENT" "$DEV_CLIENT" "$PROD_CLIENT" "$LOCAL_API" "$LOCAL_PY_API" "$LOCAL_RUST_API" "$NGINX")

    clear

    if [ "$ACTIONS" == "$WEB_CLIENT" ]; then
        make run-web
    elif [ "$ACTIONS" == "$DEV_CLIENT" ]; then
        make run-dev
    elif [ "$ACTIONS" == "$PROD_CLIENT" ]; then
        make run-prod
    elif [ "$ACTIONS" == "$LOCAL_API" ]; then
        make reload-api
    elif [ "$ACTIONS" == "$LOCAL_PY_API" ]; then
        make run-py-api
    elif [ "$ACTIONS" == "$LOCAL_RUST_API" ]; then
        make run-rust-api
    elif [ "$ACTIONS" == "$NGINX" ]; then
        make run-nginx
    fi

elif [ "$ACTIONS" == "$DEPLOY" ]; then
    LOGIN_IN_VM="SSH into a Virtual Machine"
    SET_VM_ENV="Set up Virtual Machine for Deployment"
    VM_IP=""

    ACTIONS=$(gum choose --limit 1 "$LOGIN_IN_VM" "$SET_VM_ENV")

    if [ "$ACTIONS" == "$LOGIN_IN_VM" ]; then
        set_vm_ip
        ssh $VM_IP

    elif [ "$ACTIONS" == "$SET_VM_ENV" ]; then
        set_vm_ip
        ssh -t $VM_IP "curl https://raw.githubusercontent.com/AUBGTheHUB/spa-website-2022/master/set_vm_env.sh | bash"
    fi
fi

if [ -z $HUB_VM ] && [ $VM_IP ]; then
    echo "Saving the $(gum style --foreground 212 "Virtual Machine")..."
    exec $SHELL
fi
