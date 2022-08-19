# @AUBGTheHUB's Single-Page Application

## How to run the project
---
<em>Commands should be run in the root directory of the project</em>

### Backend
* Installation: 
```shell
# 1. install go - https://go.dev/doc/install
# 2. git clone the repo in go/src
# 3. download the .env file from Google Drive and place it in root/packages/api
```

* Run:
```shell
make run-api
```

### Frontend 
* Installation: 
```shell
# update node to 16.16.0
make install-web
```

* Run:
```shell
make run-web
```

* Lint:
```shell
make lint  # makes your code more readable 🥰
```

### Git hooks

* Install pre-commit hook:
```shell 
make install-hooks  # GitBash, WSL, UNIX/Linux -> anything that can run bash scripts
```
Do not install the hooks if you are going to be using `Powershell`

This is going to execute a script which will <em>install</em> git commit hooks.  
The pre-hook is linting the JS code and the post-hook amends the changes to the commit, hence there will be no need for you to do it manually.  
The hooks generate a `files_for_commit.txt`, which is used for tracking state. Please, do ignore it!   

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

---
###### CODEOWNERS: [NOSYNCDEV](https://github.com/orgs/AUBGTheHUB/teams/nosyncdev)
