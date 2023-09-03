.PHONY: install-web
install-web:
	cd ./packages/web/ && npm install

.PHONY: run-web
run-web:
	cd ./packages/web/ && npm run start

.PHONY: run-dev
run-dev:
	cd ./packages/web/ && npm run dev

.PHONY: run-prod
run-prod:
	cd ./packages/web/ && npm run prod

.PHONY: run-api
run-api:
	cd ./packages/api/ && go run main.go

.PHONY: lint
lint:
	cd ./packages/web/ \
	&& npm run lint || true \
	&& npm run lint:fix \
	&& npm run format

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
	code --install-extension golang.Go


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
	ln -sf ${PWD}/.env ${PWD}/packages/web/.env.development; \
	ln -sf ${PWD}/.env ${PWD}/packages/api/.env; \
	ln -sf ${PWD}/.env ${PWD}/packages/services/url_shortener/.env; \
	ln -sf ${PWD}/.env ${PWD}/packages/py-api/.env

.PHONY: install-python
install-python:
	if [ $(shell uname -s) = Linux ]; \
	then \
		echo 'export PATH="/$(shell whoami)/.local/bin:$$PATH"' >> ~/.zshrc; \
		curl -sSL https://install.python-poetry.org | python3 - ;\
		cd ./packages/py-api && \
		PATH=/$(shell whoami)/.local/bin:$$PATH poetry install; \
	else \
		echo 'export PATH="/Users/$(shell whoami)/.local/bin:$$PATH"' >> ~/.zshrc; \
		curl -sSL https://install.python-poetry.org | python3 - ;\
		cd ./packages/py-api && \
		PATH=/Users/$(shell whoami)/.local/bin:$$PATH poetry install; \
	fi \

	echo "Please, reload your shell!"

.PHONY: run-py-api
run-py-api:
	cd packages/py-api && poetry run start

.PHONY: run-nginx
run-nginx:
	cd nginx && docker-compose up --build

.PHONY: run-svelte
run-svelte:
	## "dev": "vite dev --port 3001 --host",
	cd packages/svelte && npm install && npm run dev -- --open
