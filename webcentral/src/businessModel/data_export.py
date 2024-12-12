from common.data_export import AbstractDataExport
from businessModel.models import BusinessModel


class DataExport(AbstractDataExport):
    """ """

    SEPARATOR_M2M = ";;"
    MAPPING_ORM_TO_XLSX = {
        "challenge": "challenge",
        "shortDescription": "shortDescription",
        "property1": "property1",
        "property1Text": "property1Text",
        "property2": "property2",
        "property2Text": "property2Text",
        "property3": "property3",
        "property3Text": "property3Text",
        "property4": "property4",
        "property4Text": "property4Text",
        "property5": "property5",
        "property5Text": "property5Text",
        "imageIcon": "imageIcon",
        "imageIconSelected": "imageIconSelected",
    }

    DATA_APP_DIR = "10_business_models"
    EXPORT_MODEL_OBJ = BusinessModel
