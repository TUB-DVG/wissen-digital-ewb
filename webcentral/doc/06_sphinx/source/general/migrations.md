# Django - Migrations

Django provides a ORM (Object relational mapping), which abstracts the database structure. Entities of the relational database will be accessible as python objects. 
Furthermore, django handles the database management. For Datamodels, which are created in a `models.py`, the corresponding database-tables are created and modified.

If a datamodel inside a `models.py` is modified, django needs a way of keeping track which changes it already executed inside the database. For that migrations are created.
These are python-files, which hold track of the modifications of the relational-database. 

When model changes have been done in one of the django apps the command 
```
  ./run makemigrations
```
needs to be performed to create the migrations. When new migrations have been created, they can be applied with the following command:
```
   ./run migrate
```
```{note}
The migrations should be seen as regular source code files, which need to be tracked by the version control system. When files are not beeing tracked it can lead to errors and inconcistencies, if migration-files are missing. If migration-files are lost or a inconcistent migration state is present, one way to reset the migration-system is to fake a initial migration.
```
## Workaround for missing migrations 
When migration-files are missing and `makemigrations` is called, django re-creates a migration-file with the already executed changes. When executing `migrate` afterwards the relational database throws an error, since the attribute already exists. To fix this state, call the following commands:
```
   python manage.py makemigrations <app_name>
```
```
  python manage.py migrate <app_name> --fake-intial
```
That will mark all existing attributes as created and the migration-system can be used without errors again. Please make sure, that no newly added attributes are present in the `models.py` of the app of which the migrations should be fixed.

 ## Updating models
Sometimes it is needed to update the models, e.g. when it is needed to change the data format or edit the name of a field. 
The workflow for updating is as follows:
1. Update one field of the `models.py`
2. Check if that field is mentioned in the corresponding `translation.py`. If so, comment it.
3. Run `makemigrations`: If the name of a attribute has changed, a prompt should appear, which asked if the name was changed from the old name to the new name.
```{note}
If changes are not detected by the migration-system. Try to run the `makemigrations` command with the app-name.
```
4. Run the `migration`-command.
