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
The command gets 3 arguments. `app_label` specifies the app-label, which holds the model into which the data should be imported. the app-label is the name of the folder in which the corrsponding model lies. Please notethat the data import is only working, if a `data_import.py` is present in the specified app folder. Please note further, that the structured data needs to have the right structure for a successfull data import. That means, that the columns in the excel need to have the name, which is used in the app-specific data-import-script. Please consult the data-folder to inspect the needed structure of the execl file.
`path_to_xlsx_or_csv` specfies the path to a .csv- or .xlsx-file, which holds the structured data. 
`path_to_diff_file` is the path, where a diff-file is saved. It is only created on collisions and will be explained in detail here (link to execute_db_changes).
The structure of the implemented python scripts is as follows: In the app `common`, which holds code used across apps. It is placed under `common/data_import.py` and holds a class `DataImport`. This class handles general functionality, which is used by the app-specfic data-import classes like e.g. reading a file. The app-specific data-import classes are located in each app in the file `data_import.py`. Each of theses files holds a class `DataImportApp`, which inherits from the general `DataImport`. 
```{mermaid}
classDiagram
    common_DataImport <|-- use_cases_DataImportApp
    common_DataImport <|-- tools_over_DataImportApp
    common_DataImport <|-- component_list_DataImportApp

    common_DataImport: +importList()
    common_DataImport: +load()
    common_DataImport: +readExcel()
    common_DataImport: -_correctReadInValue()
    common_DataImport: -_selectNearestMatch()
    class use_cases_DataImportApp{
      +getOrCreate()
    }
    class tools_over_DataImportApp{
      +getOrCreate()
    }
    class component_list_DataImportApp{
      +getOrCreate()
    }

```
### Tools import
To import digital tools and digital applications into the database, a excel-file can be used as shown in `/02_work_doc/01_daten/02_toolUebersicht/2024_05_EWB_newToolsImportWithTranslation.xlsx`. The file holds, besides others, the sheets `German` and `English`. The import script scans for these 2 specific sheets and imports the content of the sheet `German` into the fields with the suffices `_de`, while it imports the content of the sheet `English` to the fields with the suffice `_en`. If the two sheets `German` and `English` are not present, it will import the first sheet (the sheet most left, when the file is opened in Excel) into the german fields of the `Tools`. It will not import any present english translations. 

To map the english translation from the sheet `English` onto the model fields the same header names are used as in the sheet `German`. When the data is imported, the 2 sheets ge merged into one list datastructure. To differantiate between german and english fields, the header names of the english fields get the suffice `__en`.
inside the `data_import.py` in the `tools_over`-app a dictionary `MAPPING_EXCEL_DB_EN` is defined as a class-attribute. That datastructure holds the name of the imported english header as key and the corresponding name of the ORM-model-field as value. For `Tools` that feels redundant at the moment since each key-value-field differs only in one `_`, but it can be used in other model-import-scripts if the headername differs from the ORM field name.

# Tracking differences after data-import

