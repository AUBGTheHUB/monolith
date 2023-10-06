BRANCH="$1"
WEBHOOK="$2"

if [ -z "$BRANCH" ] || [ -z "$WEBHOOK" ]; then
  echo "Error: BRANCH or WEBHOOK is empty. Exiting."
  exit 1
fi

docker-compose up --build -d

if [ $? -eq 0 ]; then
    TAILED_LOGS=$(tail -n 20 ./deployment.logs)
    RESULT_STRING="branch ${BRANCH} deployment is ok\nsukablyat: ${TAILED_LOGS}"
    curl -X POST ${WEBHOOK} -H "Content-Type: application/json" -d "{\"content\": \"${RESULT_STRING}\"}"
else
    FAILURE_OUTPUT=$(tail -n 20 ./deployment.logs)
    RESULT_STRING="branch ${BRANCH} deployment is bad bad stuff\nLast 20 Lines: ${FAILURE_OUTPUT}"
    curl -X POST ${WEBHOOK} -H "Content-Type: application/json" -d "{\"content\": \"${RESULT_STRING}\"}"
fi
