<img src="img/wissensplattformLogo.svg" style="width:50%;">
![Wissensplattform]()
# WenDE – Knowledge Platform for Sustainable Digitalization Strategies in Energiewende Construction

The shift from a traditional supply infrastructure to a regenerative, decentralized energy system introduces increased complexity and necessitates the integration of previously independent sectors. The efficient operation of these systems relies on modern IT communication and control technologies. This transition poses significant changes and new challenges for all stakeholders, alongside a substantial need for research.

Research, development, and innovation projects in the field of Energiewende construction, as well as real-world energy transition laboratories, focus on various aspects of this multifaceted topic. They conduct in-depth analyses of the economic, political, and user-specific requirements and challenges.

A key objective of the WeNDE project is to simplify and disseminate the findings from these projects. The EWB knowledge platform is being developed as a central element of this initiative. It serves as a repository where knowledge is aggregated and tailored for different user groups. The platform emphasizes the visual presentation of data, examines the impacts of varying conditions, and facilitates the application of technological advancements. It also involves the verification of digital tools and supports the testing and development of new methodologies.
web interface with data base system of project infromation of the "Begleitforschung Energiewendebauen 2020" (focus modul digitalization).

# Main concept
The Web-Application consists of 3 services, which are containerized, each of them living in a seperate container. In the backend the python based `Django`-Framework is used. Data is stored in a relational-database, whereby as a DBMS `PostgreSQL` is chosen. A `nginx`-instance is used as reverse-proxy to redirect HTTP-requests to the `Django`-Backend, using the `uwsgi`-protocol. Static-content is directly served by `nginx`, since it has access to a `Docker`-Volume, which is shared with the `Django`-application.
![Structure of the Project](./img/dockerComposeDeploymentStructure.png)

To start all needed services, networks and volumes Docker-compose can be used. Thereby it is possible to start it in development- or production-mode. As a prerequesite, the `.env.example`-file needs to be reviewed. It contains the secrets of the application. Please change the values of the environmental-variables inside there. E.g. the `DJANGO_SUPERUSER_USERNAME` contains the username, which can be used to access the admin-panel and `DJANGO_SUPERUSER_PASSWORD` is the corresponding password. With the `POSTGRES_*`-variables a database with the name `POSTGRES_DB` together with a database-user `POSTGRES_USER` is created on the first startup of the Application. The created database lives in the volume `pgdata`. When changing the values of the `POSTGRES_*`-variables after database creation, it wont be possible for the web-application to access the database. 
As a first step a `.env`-file needs to be created from the `.env.example`-file. On linux, that can be done with the `cp`-command. From within the project-folder execute the following command in a shell:
```
   cp .env.example .env
   
```
When the app should be started in production-mode, SSL-certificates need to be provided to the `nginx`-instance. The files need to be put into the `proxy/conf/`-folder. If the `conf/`-folder does not exist, it needs to be created. The filename of the SSL-Certificate and the SSL-Certificate Key need to be placed inside the `NGINX_SSL_CERTIFICATE_FILENAME` and `NGINX_SSL_CERTIFICATE_KEY_FILENAME` respectivly. 
After that, the `run`-script can be used to start the project. For the development-mode use:
```
   ./run up dev
```
For the production-mode use:
```
   ./run up prod
```
Now that the app is running it is possible to eighter import dummy-data or start with an empty database.
## Importing Dummy-Data
For importing the dummy-data the `run`-script can be used. Open a seperate terminal, while the app is still running in the first shell and execute:
```
   ./run restore_db postgres/dummy_data.sql
```
That imports the sql-dump from the `postgres`-folder into the database. After that go back to the shell where the web-app is running and stop it by pressing ``CTRL+C` and restart it with the `./run up <env>` command. You can access the web-app UI by going to 
```
   http://127.0.0.1:8000
```
when you started the development environment or 
```
   http://127.0.0.1:PORT_TO_OUTSIDE
```
where `PORT_TO_OUTSIDE` needs to be replaced by the port, which is set in the `.env`-file.
## Starting the App with an empty database
Leave the app running in the terminal and open another one. There run the following to commands:
```
   ./run makemigrations
```
and 
```
   ./run migrate
```
after that, restart the app from within the first terminal by pressing `CTRL+C` and run the command `./run up <env>` again.
# Hosted 
- https://wissen-digital-ewb.de

## License / Copyright

This repository is licensed under [MIT License](https://mit-license.org/). 

# work docs
 - in ~/Nextcloud/Shared/Digitale_Vernetzung/02_Assis/03_Projekte/DVG0001_BMWi_Wende/08_gemeinsames_Arbeiten/09_Wissensplattform_M4
 - actual folder structure:
├── 01_Backup_Server_DB
├── 02_Backup_lokal_Falk
├── 03_vServer
├── 04_Dokumentation
│   ├── 01_styleGuides
│   └── 02_technicalTutorials_helpers
├── 05_input_ioew
│   └── 2023-02-09-Swanje-EMail
├── 06_BIM2Sim
├── 09_DB_ERM_drawio
│   └── 99_Archiv
├── 10_Zugang_Server
├── 12_media_backup
│   └── media
├── 13_Templates
│   ├── Around
│   └── eduport_v1.1.0
└── 99_Archiv
    ├── 2022_07_14_Archiv
    └── 2023-06-27_CleanUp_WorkDoc

# Funding
![Alt text](./img/BMWi_Logo_2021.svg)

We gratefully acknowledge the financial support by the Federal Ministry for Economic Affairs and Climate Action (BMWK), promotional reference: 03EWB004A 
