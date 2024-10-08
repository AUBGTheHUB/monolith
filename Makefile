.PHONY: install-web
install-web:
	cd ./services/web/ && npm install

.PHONY: run-web
run-web:
	cd ./services/web/ && npm run dev

.PHONY: install-hooks
install-hooks:
	npm install; \
	npm run prepare; \

.PHONY: install-code-plugins
install-code-plugins:
	code --install-extension aaron-bond.better-comments \
	code --install-extension dbaeumer.vscode-eslint \
	code --install-extension esbenp.prettier-vscode \

.PHONY: install-gum
install-gum:
	go install github.com/charmbracelet/gum@latest

.PHONY: install-air
install-air:
	go install github.com/cosmtrek/air@latest

.SILENT: gum
gum:
	bash ./cli.sh

.PHONY: install-env
install-env:
	cp -n .env.sample .env; \
	ln -sf ${PWD}/.env ${PWD}/services/web/.env.development; \
	ln -sf ${PWD}/.env ${PWD}/services/api/.env; \
	ln -sf ${PWD}/.env ${PWD}/services/url_shortener/.env; \
	ln -sf ${PWD}/.env ${PWD}/services/py_api/.env; \
	ln -sf ${PWD}/.env ${PWD}/services/questionnaire;

.PHONY: run-py-api
run-py-api:
	cd services/py_api && poetry run start

.PHONY: install-signed-certs
install-signed-certs:
	cp data/certs/local.crt data/certs/devenv.crt
	cp data/certs/local.key data/certs/devenv.key

.PHONY: run-rust-api
run-rust-api:
	cd services/url_shortener && make watch

.PHONY: run-svelte-quest
run-svelte-quest:
	cd services/questionnaire && npm run dev -- --open

.PHONY: run-email-template
run-email-template:
	cd services/react-email-starter && npm run dev
