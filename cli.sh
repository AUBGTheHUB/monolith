#!/bin/bash

current_directory=${PWD##*/}

if [[$current_directory != "monolith" ]]
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

echo -e "What instance do you want to spin up?"

WEB_CLIENT="React frontend"
LOCAL_PY_API="Python backend"
LOCAL_QUESTIONNAIRE="Questionnaire"
LOCAL_RUST_API="URL Shortener"
EMAIL_TEMPLATE="Email Template"
ACTIONS=$(gum choose --limit 1 "$WEB_CLIENT" "$LOCAL_PY_API" "$LOCAL_RUST_API" "$LOCAL_QUESTIONNAIRE" "$EMAIL_TEMPLATE")

ACTIONS_EXIT_STATUS=$?
clear

if [ $ACTIONS_EXIT_STATUS -eq 0 ]; then
    gum style --border normal --margin "1" --padding "1 2" --border-foreground 212 "You might need to pull the latest dependencies if the service is unable to start."
fi


if [ "$ACTIONS" == "$WEB_CLIENT" ]; then
    make run-web
elif [ "$ACTIONS" == "$LOCAL_PY_API" ]; then
    make run-py-api
elif [ "$ACTIONS" == "$LOCAL_QUESTIONNAIRE" ]; then
    make run-svelte-quest
elif [ "$ACTIONS" == "$LOCAL_RUST_API" ]; then
    make run-rust-api
elif [ "$ACTIONS" == "$EMAIL_TEMPLATE" ]; then
    make run-email-template
else
    echo "Invalid option"
    exit 1

fi
