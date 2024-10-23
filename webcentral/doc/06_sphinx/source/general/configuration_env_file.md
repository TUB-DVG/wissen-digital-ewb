# Configuration using .env file
One location to do global configuration for the `EWB Wissensplattform` is a `.env`-file. With this file environmental variables and secrets can be loaded into the application. In that way a central place for configuration is used. Furthermore secrets are not hardcoded in the source code and could be potentially be visual publicly on github. 
```{note}
A .env needs to be present in the root of the project repository, since values from the file are directy used inside the application.
```
## Create a .env-file
The `.env`-file can be created from the example simple `.env.example`. This can be done using the shell:
```bash
cp .env.example .env
```

## Description of used environmental variables
In the following section a description of the used environmental variables is presented:

### Django superuser credentials:

The following environmental variables specify the credentials for a `django` superuser account. 
```
DJANGO_SUPERUSER_PASSWORD=adminPassword
DJANGO_SUPERUSER_USERNAME=admin
DJANGO_SUPERUSER_EMAIL=example@hallo.com
```
These credentials allow the login into the admin panel. In local development the panel can be reached via `http://127.0.0.1:8000/admin`.
```{note}
An update of the superuser credentials in the .env-file results in the deletion of the user account with the old credentials and creates a 
superuser with the new credentials.
```

### Database credentials
The database credentials can be set using the following variables:
```
POSTGRES_USER=postgresUser
POSTGRES_PASSWORD=password
POSTGRES_DB=DatabaseName
```
```{note}
On first start-up of the app, a database is created inside the `database` container. These credentials are also used by the `django` container to connect to the database. Changing the credentials after the intialization of the database leads to the app beeing in a failure state since `django` is not able to connect to the database. To create a new database, the old one needs to be deleted following the [interacting with the web app](./interacting_with_the_app.md) page.
```
