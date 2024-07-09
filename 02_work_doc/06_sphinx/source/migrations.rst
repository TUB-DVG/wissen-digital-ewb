Django - Migrations
-------------------

Django provides a ORM (Object relational mapping), which abstracts the database structure. Entities of the relational database will be accessible as python objects. 
Furthermore, django handles the database management. For Datamodels, which are created in a `models.py`, the corresponding database-tables are created and modified.

If the datamodels inside a `models.py` is modified, django needs a way of keep track of these changes. For that migrations are created.
These are python-files, which hold track of the modifications. 

When model changes have been done in one of the django apps the command 
```
  ./run makemigrations
```
needs to be performed to create the migrations. When new migrations have been created, they can be applied with the following command:
```
   ./run migrate
```
Please note: The migrations should be seen as regular source code files, which need to be tracked by the version control system. When files are not beeing tracked it can lead to errors and inconcistencies, if migration-files are missing. If migration-files are lost or a inconcistent migration state is present, one way to reset the migration-system is to fake a initial migration.
Django

