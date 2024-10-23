# Getting started
This document describes the basic setup process for the development environment of the EWB-Wissensplattform. It is intended to acclimatize the user with the project. Please consult the developer documentation for a more in-depth view.

To start the EWB-Wissensplattform the tools docker and docker-compose are needed. Please read the installation manual on the `docker website <https://docs.docker.com/engine/install/>`_ for your operating system. Furthermore `node.js` is needed. It can be downloaded from the official website: https://nodejs.org/en/download/package-manager. Please install the latest LTS-version.

```{note}
We have tested the web application on linux, macOS and windows. However if you are not working on linux you need to install the `Bash`-shell, since bash-scripts are used as utilities and as a entry-point to the application. One way to install Bash is when installing `git under windows <https://gitforwindows.org/>`. In the following guide, linux commands are used. Please execute these commands in your installed Bash-shell. 
```
1. Please clone the repository to a local location of your choice. 
2. Create a .env-file from the the .env.example file.
```
  cp .env.example .env
```
3. Execute the command `npm install` to install the `node.js`-dependencies these are used to transpile the `scss`-stylesheets into a bundled `css`-stylesheet.
4. Build the development environment execute:
```
    ./run build_initial dev
```
To interact with the web application a bash script with the name `run` is used. This script is used to interact with the application.  

4. In the `Wissensplattform` images like logos of in the database included tools, are not located in the repository. These files have to be downloaded from the following link `https://tubcloud.tu-berlin.de/f/3546499069`. The `media`-folder has to be copied to `webcentral/src/media/`.

5. In a last step the database needs to be populated with data. For that a database dump is located inside the repository under `postgres/` with the extension `.sql`.
```{warning}
Please note that the filename of the database dump may change. Please look for the latest file with the extension `.sql` in the `postgres/`-folder.
```

Start the setup process by calling the run script with the argument `up_initial` and providing a database dump file.
```
  ./run up_initial dev postgres/filename.sql
```
After the data has been imported into the database, the web-application should restart and run in the terminal. You can now access the web-application via your favorite web browser via `http://127.0.0.1:8000`. 
```{note}
Please note that you are running the development version of the application. That version is sufficent to run on your local machine and is optimized for development. If you wish to deploy the application in a server environment please read [production](production) site. 
```

