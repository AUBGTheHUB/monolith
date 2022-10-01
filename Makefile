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
	&& npm run lint:fix

.PHONY: install-hooks
install-hooks:
	./.githooks/install_hooks.sh

.PHONY: install-osx
install-osx:
	./install_osx.sh

.PHONY: post-osx
post-osx:
	./install_osx.sh --post
