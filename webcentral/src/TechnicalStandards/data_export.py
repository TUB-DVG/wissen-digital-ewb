import pandas as pd
from django.db import models

from .models import Norm
from common.data_export import AbstractDataExport


class DataExport(AbstractDataExport):
    """ """

    SEPARATOR_M2M = ";;"
    MAPPING_ORM_TO_XLSX = {
        "name": "name",
        # "isNorm": "isNorm",
        "title": "title",
        # "image": "image",
        "link": "link",
        "shortDescription": "shortDescription",
        "source": "source",
    }

    DATA_APP_DIR = "05_technical_standards"
    EXPORT_MODEL_OBJ = Norm
