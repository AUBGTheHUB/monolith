BRANCH="$1"
WEBHOOK="$2"

if [ -z "$BRANCH" ] || [ -z "$WEBHOOK" ]; then
  echo "Error: BRANCH or WEBHOOK is empty. Exiting."
  exit 1
fi

docker-compose up --build -d

if [ $? -eq 0 ]; then
    result_string="branch ${BRANCH} deployment is ok"
    curl -X POST ${WEBHOOK} -H "Content-Type: application/json" -d "{\"content\": \"${result_string}\"}"
else
    # FAILURE_OUTPUT=$(tail -n 20 ./nohup.out)
    result_string="branch ${BRANCH} deployment is bad bad stuff\nExit Code: ${$?}"
    curl -X POST ${WEBHOOK} -H "Content-Type: application/json" -d "{\"content\": \"${result_string}\"}"
fi
