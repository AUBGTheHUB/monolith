# @AUBGTheHUB's Single-Page Application

[![Actions Status](https://github.com/AUBGTheHub/spa-website-2022/workflows/build-compose/badge.svg)](https://github.com/AUBGTheHUB/spa-website-2022/actions)

### For local development:
Remove any `.env` files persistent in the web directory

### For deployment:
* Set WEB:
```shell
echo REACT_APP_DEV_URL=$URL > $ROOT_DIRECTORY_SPA/packages/web/.env

# where ROOT_DIRECTORY_SPA is the root of the project
# for most of you, this will be $HOME/go/src/spa-website-2022
```

* Set API:
Check NOSYNCDEV for `echo` command

## How to run the project
`make` <em>commands should be run in the `root` directory of the project</em>  
`npm run` <em>commands should be run in the `web` directory</em>   
##### Recommended Text Editor: `VSCode`

### Adding your SSH key to the ssh-agent and GitHub
⚠️ This step is a prerequisite for the installation scripts

Here is the guide:
* [Generate SSH key and add it to agent](https://docs.github.com/en/authentication/connecting-to-github-with-ssh/generating-a-new-ssh-key-and-adding-it-to-the-ssh-agent)

* [Add key to Github](https://docs.github.com/en/authentication/connecting-to-github-with-ssh/adding-a-new-ssh-key-to-your-github-account)

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
spa # alias for cd ~/go/src/spa-website-2022 set in .zshrc
```

### Backend
* Installation from `root` (not needed if you've run one of the above mentioned installations): 
```markdown
1. install go - https://go.dev/doc/install
2. git clone the repo in go/src
3. download the .env file from Google Drive and place it in root/packages/api
```

* Run:
```shell
make run-api
```

### Frontend 
* Installation from `root` (needed when there are new packages added to `package.json`): 
```shell
# update node to 16.16.0
make install-web
```

* Run from `root`:
```shell
make run-web
```

** For installing, running, cleaning and building from `web` - take a look at the `scripts` in `web/package.json`

* Lint (part of the hooks):
```shell
make lint  # makes your code more readable 🥰
```


### Git hooks

* Install pre-commit hook:
```shell 
make install-hooks  # POSIX compliant shells only
```
Do not install the hooks if you are going to be using `Powershell`

This is going to execute a script which will <em>install</em> git commit hooks.  
The pre-hook is linting the JS code and the post-hook amends the changes to the commit, hence there will be no need for you to do it manually.  
The hooks generate a `files_for_commit.txt`, which is used for tracking state. Please, do ignore it!   

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
