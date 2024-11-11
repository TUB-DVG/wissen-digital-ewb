# Data import 
The following document describes the data-import from a developer perspective. It gives inside in the
structure of the source code files and the workflow in the background, when executing the
`data_import` django management command for a specific django app.
## Configuration of DataImportApp
The `DataImportApp` is the django app specific implementation of the `data_import` custom management command.
There it is specified
