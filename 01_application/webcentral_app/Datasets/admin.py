from django.contrib import admin
from .models import * 
from import_export.admin import ImportExportModelAdmin , ImportMixin
from import_export import fields,resources
from import_export.widgets import *



class collectedDatasetsResource(resources.ModelResource,ImportMixin):
    useCaseCategory=fields.Field(
        attribute='useCaseCategory',
        column_name='Kateogrie Anwendungsfall',
        widget=CharWidget()  
    ),
    categoryDataset=fields.Field(
        attribute='categoryDataset',
        column_name='Kategorie Datensatz',
        widget=CharWidget()  
    ),
    reference=fields.Field(
        attribute='reference',
        column_name='Quelle',
        widget=CharWidget()  
    ),
    referenceLink=fields.Field(
        attribute='referenceLink',
        column_name='Link',
        widget=CharWidget()  
    ),
    availability=fields.Field(
        attribute='availability',
        column_name='Verfügbarkeit',
        widget=CharWidget()  
    ),
    coverage=fields.Field(
        attribute='coverage',
        column_name='Geographische Abdeckung',
        widget=CharWidget()  
    ),
    resolution=fields.Field(  
        attribute='resolution',
        column_name='Auflösung',
        widget=CharWidget()  
    ),
    comment=fields.Field(  
        attribute='comment',
        column_name='Kommentar',
        widget=CharWidget()  
    ),
    dataSources=fields.Field(  
        attribute='dataSources',
        column_name='Referenz der Anwendung',
        widget=CharWidget()  
    ),
    shortDesciption=fields.Field(  
        attribute='shortDesciption',
        column_name='Beschreibung',
        widget=CharWidget()  
    ),
    includesNonResidential=fields.Field(  
        attribute='includesNonResidential',
        column_name='Enthält Nichtwohngebäude',
        widget=CharWidget()  
    ),


    class Meta:
        model   =   collectedDatasets
        import_id_fields = ['useCaseCategory']
        skip_unchanged = True
        report_skipped=False

class collectedDatasetsAdmin( ImportExportModelAdmin,ImportMixin,admin.ModelAdmin):
    
    resource_class = collectedDatasetsResource

admin.site.register(collectedDatasets,collectedDatasetsAdmin)

# Register your models here.