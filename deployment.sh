BRANCH="$1"
WEBHOOK="$2"

if [ -z "$BRANCH" ] || [ -z "$WEBHOOK" ]; then
  echo "Error: BRANCH or WEBHOOK is empty. Exiting."
  exit 1
fi

# ! subdomain should include all periods including the one before the domain
SUBDOMAIN="dev."
if [ $BRANCH -eq "production" ]; then
    SUBDOMAIN=""
# ------------------------------------------------

declare -A services
services["https://${SUBDOMAIN}thehub-aubg.com"]=200
services["https://${SUBDOMAIN}thehub-aubg.com/api/validate"]=400
services["https://${SUBDOMAIN}thehub-aubg.com/v2/health"]=200
services["https://${SUBDOMAIN}thehub-aubg.com/s/mono"]=200

# ? --- questionnaire check is missing in manage_app ?
# services["https://${SUBDOMAIN}thehub-aubg.com/questionnaires/test"]=200

# ------------------------------------------------

docker-compose up --build -d

if [ $? -eq 0 ]; then
    RESULT_STRING="Running docker-compose on ${BRANCH} deployment failed!"
    curl -X POST ${WEBHOOK} -H "Content-Type: application/json" -d "{\"content\": \"${RESULT_STRING}\"}"
    exit 1
fi

for url in "${!services[@]}"; do
    expected_status="${services[$url]}"
    actual_status=$(curl -o /dev/null -Isw '%{http_code}\n' "$url")

    if [[ "$actual_status" -ne "$expected_status" ]]; then
        RESULT_STRING="Health check to ${url} failed with status code: ${actual_status}"
        curl -X POST ${WEBHOOK} -H "Content-Type: application/json" -d "{\"content\": \"${RESULT_STRING}\"}"
        exit 1
    fi
done

RESULT_STRING="Deployment was successful for branch: ${BRANCH}"
curl -X POST ${WEBHOOK} -H "Content-Type: application/json" -d "{\"content\": \"${RESULT_STRING}\"}"
