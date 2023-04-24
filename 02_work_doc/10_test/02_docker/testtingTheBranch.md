# Testing the merged Branch
Hint: The docker-compose project was developed under the docker-compose version 2.15. If you are using 
an older docker-compose version make sure to upgrade your Docker-compose to a version newer or equal to 2.15.
## Preparation of the Project:
First, the `.env`-file has to be edited. The `.env.example`-file should be copied into 
a file called `.env`-file:
```
    cp .env.example .env 
``` 

In case you use windows: 
```
    copy .env.example .env 
``` 
Open the `.env`-file with a editor of your choice and edit the `PATH_WEBCENTRAL_SRC` to the absolute path of the root-directory of webcentral-repo.
Furthermore, copy the `.sql`-file, which holds the dump of the database you want to import,
into `postgres/` and specify the filename of the `.sql` as `DATABASE_PLAIN_SQL_FILE`.
If you also want the media-images to be loaded you need the media-files to be located inside 
`01_application/webcentral_app/media`. If you don't care if the images are present, you don't have to do anything.
## Testing the Production-Docker environment
First, make sure, that all volumes are deleted. Change directory into the root-webcentral-git-repo (directory where the docker-compose.yml files are located) and execute
```
    docker-compose -f docker-compose.yml -f docker-compose.prod.yml down --volumes
```
Starting the Docker-production Environment:
```
    docker-compose -f docker-compose.yml -f docker-compose.prod.yml up --build
```
Check if any container exits after creation
Since we deleted the volumes with the `down --volumes`-command, the website should be 
completely empty. It shouldn't have a user or a admin or any data inside the admin panel or the "Digitale Werkzeuge"-Tab.
Lets populate the database. In a new terminal, cd into root-directory of the repository.
Make sure, that the docker-compose app is still executed in a separate terminal!

```
    bash postgres/restoreDB.sh
```
This should load the database, perform a migration and create a superuser with the credentials specified in `.env` in `DJANGO_SUPERUSER_USERNAME` and `DJANGO_SUPERUSER_PASSWORD`

Check if website is accessible under `http://127.0.0.1:8070`
## Testing the Development-Docker environment
Start the development environment with
```
    docker-compose -f docker-compose.yml -f docker-compose.dev.yml up --build
```
Check again if any error occur during initialisation, e.g. if container exit. Further check if website is accessible through `http://127.0.0.1:8000`. The database should still be filled, since you loaded the database in the production-test.
Now stop execution of the docker-compose app with `ctrl+c` and remove the volumes with
```
    docker-compose -f docker-compose.yml -f docker-compose.dev.yml down --volumes
```
Restart the docker-development environment:
```
    docker-compose -f docker-compose.yml -f docker-compose.dev.yml up --build
```
The website should be empty now. Use the `restoreDB.sh`-script to populate the database and make a django-migration. This step needs to be done in a separate terminal, while the docker-compose dev-environment is still running:
```
    bash postgres/restoreDB.sh
```
It should be possible to login with the superuser-credentials from the .env file. Furthermore the ptj-user should be useable, and the website should be populated with the data from the dump-file.
## Testing App Usage without docker
When using the app without docker, it is necessary to override the settings inside settings.py.
For that a file called `local_settings.py` needs to be placed inside `01_application/webcentral_app/webcentral_app`. Here the database-credentials need to be set for an existing database on the local host. The file should contain something similar like 
```
    from pathlib import Path

    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': 'Empty_Database',
            'USER': 'postgres',
            'PASSWORD': 'Anthem2018',
            "HOST": "localhost",
        }
    }
    SECRET_KEY = "django-insecure-l6nvsp#y_3o8--2^h5@903kz%_yx_0=l+i%(2kllzhb=@3+ar("
    DEBUG = True

    BASE_DIR = Path(__file__).resolve().parent.parent
    STATIC_ROOT= Path.joinpath(BASE_DIR, 'static')
    STATIC_URL = '/static/'
    STATICFILES_DIRS = [
        Path.joinpath(BASE_DIR, 'webcentral_app/static')
    ]
    # Media folder settings
    MEDIA_ROOT=Path.joinpath(BASE_DIR,'media')
    MEDIA_URL = '/media/'
```

When the local_settings.py is present, start the django-development server from the git-root-directory. 
The python-dependencies need to be present for the application to work. For that, a python virtual environment needs to
be created. For that, in a Directory of choice the following command has to be executed:
```
    python3 -m venv venv
```
This creates a virtual environment with the name `venv`. Activate the environment by
```
    . venv/bin/activate
```
Navigate to the webcentral-folder and change directory into `01_application`. There, the python dependecies have to be installed in the virtul environment with the command:
```
    pip install -r requirements.txt
```
Now, the django application can be executed with the command: 
```
    python3 webcentral_app/manage.py runserver 
```
Now the app should be accessible over http://127.0.0.1:8000
