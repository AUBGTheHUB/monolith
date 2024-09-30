#Installs the node_modules in the project root and creates .env files for each of the services
npm install && make install-env
#Installs husky - pre-commit manager for .js, .css, .html
npm run prepare
#Installs gum - helps with creating interactive terminal user interfaces
make install-gum
#Enables the .venv folder to appear inside the project - currently ./services/py_api - poetry installs all the deps on this
poetry config virtualenvs.in-project true
#Installs the node_modules inside ./services/web
make install-web
#Installs the backend dependencies
cd ./services/py_api/
poetry install
