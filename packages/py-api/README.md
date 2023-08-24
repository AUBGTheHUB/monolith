# Python API

## Prerequisites

Check your python version:
```bash
python --version
```
If your version is not `3.11.*`, follow the guides below:
* For [Linux/WSL](https://www.itsupportwale.com/blog/how-to-upgrade-to-python-3-11-on-ubuntu-20-04-and-22-04-lts/)
* For [MacOS](https://apple.stackexchange.com/questions/201612/keeping-python-3-up-to-date-on-a-mac#:~:text=to%20update%20python%20run%20brew,also%20take%20care%20of%20R)

## Installation
1. Navigate to `py-api` directory
2. Run `poetry config virtualenvs.in-project true`
3. Run `poetry install`
4. Copy the path of the newly generated `.venv` folder in `py-api`
5. `Ctrl + Shift + P` and search for `Python: Select Interpreter` in VSCode (`Cmd` instead of `Ctrl` for Mac users) - [Command Palette](https://code.visualstudio.com/docs/getstarted/userinterface#_command-palette)
6. Paste the copied path

## How to run
`poetry run start` will start the server on port `6969`
