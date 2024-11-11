# Data import 
The following document describes the data-import from a developer perspective. It gives inside in the
structure of the source code files and the workflow in the background, when executing the
`data_import` django management command for a specific django app.
## Configuration of DataImportApp
The `DataImportApp` is the django app specific implementation of the `data_import` custom management command.
There it is specified, how to process the structured data file, which is given as an argument to the `data_import`-command.
The class-constant `MAPPING_EXCEL_DB` maps a column-header of the structured input file to a attribute of the specified django ORM-class.
The following listing shows an example:
```
DJANGO_MODEL = "collectedDatasets"
DJANGO_APP = "Datasets"
MAPPING_EXCEL_DB = {
        "name": ("name", None),
        "applicationArea": ("applicationArea", ApplicationArea),
        "classification": ("classification", Classification),
        "focus": ("focus", Focus),
        "provider": ("provider", None),
}
```
`MAPPING_EXCEL_DB` defines a mapping of the columns `name`, `applicationArea`, `classification`, `focus` and `provider` to the attributes 
`name`, `applicationArea`, `classification`, `focus` and `provider`, which are atributes of the django model class specified in `DJANGO_MODEL`, which lies inside the django app `DJANGO_APP`.   
```{note}
    Only in the specified example the column names and the attribute names are the same. But that is not always the case. You can update the the names of the columns, if the column names differ in your structured data file. If you want to change the names of the django ORM attributes, please check the dev-guide.  
```
