PHONY: func-debug
func-debug:
	functions-framework --target object_uploader --debug

PHONY: func-deploy
func-deploy:
	gcloud functions deploy object_uploader --region=europe-west3 --runtime=python310 \
	--trigger-http  \
	--set-secrets="BEARER=BEARER:latest" --allow-unauthenticated