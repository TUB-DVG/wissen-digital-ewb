# Project repository structure
On this page the structure of the project repository is described. 

The root folder of the project contains global configuration files, text files for the interested github user and the `run`-script as a way to interact with the application. Furthermore 3 folders are present, namly `webcentral/`, `postgres/` and `nginx/`, which correspond to the basic docker containers of the application. These folders contain the files, which are relevant to the specfic containers. Their content is summarized briefly in the following sections.

## webcentral-folder
This folder contains the content relevant for the `django` application container. Inside `webcentral/` are 3 folders: `src/`, `doc/`, `test/`.
The `src/`-folder holds the source code of the django-application. The `doc/`-folder contains the collected data, which was imported into the database in spreadsheet files.

### Structure of the src-folder
Below the `src/`-folder lies a typical `django`-project structure (For more information, visit [django-documentation](https://docs.djangoproject.com/en/5.1/)). In that folder also the general `django` management-script `manage.py` is located, which can be used to interact with the `django` project. 
