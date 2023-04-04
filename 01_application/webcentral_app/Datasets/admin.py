from django.contrib import admin
from .models import * 
from import_export.admin import ImportExportModelAdmin 
from import_export import fields,resources
from import_export.widgets import *



class collectedDatasetsResource(resources.ModelResource):

    nameDataset=fields.Field(
        column_name='Name des Datasets',
        widget=CharWidget()  
    ),
    useCaseCategory=fields.Field(
        column_name='UseCaseKategorie',
        widget=CharWidget()  
    ),
    categoryDataset=fields.Field(
        column_name='Kategorie',
        widget=CharWidget()  
    ),
    
    reference=fields.Field(
        column_name='Quelle',
        widget=CharWidget()  
    ),
    referenceLink=fields.Field(
        column_name='Link',
        widget=CharWidget()  
    ),
    availability=fields.Field(
        column_name='Verfügbarkeit',
        widget=CharWidget()  
    ),
    coverage=fields.Field(
        attribute='coverage',
        column_name='Coverage (GEO)',
        widget=CharWidget()  
    ),
    resolution=fields.Field(  
        attribute='resolution',
        column_name='Resolution',
        widget=CharWidget()  
    ),
    comment=fields.Field(  
        attribute='comment',
        column_name='Comment (Resolution, Quality,..)',
        widget=CharWidget()  
    ),
    dataSources=fields.Field(  
        attribute='dataSources',
        column_name='Datenquellen',
        widget=CharWidget()  
    ),
    shortDesciption=fields.Field(  
        attribute='shortDesciption',
        column_name='Kurzbeschreibung',
        widget=CharWidget()  
    ),
    includesNonResidential=fields.Field(  
        attribute='includesNonResidential',
        column_name='Includes Non-Residential',
        widget=CharWidget()  
    ),
    

    class Meta:
        model   =   collectedDatasets
        import_id_fields = ['nameDataset',]
        skip_unchanged = True
        report_skipped = True

class collectedDatasetsAdmin( ImportExportModelAdmin):
    
    resource_class = collectedDatasetsResource

admin.site.register(collectedDatasets,collectedDatasetsAdmin)

# Register your models here.