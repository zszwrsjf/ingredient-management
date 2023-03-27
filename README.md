# Refrigerator Catalogue
This is a repository for 2022 Team1.

[Health Up Web App](https://healthup-0.web.app/auth/login)

This README contains general information.  
For service-specific documentations, please refer to [React README](react/README.md) or [Django README](django/README.md).

## Resources

jamboard: https://jamboard.google.com/d/1hQ962Ly-KbNQiLvUya-uPap_H-8a0iq9caeOcKUVelg/viewer?f=0
![Screenshot from 2022-10-28 10-50-39](https://user-images.githubusercontent.com/58214906/198449172-c8a4a720-3d8d-4efa-9b07-ca9cca5f2b8e.png)
![Screenshot from 2022-10-28 10-51-28](https://user-images.githubusercontent.com/58214906/198449693-22e9db72-a4fe-4f40-bcef-0e732b4a21f3.png)
![Screenshot from 2022-10-28 10-51-39](https://user-images.githubusercontent.com/58214906/198449709-6b2fb20a-bb3e-4038-9fa3-2578b16f3cfd.png)


database schema version1.2: https://dbdiagram.io/d/635b565d6848d85eee8d27e9
![image](https://user-images.githubusercontent.com/58214906/199888162-91daa17e-a709-49a6-b014-99f957fd4c60.png)

databasae schema version1.0: https://dbdiagram.io/d/635167254709410195a77dd0

member ![image](https://user-images.githubusercontent.com/58214906/199888478-0420426a-05e3-4a72-8aee-095f782d506e.png)


coding rules: https://docs.google.com/document/d/1hcsxrUZsbla35nCRoMQFFRPE8cllPBuCslLoEqq-2p8/edit

gantt chart https://docs.google.com/spreadsheets/d/1DVd-SXJ-Z1dh1WXclT0675OdXHi0kdlpJd5Qjd8MQAU/edit#gid=1984069268

## Prerequisites
- [Docker Desktop](https://www.docker.com/products/docker-desktop/)
  - For Linux users, please install `docker` command instead.
- [VSCode (Visual Studio Code)](https://code.visualstudio.com/download)

<details>
<summary>Note for Windows users</summary>

If you use **Windows**, please clone this repo on [WSL2](https://learn.microsoft.com/en-us/windows/wsl/install)-managed directory (or perhaps WSL is okay) because bind-mounting feature of Docker may not work on the native Windows directory.

</details>


## Launch Dev Environtment Using VSCode *(Recommended)*
<details>
<summary>Initial setup</summary>

### Step 1 (Installing an extension)
Install the [Dev Containers extension](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-containers) for VSCode.

### Step 2 (Copying example config files)
From the project root directory, run the following two commands:
- `cp .devcontainer/devcontainer.json.example .devcontainer/devcontainer.json`
- `cp .devcontainer/docker-compose.yml.example .devcontainer/docker-compose.yml`

### Step 3 (Optional customizations)
You can customize the configuration files as you like.  
For example, you can install `bpython` package that you might use in the integrated shell by uncommenting `postCreateCommand` section of `.devcontainer/devcontainer.json` and replacing `curl` with `bpython`, or using both.  
The command in this section runs after VSCode builds the docker image it extends.  

</details>

### How to start?
- Open the project root directory using VSCode.
- Open the command palette (`Cmd+Shift+P`) and select `Reopen in Container`
  - This should start up the environment. Yay!

<details>
<summary>How does it work?</summary>

VSCode looks in `.devcontainer/devcontainer.json` for configurations.  
The first Docker-Compose configuration file under `"dockerComposeFile"` section is started (after building them, if not done yet) by VSCode.  
The second Docker-Compose configuration file specifies the overrides we want for the Dev Container. The example file mounts the project root directory `../` (note this is relative to the first Docker-Compose configuration file) into `/app` in the containers.  
Back in `.devcontainer/devcontainer.json`, `"service"` section defines the service you want VSCode to extend. Meaning, the service you want to work on at that time (debug, develop, etc). The integrated shell inside VSCode and all the directories you see when working with Dev Containers are using this container.

</details>

### How to access?
|     Service    | Port |          URL          |
|:--------------:|:----:|:---------------------:|
|      React     | 3000 | http://localhost:3000 |
|   JSON-Server  | 3001 | http://localhost:3001 |
|     Django     | 8000 | http://localhost:8000 |
| Django (debug) | 9000 | http://localhost:9000 |
|   PostgreSQL   | 5342 | http://localhost:5432 |


### How to debug?
An exmaple configuration file for debugging Django is provided in `.vscode/launch.json.example`  
This uses port 9000 to avoid conflicts.  
Copy this file as `.vscode/launch.json` and you can start debugging!
- `cp .vscode/launch.json.example .vscode/launch.json`


## Alternative: Launch Dev Environtment Using Docker-Compose
Go to `docker/` directory and run `docker compose up -d` to launch the development environment (`-d` flag defines the run in detached mode, non blocking the terminal).  
You can stop the containers by running `docker compose down` in the same directory.  
Note that the last command will not delete container images as well as defined volumes.


## FAQ

<details>
<summary>
How to switch between React and Django in Dev Container? 🤔
</summary>

It's simple!  
You can just change the `"service"` value in `.devcontainer/devcontainer.json` to `"react"`, for example, and select `Dev Containers: Rebuild Container` or `Dev Containers: Reopen in Container` from the command pallete.  

</details>

<details>
<summary>
Dev Container does not start somehow 🤨
</summary>

Instead of using `Dev Containers: Reopen in Container`, try `Dev Containers: Rebuild Container without Cache and Reopen in Container` (`without Cache` might not be necessary though).  
If this does not solve the problem, you can try running `docker system prune` (with perhaps `--force` option).  

</details>

<details>
<summary>
pip-installed package is lost when I restart the Dev Container 🙃
</summary>

Installation inside the container does not persist after the container is removed.  
To persist the installation, please update `django/requirements.txt` (e.g., by `cd` into Django folder and using `pip freeze` from the container terminal).  

As a side note, packages installed inside `"react"` container should persist if you run `npm install {{package_name}}` in `/app/react` directory.  
This is because `npm install` automatically updates the `package.json` and `package-lock.json` files, which are used when (re-)building the react image.

</details>


## Branching Strategy

We use the following branches.

- `main`
- `develop`
- `username/xxx`
- `release`

<details>
<summary>
Working with your own branch
</summary>

Typical procedures are as follows:
- Update the `develop` branch.
  - `git checkout develop && git pull origin develop` 
- Create your own branch from `develop`.
  - `git checkout -b username/feature-you-want-to-implement`
- Make commits in your own branch.
- When you finish your implementation, push your branch to GitHub.
  - `git push origin username/feature-you-want-to-implement`
  - **PLEASE DO NOT PUSH YOUR CODR DIRECTLY TO THE** `develop` **BRANCH.**
- Visit the repo on GitHub and create a pull request into the **develop** branch.
  - Ask others for review!
- Upon review approval, your branch finally gets merged into the develop branch! Congrats! 🎉

</details>

<details>
<summary>
Release operations
</summary>

`release` branch is used for release-related modificaions.  
`main` branch hosts the stable source code that is running on the production environment

- Create `release` branch from `develop`.
- Make some modifications, if necessary, so that our app runs correctly in the production environment.
- Merge `release` branch into `main`.

</details>
