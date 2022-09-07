# Notes:
 - There seems to be an issue with decimal fíelds when using the import_export django app, decimal fields always get the update status even when no changes are to be made.
 - It seems to be very important to initialize your model fields with "null=True" 
 - When dealing with foreign key objects without using the foreignKey widget, if the object does not exist, a comparison cannot be made and this causes an issue . A solution found would be to change the attribute for each field in your model resource in the before_import_row function ( they could be changed to none but then no comparison would be made and the GUI would not display anything, another way is to change the attributes to random string : compare to no existing field).
 - Deleting rows from an xlsx or csv  file manually causes the functionality to crash, instead creating a new xlsx file and copying all the data except the row to deleted seems to be a solution.
 - It is recommended to not import large files in one import action(rows exceeding 1000), it would be advised to limit every xlsx or csv file to 500 rows.
 - The import id field must match with the column name (including lower and upper cases).

# Admin page layout:
## General.

To integrate django-import-export with a model, we create a ModelResource class in admin.py that will describe how this resource can be imported or exported:

By default ModelResource introspects model fields and creates Field-attributes with an appropriate Widget for each field.

To affect which model fields will be included in an import-export resource, use the fields option to whitelist fields:
```
class BookResource(resources.ModelResource):

    class Meta:
        model = Book
        fields = ('id', 'name', 'price',)
```
The default field for object identification is id, you can optionally set which fields are used as the id when importing:
```
class Meta:
        model = Book
        import_id_fields = ('isbn',)
        fields = ('isbn', 'name', 'author', 'price',)

```
For more resource customization options :https://django-import-export.readthedocs.io/en/latest/getting_started.html#creating-import-export-resource

## Declaring Fields:
Field represent mapping between object field and representation of this field.
Parameters:	
- attribute : A string of either an instance attribute or callable off the object.
- column_name : Lets you provide a name for the column that represents this field in the export.
- widget : Defines a widget that will be used to represent this field’s data in the export.
- readonly : A Boolean which defines if this field will be ignored during import.
- default : This value will be returned by clean() if this field’s widget did not return an adequate value.
- saves_null_values : Controls whether null values are saved on the object


It is possible to override a resource field to change some of its options:

```
from import_export.fields import Field

class BookResource(resources.ModelResource):
    published = Field(attribute='published', column_name='published_date')

    class Meta:
        model = Book
```

The fields is how we can import different model obejcts through foreign keys:

Example:
```
class TeilProjektResource(resources.ModelResource):
 datenbank=fields.Field(
        attribute='enargus_daten__datenbank',
        column_name='Datenbank',
        widget=CharWidget()  
    )

datenbank is field of a model called Enargus that is is linked through a foreign key 'enargus_daten' to our main model Teilprojekt(the model that we want to mainly import)

The attribute parameter defines what should the data that is found in the column with the name 'Datenbank' for each row in our import file be compared to ( in this case it should be compared to a field, in a model that is linked with the foreign key enargus_daten, that is called datenbank)
```

If the id field or a field that can uniquely identify a particular object of foreign model is present in the import file then to make importing easier the ForeignKeyWidget should be used:

Widget field which looks up a related model using “natural keys” in both export and import.
The lookup field defaults to using the primary key (pk) as lookup criterion but can be customised to use any field on the related model.
Parameters:	    
- model: The Model the ForeignKey refers to (required).
- field: A field on the related model used for looking up a particular object.

Example:
```
widget=ForeignKeyWidget(Author, 'name') (Author is the name of our model and 'name' is our lookup field)
```
If such field is not present in the import file, the import funcionality must be updated, by creating manual inserts to the database at the desired stage of the import process.

The import workflow can be found here: https://django-import-export.readthedocs.io/en/latest/import_workflow.html

One possibility would be to override some of the import functions using the get_or_create django command to update or create new objects for your different models.