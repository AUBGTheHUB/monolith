BRANCH="$1"
WEBHOOK="$2"

if [ -z "$BRANCH" ] || [ -z "$WEBHOOK" ]; then
  echo "Error: BRANCH or WEBHOOK is empty. Exiting."
  exit 1
fi

docker-compose up --build -d

if [ $? -eq 0 ]; then
    RESULT_STRING="${BRANCH} deployment is ok"
    curl -X POST ${WEBHOOK} -H "Content-Type: application/json" -d "{\"content\": \"${RESULT_STRING}\"}"
else
    RESULT_STRING="${BRANCH} deployment failed"
    curl -X POST ${WEBHOOK} -H "Content-Type: application/json" -d "{\"content\": \"${RESULT_STRING}\"}"
fi
