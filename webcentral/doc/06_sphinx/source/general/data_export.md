# Export data
In the following sections it is described how to export structured data for a specific `django` app from the database into spreadsheet files. Thereby the data from the database is exported in files with the tabular structure present in `webcentral/doc/01_data/`. Each of the subsequent folders corespond to a `django` app whereby the different `django` apps are present in the folder `webcentral/src/`.
This approach can be helpful, when data was imported into the database in several ways (via admin-panel, via spreadsheet files etc.) and a central data source is needed for future imports.

## Structure of the source code 
The `data_export` function can be called from the `django` `manage.py` management script. The general structure of the custom management command is written out below:
```bash
python manage.py data_export app-name spreadsheet-filename.xlsx
```
This command starts the `data_export` for one of the `django` apps inside the `webcentral/src/` folder with the name `app-name` and exports a spreadsheet file `spreadsheet-filename.xlsx` into the  `webcentral/src/` folder. 
```{note}
The spreadsheet file will only be visible on the host system when using the development mode of the `EWB Wissensplattform`. If you are using the production mode of the application you need to copy the created .xlsx file manually to the host filesystem.
```
```{note}
It can happen, that it is not possible to open the spreadsheet on the host-system because of insuficient rights. If on a linux-system you can use the `chown` utility to change the file owner to the current OS-user. 
```
## Code structure
Similar to the the `data_import`-structure, a script `data_export.py` inside the folder `webcentral/src/common/management/commands/` is needed to introduce a custom management command `data_export`. It defines a class `CustomCommand`, which inherits from the `BaseCommand` `django` class. In the `CustomCommand` two methods need to be implemented: The `add_arguments()`- and the `handle()`-method, whereby the `add_arguments()` is used to add argument-structure to the command and the `handle()`-method is used to add functionality.
The `handle()`-method then searches the installed `django`-app for the given app in the first argument and loads the `data_export.py`-module inside that app-directory. Inside the app specific `data_export.py`-module a class `DataExport` is definied, which is implemented differently for each app based on the structure of the apps models and the corresponding spreadsheet file.

