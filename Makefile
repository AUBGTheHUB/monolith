.PHONY: install-web
install-web:
	cd ./services/web/ && npm install

.PHONY: run-web
run-web:
	cd ./services/web/ && npm run dev

.PHONY: install-gum
install-gum:
	go install github.com/charmbracelet/gum@latest

.SILENT: gum
gum:
	bash ./cli.sh

.PHONY: run-py-api
run-py-api:
	cd services/py-api && poetry run start

.PHONY: run-rust-api
run-rust-api:
	cd services/url_shortener && make watch

.PHONY: run-svelte-quest
run-svelte-quest:
	cd services/questionnaire && npm run dev -- --open

.PHONY: run-email-template
run-email-template:
	cd services/react-email-starter && npm run dev
