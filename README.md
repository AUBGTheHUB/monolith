# @AUBGTheHUB's Monolith

[![Build Frontend](https://github.com/AUBGTheHUB/monolith/actions/workflows/build_frontend.yml/badge.svg)](https://github.com/AUBGTheHUB/monolith/actions/workflows/build_frontend.yml)

[![Build Python Backend](https://github.com/AUBGTheHUB/monolith/actions/workflows/build_python_backend.yml/badge.svg)](https://github.com/AUBGTheHUB/monolith/actions/workflows/build_python_backend.yml)

[![Notify Discord - New Issue](https://github.com/AUBGTheHUB/monolith/actions/workflows/discord_issue.yml/badge.svg)](https://github.com/AUBGTheHUB/monolith/actions/workflows/discord_issue.yml)

[![Notify Discord - New PR](https://github.com/AUBGTheHUB/monolith/actions/workflows/discord_pr.yml/badge.svg)](https://github.com/AUBGTheHUB/monolith/actions/workflows/discord_pr.yml)
## > How to set up the project

### Prerequisites
> To understand why we need the following, read more about [Dev Containers](https://containers.dev/).

- Download [Docker Desktop](https://www.docker.com/products/docker-desktop/).
- Download [Visual Studio Code](https://code.visualstudio.com/Download).
- Install the [Dev Containers Extension](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-containers) in Visual Studio Code.
#### For WSL users
---
>Run the following commands in PowerShell admin mode.
- Check the version of your WSL.
```PowerShell
wsl -l -v
```
- If you don't have WSL version 2. Run:
```PowerShell
wsl --set-version <distro name> 2
```
> Change the <distro name> to match the one that you are running. You could see your distro name from the result of the previous command.
- After your WSL version is updated set it as default by running:
```PowerShell
wsl --set-default-version 2
```
- Set the chosen distro as default
```PowerShell
wsl --set-default <distro name>
```
- **Close WSL and reopen it**

After running the above commands. Close PowerShell.
- Open **Docker Desktop**
- Navigate to **Settings**
- From the **General** tab, select **Use WSL 2 based engine**

>You should be all set 🎉
---

### 1. Add your SSH key to the ssh-agent and GitHub

Here is the guide:
* [Generate SSH key and add it to agent](https://docs.github.com/en/authentication/connecting-to-github-with-ssh/generating-a-new-ssh-key-and-adding-it-to-the-ssh-agent)

* [Add key to Github](https://docs.github.com/en/authentication/connecting-to-github-with-ssh/adding-a-new-ssh-key-to-your-github-account)

### 2. Clone the repository to your machine
```bash
git clone git@github.com:AUBGTheHUB/monolith.git
```
### 3. Navigate to the project directory
```bash
cd monolith
```
### 4. Open your project in Visual Studio code. Run:
```bash
code .
```
### 5. Navigate to Visual Studio Code and perform:
- <kbd>command</kbd> + <kbd>shift</kbd> + <kbd>P</kbd> (Mac) or <kbd>ctrl</kbd> + <kbd>shift</kbd> + <kbd>P</kbd> (Windows) to open the command palette
- In the command palette write and select:
```
>Dev Containers: Reopen in Container
```

>After this step you should wait until the container is built. It will install all the dependencies needed for development on its own.

### 6. Check if Dev Container is running successfully
If your Dev Container is running successfully you should be able to see the following in the bottom-right of your
Visual Studio Code client.

<img src="https://i.ibb.co/qnYQ6Qp/Screenshot-2024-10-07-at-2-33-55-PM.png" alt="image" border="0">


### __HOW TO RUN PROJECT__ or so called __GUM__:
> Before running the command below, make sure you are on the root directory of the project
```bash
make gum
```
> This is a command-line tool for managing running services and setting up deployment environments

**For developers**:


**For deployments**:

<img src="https://i.ibb.co/7nBqHkn/image.png" alt="image" border="0">

---
### Backend

* __Static BEARER-TOKEN__:
Add this in the .env file (update root .env)
```bash
MONGO_URI=<uri>    # Ask NOSYNCDEV for the uri

IS_OFFLINE=true    # IS_TEST=true overwrites this
                   # so make sure that you set IS_TEST to false
                   # after you're done running integration/unit tests
```

* __Run__:
```shell
make run-api # Golang API
make run-py-api # Python API
```

* __Run (hot reload)__:
```
make reload-api
```

* using a task:
    * `ctrl + P` (for mac keybindings might differ)
    * type `task Hot Reload API`

* or:
    * `ctrl + shift + P` (for mac keybindings might differ)
    * type `Tasks: Run Task` and find `Hot Reload API`

---


* #### __Debug__:
1. Put breakpoints:
<img src="https://i.ibb.co/5vW0H6N/image.png" border="0">

2. Go to `main.go`, open `Run and Debug` and choose the `Debug API` task:
<img src="https://i.ibb.co/K0GnCY9/image.png" border="0">

3. Click the green arrow icon:
<img src="https://i.ibb.co/9VrKp3R/image.png" border="0">


* #### __How to resolve `could not import module ...`__:
<img src="https://i.ibb.co/KmHqm1q/image.png" alt="image" border="0">


* Open `/packages/api` as a Workspace folder:
    <img src="https://i.ibb.co/tbTs4Wg/image.png" alt="image" border="0">

* Open VSCode directly from within `packages/api` (e.g. `spa && cd packages/api && code .`)

---
### Frontend
Notes:
* No need to run any of this if you installed the project using either one of the installation scripts.
* Object Uploader (S3 admin panel) won't work if you don't update your .env file with the appropriate content (ask the team)

* Installation from `root` (needed when there are new packages added to `package.json`):
```shell
# update node to 16.16.0
make install-web
```

* Run from `root`:
```shell
make run-web    # run this if you are applying changes to the api and you want to test them locally using the frontend (or if prod and dev are down)

make run-dev    # run this if you want the frontend to make requests towards the api which is currently staged on the dev environment

make run-prod   # run this if you want the frontend to make requests towards the production api on https://thehub-aubg.com
```

** For installing, running, cleaning and building from `web` - take a look at the `scripts` in `web/package.json`

* Lint (part of the hooks):
```bash
make lint  # makes your code more readable 🥰
```
---

### Git hooks

* Install pre-commit hook:
```shell
make install-hooks  # POSIX compliant shells only
```
Do not install the hooks if you are going to be using `Powershell`

This is going to execute a script which will <em>install</em> git commit hooks.
The pre-hook is linting the JS code and the post-hook amends the changes to the commit, hence there will be no need for you to do it manually.
The hooks generate a `files_for_commit.txt`, which is used for tracking state. Please, do ignore it!

---
### VSCode plugins
* Install needed plugins by running the following phony:
```
make install-code-plugins # linters and better comments
```

### Docker

```shell
docker-compose up --build
```

---
## Directory structure
```
.
└── packages
    ├── api
    ├── py-api
    └── services
    │   └── url_shortener
    └── web
```

---
## How to work on a feature and open a Pull Request?
1. Choose an issue you want to work on (e.g. [#11 - Optimizations](https://github.com/AUBGTheHUB/monolith/issues/11))
2. Create a new branch by running the following command:
```shell
git checkout -b "11-specific-optimizations"
```
3. When commiting, place the issue number at the beginning of the commit message
```shell
git add .                               # be careful if something important is not gitignored
git commit -m "#11 Added a new feature"
```
4. Push your updates to the remote branch
```bash
git push --set-upstream origin 11-Optimizations
```
5. Contribute 😎 (Open a Pull Request towards the main branch)
- Reference the issue in the title
- Write a brief discription of what you have worked on

---
### Important:
* If you encounter any issues setting up the project, ping the team in Discord or Messenger
* If you are stuck and you need help, ping the dev group chat in facebook 🤼
* Do not forget to <em>crack open a cold one</em> 🍻 with your fellow colleagues after spending countless hours debugging rendering issues 😁

### Possible problems:

MONGO DNS issue:
```bash
make run-api
cd ./packages/api/ && go run main.go
2022/10/03 01:57:24 error parsing uri: lookup thehubwebsite.h9aqj.mongodb.net on 192.168.68.1:53: cannot unmarshal DNS message
exit status 1
make: *** [Makefile:11: run-api] Error 1
```

--> resolve by [doing this](https://stackoverflow.com/a/60560041)

### Tips & Tricks:
* If you suspend either the react app job or the api job by mistake and cannot kill the job for some reason, use this to unbind the port `lsof -ti:PortNumberGoesHere | xargs kill -9`

---
#### CODEOWNERS: [NOSYNCDEV](https://github.com/orgs/AUBGTheHUB/teams/nosyncdev)
After you are done working on a feature, you may add yourself to the `CODEOWNERS` file.
