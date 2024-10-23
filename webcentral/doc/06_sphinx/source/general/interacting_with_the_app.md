# Interacting with the EWB Wissensplattform
The following document describes how to execute basic management commands like starting or stoping the web application, load database dumps or perform migrations.
For convience a bash-script with the name `run` is provided in the root-folder of the repository. The functionality of it is described in the following sections. Since the script only provides a abstraction to the docker- and django API, the corresponding API commands are also shorty explained.
## Building the docker images
Before the different parts of the `EWB Wissensplattform` can be started, docker images need to be built, which can then be run as containers. The process of building an image may include downloading and installing dependncies or copying the `Wissensplattform`s source code into the image.
```{note}
The production- und development built work differently when it comes to updates of the source code: In the development-built, the folders of the host-system containing the source-code are mounted into the container. That means, that changes in the source code can directly be seen and a rebuilt of the container is not needed. For the production envoironment this is not the case. That means, that everytime changes to the source code have been made, a rebuilt of the container is needed.
However there are cases were its also needed to rebuild the development-mode. That includes updates of dependecies, since these are usually installed in the image-build stage. 
In situations were the user is not sure if a rebuild is needed or not, a rebuild can just be done. 
```
Prerequisite:
If the stylesheet classes in the *.scss files have been changes a transpiling processes to a css-file is needed. That can be done using the following command in the root of the project-repository:
```
npx webpack --mode=development
```
When building for development or 
```
npx webpack --mode=production
```
when building for production.

To build images of the application using the `run`-script, the following command can be executed to build the development environement:
```
./run build dev
```
To build the production environment the following command can be used:
```
./run build prod
```
There is also an convenience command combining the transpiling from SCSS to CSS and the building process of the images:
For development:
```
./run build_initial dev
```
For production:
```
./run build_initial prod
```
Instead of the run-script the `docker compose`-command can also be used directly:
For development:
```bash
docker compose -f docker-compose.yml -f docker-compose.dev.yml build
```
For production:
```bash
docker compose -f docker-compose.yml -f docker-compose.prod.yml build
```

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
To further simplify the database dump import process the `run` script provides a convenience command, which executes the previously described steps automatically. The command can be called as follows:
```bash
    ./run up_initial dev postgres/webcentral_db_20240927_translation_use_cases_data_sufficiency.sql 
```
This starts the development mode and loads the database dump located in the `postgres/`-folder with the specified name.

## Creating a new dump from the database
To create a new dump, which contains the full database as a plain text file, the following command can be used when in the root folder of the project repository.
```bash
./run dump_db postgres/postgres_dump.sql 
```
This saves the dump in the file `postgres_dump.sql` in the `postgres/` folder.
## Switching into the container-shell
Sometimes it is necessary to attach a shell to a container and work in the container filesystem. This can be the case when it is needed to interact with the django application using the `manage.py` file inside the `webcentral`-container. The run-script provides a command to switch into the container shell:
```
./run webcentral_shell
```
This will open a shell instance inside the container and shell commands can be executed in the container. To exit the container shell `CTRL+C` can be used.
The same can be done using the docker API:
```
docker exec -it webcentral bash
```
This command attaches a interactive bash-session to the docker container with the name `webcentral`.

## Django makemigrations-command
To execute the django management command `makemigrations` the run script can be used:
```
./run makemigrations
```
The equivalent docker and linux commands are described below:
```
docker exec -it webcentral bash
cd src/
python manage.py makemigrations
```
These commands create a container shell-session, change directory into the `src/`-folder and execute the `manage.py`-script with the `makemigrations` attribute.
```{note}
The `makemigrations` command creates `django` migration files, which are located in the app-specific `migrations/`-folder. When running the `Wissensplattform` in developement mode these files will also appear in the host filesystem. However, when in production mode, the migration files are not visible to the host filestytem and need to be copied manually.
```
## Django migrate-command
To execute the `django` `migrate` command the run script can be used:
```bash
./run migrate
```
This is equivalent to the following docker and linux commands:
```
docker exec -it webcentral bash
cd src/
python manage.py migrate
```
These commands create a container shell-session, change directory into the `src/`-folder and execute the `manage.py`-script with the `migrate` attribute.
