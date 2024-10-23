## How to set up the API and run it as a standalone:
1. Run `poetry config virtualenvs.in-project true`, this tells poetry to create the virtual env in the project dir. You can learn more [here](https://python-poetry.org/docs/configuration/#virtualenvsin-project)
2. If you have pyenv installed run `poetry config virtualenvs.prefer-active-python true`. You can learn more [here](https://python-poetry.org/docs/managing-environments/)
3. Run `poetry install`
4. Run `poetry run pre-commit install` to install the pre-commit hooks
5. Run `poetry run start` to start the server
