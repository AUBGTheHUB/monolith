PHONY: func-debug
func-debug:
	functions-framework --target object_uploader --debug

PHONY: func-deploy
func-deploy:
	gcloud functions deploy object_uploader --region=europe-west3 --runtime=python310 \
	--trigger-http --set-secrets="AWS_PUB_KEY=AWS_PUB_KEY:latest" \
	--set-secrets="AWS_PRIV_KEY=AWS_PRIV_KEY:latest" --set-secrets="AWS_BUCKET_NAME=AWS_BUCKET_NAME:latest" \
	--set-secrets="BEARER=BEARER:latest" --allow-unauthenticated