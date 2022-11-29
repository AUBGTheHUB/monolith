.PHONY: install-web
install-web:
	cd ./packages/web/ && npm install

.PHONY: run-web
run-web:
	cd ./packages/web/ && npm run start

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
	./.githooks/install_hooks.sh

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
	code --install-extension esbenp.prettier-vscode

