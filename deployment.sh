#!/bin/bash

BRANCH="$1"
WEBHOOK="$2"

if [ -z "$BRANCH" ] || [ -z "$WEBHOOK" ]; then
  echo "Error: BRANCH or WEBHOOK is empty. Exiting."
  exit 1
fi

REPO_URL="https://github.com/AUBGTheHUB/monolith"
COMMIT_ID=$(git rev-pase HEAD)
COMMIT_TITLE=$(git log -1 --pretty=%B)
COMMIT_URL="$REPO_URL/commit/$COMMIT_ID"
COMMIT_TITLE_URL="🔔:[$COMMIT_TITLE]($COMMIT_URL)"

if [ "$BRANCH" = "production" ]; then
    DEPLOYMENT_ENV="PROD"
else
    DEPLOYMENT_ENV="DEV"
fi

#----------------------------BUILD SERVICES---------------------------------------
ERROR_MESSAGE = $(docker compose up --build -d 2>&1) #Runs the command and stores the error message if something goes wrong

if [ $? -ne 0 ]; then
    content="🏗️: $DEPLOYMENT_ENV
    $COMMIT_TITLE_URL
    ❌: Build Failed"

    json_payload=$(jq -n --arg ERR "$ERROR_MESSAGE" --arg CONTENT "$content" '{"content": $CONTENT, "embeds":[{"title": "BUILD",  "description": $ERR}]}')
    curl -X POST "${WEBHOOK}" -H "Content-Type: application/json" -d "$json_payload"
    exit 1
fi

sleep 20

#----------------------------HEALTH CHECKS----------------------------------------
# ! subdomain should include all periods, including the one before the domain
# we assume all non-prod deployments are tested on dev machine
SUBDOMAIN="dev."
if [ "$BRANCH" = "production" ]; then
    SUBDOMAIN=""
fi

# domain variable for easily debugging locally
DOMAIN="thehub-aubg.com"

MAIN_FE="${SUBDOMAIN}${DOMAIN}"
GO_API="${SUBDOMAIN}${DOMAIN}/api/validate"
PY_API="${SUBDOMAIN}${DOMAIN}/v2/health"
SHORTENER="${SUBDOMAIN}${DOMAIN}/s/mono"

# ? declare -A services was BuGgInG, g :/
# * define services' urls
services=($MAIN_FE $GO_API $PY_API $SHORTENER)

# * define their appropriate request methods
methods=("GET" "POST" "GET" "GET")

# * define expected status codes
status_codes=(200 400 200 301)

# TODO: Even if there's a failing request, finish up for loop and then exit
for ((i = 0; i < ${#services[@]}; i++)); do
    url="${services[i]}"
    method="${methods[i]}"
    expected_status="${status_codes[i]}"
    actual_status=$(curl -m 5 -o /dev/null -Isw '%{http_code}\n' -X "$method" "https://$url")

    if [[ "$actual_status" -ne "$expected_status" ]]; then
        RESULT_STRING="Health check to ${url} failed with status code: ${actual_status}"

        content="🏗️: $DEPLOYMENT_ENV
        $COMMIT_TITLE_URL
        ❌: Build Failed"

        json_payload=$(jq -n --arg ERR "$RESULT_STRING" --arg CONTENT "$content" '{"content": $CONTENT, "embeds":[{"title": "BUILD",  "description": $ERR}]}')
        curl -X POST "${WEBHOOK}" -H "Content-Type: application/json" -d "$json_payload"
        exit 1
    fi
done

#----------------------------HEALTH CHECKS DONE-----------------------------------

curl -X POST "${WEBHOOK}" -H "Content-Type: application/json" -d "{\"content\": \"🏗️:${DEPLOYMENT_ENV}\\n${COMMIT_TITLE_URL}\\n✅:Build Successful\"}"
