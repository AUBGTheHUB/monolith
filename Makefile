.PHONY: install-web
install-web:
	cd ./services/web/ && npm install

.PHONY: run-web
run-web:
	cd ./services/web/ && npm run dev

# TO-DO: Write the script for spinning up the dev server
# .PHONY: run-dev
# run-dev:
# 	cd ./services/web/ && npm run start

.PHONY: run-prod
run-prod:
	cd ./services/web/ && npm run prod

.PHONY: lint
lint:
	cd ./services/web/ \
	&& npm run lint || true \

.PHONY: install-hooks
install-hooks:
	npm install; \
	npm run prepare; \

.PHONY: post-osx
post-osx:
	./install_osx.sh --post

.PHONY: post-wsl
post-wsl:
	./install_wsl.sh --post

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

.PHONY: reload-api
reload-api:
	cd packages/api && bash ./reload.sh

.SILENT: gum
gum:
	bash ./cli.sh

.PHONY: install-env
install-env:
	cp -n .env.sample .env; \
	ln -sf ${PWD}/.env ${PWD}/services/web/.env.development; \
	ln -sf ${PWD}/.env ${PWD}/services/url_shortener/.env; \
	ln -sf ${PWD}/.env ${PWD}/services/py_api/.env; \
	ln -sf ${PWD}/.env ${PWD}/services/questionnaire;


.PHONY: install-python
install-python:
	if [ $(shell command -v apt-get) ]; then \
		sudo apt-get update; \
		sudo apt-get install -y python3.12; \
		sudo apt install -y pipx; \
	elif [ $(shell command -v brew) ]; then \
		brew install python@3.12; \
		brew install pipx; \
	else \
		echo "No supported package managers found."; \
		exit 1; \
	fi; \
	pipx ensurepath; \
	pipx install poetry; \
	poetry config virtualenvs.in-project true; \
	cd ./services/py_api/; \
	poetry install; \
	poetry run pre-commit install;


.PHONY: run-py-api
run-py-api:
	cd services/py_api && poetry run start

.PHONY: install-signed-certs
install-signed-certs:
	cp data/certs/local.crt data/certs/devenv.crt
	cp data/certs/local.key data/certs/devenv.key

.PHONY: run-rust-api
run-rust-api:
	cd packages/services/url_shortener && make watch

.PHONY: run-svelte-quest
run-svelte-quest:
	cd packages/services/questionnaire && npm run dev -- --open

.PHONY: run-email-template
run-email-template:
	cd packages/services/react-email-starter && npm run dev
