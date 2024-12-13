import pandas as pd
from django.db import models

from tools_over.models import Tools
from .models import Dataset
from common.data_export import AbstractDataExport

class DataExport(AbstractDataExport):
    """ """

    SEPARATOR_M2M = ";;"
    MAPPING_ORM_TO_XLSX = {
        "name": "name",
        "applicationArea": "applicationArea",
        "focus": "focus",
        "classification": "classification",
        "lifeCyclePhase": "lifeCyclePhase",
        "scale": "scale",
        "targetGroup": "targetGroup",
        "alternatives": "alternatives",
        "developmentState": "developmentState",
        "provider": "provider",
        "resources": "resources",
        "availability": "availability",
        "coverage": "coverage",
        "accessibility": "accessibility",
        "resolution": "resolution",
        "description": "description",
        "furtherInformation": "furtherInformation",
        "license": "license",
        "licenseNotes": "licenseNotes",
        "image": "image",
        "lastUpdate": "lastUpdate",
        "released": "released",
        "releasedPlanned": "releasedPlanned",
        "yearOfRelease": "yearOfRelease",
        "programmingLanguages": "programmingLanguages",
        "specificApplication": "specificApplication",
    }

    DATA_APP_DIR = "02_tool_over"
    EXPORT_MODEL = Dataset
