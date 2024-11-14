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
Each `DataImportApp` holds a `getOrCreate`-method, which holds the logic for importing the structured data of the data file into the django ORM model. As arguments it gets the data as a list of rows and the header as a list of header name strings.
These 2 data structures are then processed and objects of the corresponding ORM-model are instantiated. The process can be described as the following:
1. Process the row-data and bring it in a dictionary form, whereby each key of the dictionary corresponds to a attribute of the ORM model where it should imported to. If a field is a `ManyToManyField` objects of the corrsponding ORM-class are instantiated.
2. Instantiate the ORM-class from the dictionary. That will create an object of type e.g. `Tools` or `Dataset` but it wont be saved in the database until `save()` is called on the object.
3. Search in the database if a item with the given `name` is already present in the database.
4. Compare the fields of the newly created object and the object present in the database. If they are not equal, save the new object with the `id` of the old object and remove the old object from the database. Furthermore update the `ManyToManyField`-relations to the relations of the ones from the new model. Serialize the old object into JSON and save it in the `History` model.

# Update of an item
When using the bulk import with a structured data file, the items in the database are automatically updated to the state of the data inside the data file. The old state of an item is saved in a `History`-model in each app. There, the item is saved as a stringified JSON object. That allows to easily rollback to the old state, if the data-import did not work as expected. 
The following section describes the process of the `data_import` and how the update works in general.

