# @AUBGTheHUB's Single-Page Application

[![Integration Tests](https://github.com/AUBGTheHUB/spa-website-2022/actions/workflows/integration_tests.yml/badge.svg)](https://github.com/AUBGTheHUB/spa-website-2022/actions/workflows/integration_tests.yml)

[![Build Frontend](https://github.com/AUBGTheHUB/spa-website-2022/actions/workflows/build_frontend.yml/badge.svg)](https://github.com/AUBGTheHUB/spa-website-2022/actions/workflows/build_frontend.yml)

[![Notify Discord - New Issue](https://github.com/AUBGTheHUB/spa-website-2022/actions/workflows/discord_issue.yml/badge.svg)](https://github.com/AUBGTheHUB/spa-website-2022/actions/workflows/discord_issue.yml)

[![Notify Discord - New PR](https://github.com/AUBGTheHUB/spa-website-2022/actions/workflows/discord_pr.yml/badge.svg)](https://github.com/AUBGTheHUB/spa-website-2022/actions/workflows/discord_pr.yml)
## How to set up the project

Check [Backend](#backend), [Frontend](#frontend), [Hooks](#git-hooks) and [Plugins](#vscode-plugins)
##### Recommended Text Editor: `VSCode`
##### Recommended Plugins: `GitLens`
---

### Adding your SSH key to the ssh-agent and GitHub
⚠️ This step is a prerequisite for the installation scripts

Here is the guide:
* [Generate SSH key and add it to agent](https://docs.github.com/en/authentication/connecting-to-github-with-ssh/generating-a-new-ssh-key-and-adding-it-to-the-ssh-agent)

* [Add key to Github](https://docs.github.com/en/authentication/connecting-to-github-with-ssh/adding-a-new-ssh-key-to-your-github-account)

---
### OSX installation

Install brew and follow the instructions (sometimes it asks you to run some additional commands):
```shell
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

```shell
curl https://raw.githubusercontent.com/AUBGTheHUB/spa-website-2022/master/install_osx.sh | bash
```

And then run:
```bash
cd ~/go/src/spa-website-2022 && make post-osx
```

⚠️  If you are getting the following exceptions:

* `nvm command not found` - you have to log out of your current user and log in again.
* golang packages not found - run the make scripts with `sudo`

---
### WSL installation
* For [Ubuntu](https://www.microsoft.com/store/productId/9PDXGNCFSCZV) WSL
```bash
curl https://raw.githubusercontent.com/AUBGTheHUB/spa-website-2022/master/install_wsl.sh | bash
```

And then run:
```bash
cd ~/go/src/spa-website-2022 && make post-wsl
```

### Easy access to repo

```bash
spa # alias for cd ~/go/src/spa-website-2022 set in .zshrc or .bashrc
```
---
### __GUM__:
* GUM can be used for the following: 
    * ``Run Client (requests towards local API)``
    * ``Run Client (requests towards deployed API)``
    * ``Run API``
    * ``SSH into a VM``
    * ``Set up VM for Deployment``

*If you don't want to use gum, you may proceed to the next sections*
#### __Set up__:
```
1. vim ~/.bashrc
2. Add export HUB_VM="root@188.166.65.120" (make sure it's not in an if statement or for cycle)
3. Type :q and press Enter
```
### __Run Development__:
```
1. make gum
2. Choose Develop
3. Choose which instance you want to spin up
```
### __Run Deploy__:
```
1. make gum
2. Choose Deploy
3. Choose what you would like to do
    3.1. SSH into a Virtual Machine
    3.2. Set up Virutal Machine for Deployment - SSHs into the VM and executes the "set_vm_env.sh" script
```
---
### Backend
* Installation from `root` (not needed if you've run one of the above mentioned installations): 
```markdown
1. install go - https://go.dev/doc/install
2. git clone the repo in go/src
3. download the .env file from Google Drive and place it in root/packages/api
```

* __Static BEARER-TOKEN__:
Add this in the .env file
```bash
IS_OFFLINE="true"  # IS_TEST="true" overwrites this
                   # so make sure that you set IS_TEST to false
                   # after you're done running integration/unit tests
```

* __Run__:
```shell
make run-api
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
* Installation from `root` (needed when there are new packages added to `package.json`): 
```shell
# update node to 16.16.0
make install-web
```

* Run from `root`:
```shell
make run-web # web is going to make requests towards a local instance of api (make run-api)

make run-dev # web is going to make requests towards a deployed instance of the api (e.g. https://dev.thehub-aubg.com/api)
```

** For installing, running, cleaning and building from `web` - take a look at the `scripts` in `web/package.json`

* Lint (part of the hooks):
```shell
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
    │   └── api
    │       ├── controllers
    │       ├── models
    │       ├── configs
    │       ├── responses
    │       └── routes
    └── web
        ├── public
        └── src
```
---
## How to work on a feature and open a Pull Request?
1. Choose an issue you want to work on (e.g. [#11 - Optimizations](https://github.com/AUBGTheHUB/spa-website-2022/issues/11))
2. Create a new branch by running the following command:
```shell
git checkout -b "#11-Optimizations"
```
3. When commiting, place the issue number at the beginning of the commit message
```shell
git add .                               # be careful if something important is not gitignored
git commit -m "#11 Added new feature"
```
4. Push your updates to the remote branch 
```
git push --set-upstream origin #11-Optimizations
```
5. Contribute 😎 (Open a Pull Request towards the main branch)
- Reference the issue in the title
- Write a brief discription of what you have worked on  

#### If nobody has reviewed the Pull Request by the end of the day, ping [@asynchroza](https://github.com/asynchroza)

---
### Important: 
* If you encounter any issues setting up the project, ping either [@asynchroza](https://github.com/asynchroza) or [@nikolayninov](https://github.com/nikolayninov)
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
