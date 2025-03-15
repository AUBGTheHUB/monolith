# @AUBGTheHUB's Monolith

[![Python API Tests](https://github.com/AUBGTheHUB/monolith/actions/workflows/pytests.yml/badge.svg)](https://github.com/AUBGTheHUB/monolith/actions/workflows/pytests.yml)

[![Web Internal Library Tests](https://github.com/AUBGTheHUB/monolith/actions/workflows/webtests.yml/badge.svg)](https://github.com/AUBGTheHUB/monolith/actions/workflows/webtests.yml)

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

> Run the following commands in PowerShell admin mode.

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

> You should be all set 🎉

---

### 1. Add your SSH key to the ssh-agent and GitHub

Here is the guide:

- [Generate SSH key and add it to agent](https://docs.github.com/en/authentication/connecting-to-github-with-ssh/generating-a-new-ssh-key-and-adding-it-to-the-ssh-agent)

- [Add key to Github](https://docs.github.com/en/authentication/connecting-to-github-with-ssh/adding-a-new-ssh-key-to-your-github-account)

### 2. Clone the repository to your machine

```bash
git clone git@images.com:AUBGTheHUB/monolith.git
```

### 3. Navigate to the project directory

```bash
cd monolith
```

---

### Extra Step: For WSL users

In order to make sure that your WSL SSH keys are forwarded to the DEV Container you should run the following script:

```bash
bash wsl_ssh_forwarding.sh
```

[Learn More](https://code.visualstudio.com/remote/advancedcontainers/sharing-git-credentials) about how this is done

---

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

> After this step you should wait until the container is built. It will install all the dependencies needed for development on its own.

### 6. Check if Dev Container is running successfully

If your Dev Container is running successfully you should be able to see the following in the bottom-right of your
Visual Studio Code client.

![](/docs/images/connected_devContainer.png)

---

### **HOW TO RUN THE PROJECT**:

> Run the following command after navigating to the project root directory

```bash
make gum
```

Spin up local server instances:

![](/docs/images/gum_interface.png)

## Directory structure

```
.
└── services
    ├── py-api
    ├── questionnaire
    ├── react-email-starter
    ├── url_shortener
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

- If you encounter any issues setting up the project, ping the team in Discord or Messenger
- If you are stuck and you need help, ping the dev group chat in facebook 🤼
- Do not forget to <em>crack open a cold one</em> 🍻 with your fellow colleagues after spending countless hours debugging rendering issues 😁

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

- If you suspend either the react app job or the api job by mistake and cannot kill the job for some reason, use this to unbind the port `lsof -ti:PortNumberGoesHere | xargs kill -9`

---

#### CODEOWNERS: [NOSYNCDEV](https://github.com/orgs/AUBGTheHUB/teams/nosyncdev)

After you are done working on a feature, you may add yourself to the `CODEOWNERS` file.
