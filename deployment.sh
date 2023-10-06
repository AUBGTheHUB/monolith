BRANCH=$1
WEBHOOK=$2

docker-compose up --build -d

if [[ $? == 0 ]]; then
    FAILURE_OUTPUT=$(tail -n 20 ./nohup.out)
    curl -X POST ${WEBHOOK} -d "content=${BRANCH} deployment: done\noutput:${FAILURE_OUTPUT}"
else
    FAILURE_OUTPUT=$(tail -n 20 ./nohup.out)
    curl -X POST ${WEBHOOK} -d "content=${BRANCH} deployment: failed\noutput:${FAILURE_OUTPUT}"
fi
