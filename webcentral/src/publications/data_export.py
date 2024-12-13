import pandas as pd
from django.db import models

from publications.models import Publication
from common.data_export import AbstractDataExport

class DataExport(AbstractDataExport):
    """ """

    SEPARATOR_M2M = ";;"
    MAPPING_ORM_TO_XLSX = {
        "type": "type",
        "title": "title",
        "copyright": "copyright",
        "url": "url",
        "abstract": "abstract",
        "focus": "focus",
    }

    DATA_APP_DIR = "publications"
    EXPORT_MODEL_OBJ = Publication
