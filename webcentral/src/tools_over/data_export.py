import pandas as pd
from django.db import models

from tools_over.models import Tools
from common.data_export import AbstractDataExport


class DataExport(AbstractDataExport):
    """ """

    SEPARATOR_M2M = ";;"
    MAPPING_ORM_TO_XLSX = {
        "name": "name",
        "resources": "resources",
        "description": "description",
        "applicationArea": "applicationArea",
        "provider": "provider",
        "usage": "usage",
        "lifeCyclePhase": "lifeCyclePhase",
        "targetGroup": "targetGroup",
        "userInterface": "userInterface",
        "userInterfaceNotes": "userInterfaceNotes",
        "programmingLanguages": "programmingLanguages",
        "frameworksLibraries": "frameworksLibraries",
        "databaseSystem": "databaseSystem",
        "classification": "classification",
        "focus": "focus",
        "scale": "scale",
        "lastUpdate": "lastUpdate",
        "accessibility": "accessibility",
        "license": "license",
        "licenseNotes": "licenseNotes",
        "furtherInformation": "furtherInformation",
        "alternatives": "alternatives",
        "specificApplication": "specificApplication",
        "released": "released",
        "releasedPlanned": "releasedPlanned",
        "yearOfRelease": "yearOfRelease",
        "developmentState": "developmentState",
        "technicalStandardsNorms": "technicalStandardsNorms",
        "technicalStandardsProtocols": "technicalStandardsProtocols",
        "image": "image",
    }

    DATA_APP_DIR = "02_tool_over"
    # EXPORT_MODEL = Tools
    EXPORT_MODEL_OBJ = Tools
