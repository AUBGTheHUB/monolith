npm install && make install-env
poetry config virtualenvs.in-project true;
cd ./services/py_api/;
poetry install;
poetry run pre-commit install;