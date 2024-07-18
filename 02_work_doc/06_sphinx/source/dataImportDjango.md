# Data-Import

This document describes the different ways to import data into the webcentral-database.
In general, data can be imported using the following ways:
    
    - Using the django-admin panel.
    - Using the custom django `data_import` command.
    - Using a SQL-dump.

In the following sections these methods are described in detail.

## Data-import using the django admin panel
This approach can be considered straight forward. If only small chunks of data need to be imported this method is apropriate. For that method to work, the django superuser-credentials are needed, which can be found in the `.env`-file in the root project folder.
The admin panel can be entered by either opening your locally hosted version or the server hosted production version. For your local version enter the following link in your browser of choice:
```
http://127.0.0.1:8000/admin
```
On the opened site, enter username and password from the `.env`-file. You should then be able to create, modify or delete 

## Data-import using the data_import command
To import greater numbers of structured data of a specific type, python-scripts has been written. These are accessible through a django custom-command `data_import`. The command can be started using the django `manage.py`:
```
    python manage.py data_import <app_label> <path_to_xlsx_or_csv> <path_to_diff_file>
```
The command gets 3 arguments. `app_label` specifies the app-label, which holds the model into which the data should be imported. the app-label is the name of the folder in which the corrsponding model lies. Please notethat the data import is only working, if a `data_import.py` is present in the specified app folder. Please note further, that the structured data needs to have the right structure for a successfull data import. That means, that the column need to have the right names.
`path_to_xlsx_or_csv` specfies the path to a .csv- or .xlsx-file, which holds the structured data. 
`path_to_diff_file` is the path, where a diff-file is saved. It is only created on collisions and will be explained in detail here (link to execute_db_changes).
The structure of the implemented python scripts is as follows: In the app `common`, which holds code used across apps. It is placed under `common/data_import.py` and holds a class `DataImport`. This class handles general functionality, which is used by the app-specfic data-import classes like e.g. reading a file. The app-specific data-import classes are located in each app in the file `data_import.py`. Each of theses files holds a class `DataImportApp`, which inherits from the general `DataImport`. 
