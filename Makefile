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

# .PHONY: install-env
# install-env:
# 	cp -n .env.sample .env; \
# 	ln -sf ${PWD}/.env ${PWD}/packages/web/.env.development; \
# 	ln -sf ${PWD}/.env ${PWD}/packages/api/.env; \
# 	ln -sf ${PWD}/.env ${PWD}/packages/services/url_shortener/.env; \
# 	ln -sf ${PWD}/.env ${PWD}/packages/py-api/.env; \
# 	ln -sf ${PWD}/.env ${PWD}/packages/services/questionnaire;

# .PHONY: install-python
# install-python:
# 	if [ $(shell uname -s) = Linux ]; \
# 	then \
# 		echo 'export PATH="/$(shell whoami)/.local/bin:$$PATH"' >> ~/.bashrc; \
# 		curl -sSL https://install.python-poetry.org | python3 - ;\
# 		cd ./services/py_api && \
# 		PATH=/$(shell whoami)/.local/bin:$$PATH poetry install; \
# 	else \
# 		echo 'export PATH="/Users/$(shell whoami)/.local/bin:$$PATH"' >> ~/.zshrc; \
# 		curl -sSL https://install.python-poetry.org | python3 - ;\
# 		cd ./services/py_api && \
# 		PATH=/Users/$(shell whoami)/.local/bin:$$PATH poetry install; \
# 	fi \

# 	echo "Please, reload your shell!"

.PHONY: install-python
install-python:
	if [ $(shell uname -s) = Darwin ]; \
	then \
		echo "Checking if HomeBrew is installed...\n"; \
		if [ $(shell command -v brew) ]; \
		then \
			echo "Homebrew is already installed!\n"; \
		else  \
			echo "Installing HomeBrew...\n"; \
			/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"; \
			export PATH="$$PATH:/opt/homebrew/bin"; \
		fi \
	else \
		echo -e "You are running linux..."; \
	fi \



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
