npm install && make install-env
npm run prepare
make install-gum
poetry config virtualenvs.in-project true
make install-web
cd ./services/py_api/
poetry install
echo "source $(poetry env info --path)/bin/activate" >> ~/.bashrc
