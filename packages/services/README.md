# **Cloud Functions**:

## Python Setup:
1. Install a python version `^3.9`
```bash
pyenv install 3.9.10  # example
```
2. Set up a virtual env
```bash
pyenv global 3.9.10  # ensure you're creating the env using the correct python version

pyenv virtualenv mailer_service_venv  # where mailer_service_venv could be anything
```

3. Activate virtual env
```bash
pyenv activate mailer_service_venv  # where mailer_service_venv is the name of your venv
```

4. Install required packages
```bash
pip install -r requirements.txt
```

5. Export packages to requirements
```bash
pip freeze > requirements.txt
```

If you're experiencing any issues with pyenv, check if your setup is done correctly. You might be missing environment variables. Read more about [pyenv](https://github.com/pyenv/pyenv) and [pyenv-virtualenv](https://github.com/pyenv/pyenv-virtualenv).

## Running functions framework:

Run cloud function locally in debug mode:
```bash
functions-framework --target <function> --debug
```

using make:
```
make func-debug
```

<img src="https://s3-eu-central-1.amazonaws.com/hubarskibucket/pyenv.png">

## Making requests towards endpoint:

```bash
curl -X POST http://127.0.0.1:8080  # endpoint accepts only POST requests by default
```

## Deploying a cloud function:
*TBD*