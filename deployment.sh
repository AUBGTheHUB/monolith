BRANCH=$1
WEBHOOK=$2

docker-compose up --build -d

if [[ $? == 0 ]]; then
    # FAILURE_OUTPUT=$(tail -n 20 ./nohup.out)
    result_string="branch ${BRANCH} deployment is ok\nExit Code: ${$?}"
    curl -X POST ${WEBHOOK} -H "Content-Type: application/json" -d "{\"content\": \"${result_string}\"}"
else
    result_string="branch ${BRANCH} deployment is bad bad stuff\nExit Code: ${$?}"
    curl -X POST ${WEBHOOK} -H "Content-Type: application/json" -d "{\"content\": \"${result_string}\"}"
fi
