# Create a dump for for the repository
This guide explains the workflow of loading

## Import new data

## Removing session data from the database
When uploding a dump to the repository it should be cleaned from personal data. That also includes session-data.
Ensure that the `EWB Wissensplattform` is running. In a seperate terminal start the `django` shell from the root of the project repository using the following command:
```
./run shell
```
Import the session model:
```
from django.contrib.sessions.models import Session
```
Remove all session-objects:
```
Session.objects.all().delete()
```
You can now close the shell using `CTRL+C`.

## Create a dump
The following command creates a SQL-dump and puts the file into the `postgres/`-folder.
```
./run dump_db postgres/new_dump.sql
```
This dump can now be included into the git repository.
