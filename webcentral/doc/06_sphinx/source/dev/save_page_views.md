# Page views
The Wissensplattform comes with a small metrics site in the admin panel, where the page views by day can be seen. 
The page views are calculated from the number of initiated sessions from the Django-Session system. Each session is saved in the backend database in a table called Sessions. When importing a new dump, the session data is overwritten. 
To not loose the session data it has to be exported from the website and imported in the database before creating a dump.
To just export the session-data toa json-file the `dumpdata` django-management command is used:
```
    python manage.py dumpdata sessions > page_views_04_08_2024.json
```
On your local development instance remove all session data. At first open the django shell:
```shell
   ./run shell
```
Inside the shell, import the `Session`-model:
```python
from django.contrib.sessions.models import Session
```
Remove the session data:
```python
Session.objects.all().remove()
```
After that, copy the dumped page-views to your local system and move the file to a location where django can access it (e.g. at `01_application/webcentral_app/`). After that, include the session data into the database of your local web instance:
```shell
python manage.py loaddata page_views_04_08_2024.json
```
Now the page views from the website should have been imported into the local database and a dump can be created.
