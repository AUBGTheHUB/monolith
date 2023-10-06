BRANCH=$1
WEBHOOK=$2

docker-compose up --build -d

if [[ $? == 0 ]]; then
    # FAILURE_OUTPUT=$(tail -n 20 ./nohup.out)
    curl -X POST ${WEBHOOK} -d "content="${BRANCH} deployment: ok\n\nexit_code:${$?}""
else
    # FAILURE_OUTPUT=$(tail -n 20 ./nohup.out)
    curl -X POST ${WEBHOOK} -d "content="${BRANCH} deployment: failed\n\nexit_code:${$?}""
fi
