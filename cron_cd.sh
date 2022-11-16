#!/bin/bash
 cd $HOME/hub-conf-signup
 git reset --hard origin/master
 git fetch

 HEADHASH=$(git rev-parse HEAD)
 UPSTREAMHASH=$(git rev-parse master@{upstream})
 FINISHED='\033[1;96m'
 NOCOLOR='\033[0m' # No Color
 ERROR='\033[0;31m'

 if [ "$HEADHASH" != "$UPSTREAMHASH" ]
 then
    echo -e "${ERROR}Not up to date with origin. ${NOCOLOR}"
    # docker-compose down
    git pull
    docker-compose up --build -d
    exit 0
else
    echo -e ${FINISHED}Current branch is up to date with origin/master.${NOCOLOR}
fi

