PHONY: func-debug
func-debug:
	functions-framework --target mailer --debug

PHONY: func-deploy
func-deploy:
	gcloud functions deploy mailer --region=europe-west3 --runtime=python310 \
	--trigger-http --set-secrets="HUB_MAIL=HUB_MAIL:latest" --set-secrets="HUB_PSW=HUB_PSW:latest" \
	--set-secrets="BEARER=BEARER:latest" --allow-unauthenticated