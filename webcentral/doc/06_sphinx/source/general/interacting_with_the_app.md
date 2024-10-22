# Interacting with the EWB Wissensplattform
The following document describes how to execute basic management commands like starting or stoping the web application, load database dumps or perform migrations.
For convience a bash-script with the name `run` is provided in the root-folder of the repository. The functionality of it is described in the following sections. Since the script only provides a abstraction to the docker- and django API, the corresponding API commands are also shorty explained.

## Starting the web-application
To start the `EWB Wissensplattform` please start a terminal in the repository folder. After that execute the following command using the Bash-shell:
```{bash}
./run up dev
```
This will start the application in development mode in the terminal foreground. If you would like to start the application in production mode run the following command:
```{bash}
./run up prod
```
```{note}
Please note, that the following command starts the application in the foreground of the terminal. If you close the terminal e.g. you close a ssh-session to a remote server where you would like to keep the applicatio running, it also stops the execution of the web application. In such cases please use the detached mode. 
```
The above provided run-script commands just call the `docker compose <https://docs.docker.com/compose/>` command line tool with configuration files for the development- and production-mode. These files are also located in the root-folder of the project-respository. There is the base file `docker-compose.yml` and the two specific files `docker-compose.dev.yml` for development and `docker-compose.prod.yml` for production.
If the application should be started in development mode using the docker compose command, the following line can be executed:
```bash
docker compose -f docker-compose.yml -f docker-compose.dev.yml up
```
To start the production environement, the following command can be executed:
```bash
docker compose -f docker-compose.yml -f docker-compose.prod.yml up
```
### Running the app in detached mode
Sometimes it can be helpful to run the app dettached from the terminal. To do that please add the `-d` flag to the `docker compose` starting command:
```bash
docker compose -f docker-compose.yml -f docker-compose.dev.yml up -d
```
To start the production environement, the following command can be executed:
```bash
docker compose -f docker-compose.yml -f docker-compose.prod.yml up -d
```
This will dettach the `docker compose` command from the terminal.

## Stoping the application
If you would like to stop the `EWB Wissensplattform` running in the background you can run the `run`-script with the arguments and `down` as a first argument and `dev` or `prod` as a second argument:

The following command stops the development application:
```bash
./run down dev
```
The following command stops the production application:
```bash
./run down prod
```
Alternativly with `compose`:
```bash
docker compose -f docker-compose.yml -f docker-compose.dev.yml down
```
```bash
docker compose -f docker-compose.yml -f docker-compose.prod.yml down
```
```{note}
The `compose` command can only stop the application when executed from within the root of the project repository.
```
If you would like to check, whether a application is running, you can use the following command of the docker API:
```
docker container ls
```
This will print all running containers. If only the `EWB Wissensplattform` in development mode is running, the output should look like the following: 
```
CONTAINER ID   IMAGE                   COMMAND                  CREATED        STATUS                  PORTS                                         NAMES
49f3a623f1a9   webcentral-webcentral   "bash -c 'python3 sr…"   22 hours ago   Up 22 hours             0.0.0.0:8000->8000/tcp, :::8000->8000/tcp     webcentral
0405a7b58636   postgres                "docker-entrypoint.s…"   24 hours ago   Up 22 hours (healthy)   0.0.0.0:5001->5432/tcp, [::]:5001->5432/tcp   database
```
## Removing the content of the database
Sometimes it can happen, that the content of the database needs to be deleted. This can be the case, when another database dump should be loaded. In such a case the first step would be to stop the application and delete the volumes attached to the compose project. This can be done with the following command from the run-script:
```bash
./run delete_db
```
This stops the application and removes all volumes for the app.
Alternativly the `compose` comand line tool can be used:
```bash
docker compose -f docker-compose.yml -f docker-compose.dev.yml down --volumes
```
```bash
docker compose -f docker-compose.yml -f docker-compose.prod.yml down --volumes
```
## Loading a dump into the database
To load a SQL dump file into the database the database needs to be empty. To acomplish that please see [Removing the content of the database](##removing-the-content-of-the-database). Please note that the app is in that state when starting it for the first time.

1. Start the app in development or production mode:
```bash
./run up dev
```
Leave the terminal window with the running app open.
2. Start a seperate terminal and navigate to the location of the project repository. Execute the following command:
```
./run restore_db <path_to_sql_dump/file.sql>
```
Please insert the relative path to the SQL dump file you would like to import.
3. Switch back to the terminal window where `EWB Wissensplattform` is running. Stop it and restart it.
Now the new dump should have been loaded.
