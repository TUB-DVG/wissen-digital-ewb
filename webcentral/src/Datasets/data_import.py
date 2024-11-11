from common.data_import import DataImport

class DataImportApp(DataImport):
    DJANGO_MODEL = "collectedDatasets"
    DJANGO_APP = "Datasets"
    MAPPING_EXCEL_DB_EN = {
        # "name_en": "name_en",
        "shortDescription__en": "shortDescription_en",
        "userInterfaceNotes__en": "userInterfaceNotes_en",
        "licenseNotes__en": "licenseNotes_en",
        "furtherInformation__en": "furtherInformation_en",
        "provider__en": "provider_en",
        "yearOfRelease__en": "yearOfRelease_en",
        "lastUpdate__en": "lastUpdate_en",
        "classification__en": "classification_en",
        "resources__en": "resources_en",
        "applicationArea__en": "applicationArea_en",
        "provider__en": "provider_en",
        "usage__en": "usage_en",
        "lifeCyclePhase__en": "lifeCyclePhase_en",
        "targetGroup__en": "targetGroup_en",
        "userInterface__en": "userInterface_en",
        "focus__en": "focus_en",
        "scale__en": "scale_en",
        "accessibility__en": "accessibility_en",
    }       

