install-web:
	cd ./services/web/ && npm install

run-web:
	cd ./services/web/ && npm run dev

install-gum:
	go install github.com/charmbracelet/gum@latest

.SILENT: gum
gum:
	bash ./cli.sh

run-py-api:
	cd services/py-api && poetry run start

run-rust-api:
	cd services/url_shortener && make watch

run-svelte-quest:
	cd services/questionnaire && npm run dev -- --open

run-email-template:
	cd services/react-email-starter && npm run dev
