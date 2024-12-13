import pandas as pd
from django.db import models

from protocols.models import Protocol
from common.data_export import AbstractDataExport


class DataExport(AbstractDataExport):
    """ """

    SEPARATOR_M2M = ";;"
    MAPPING_ORM_TO_XLSX = {
        "name": "name",
        "focus": "focus",
        "classification": "classification",
        "lifeCyclePhase": "lifeCyclePhase",
        "scale": "scale",
        "targetGroup": "targetGroup",
        "alternatives": "alternatives",
        "developmentState": "developmentState",
        "furtherInformation": "furtherInformation",
        "released": "released",
        "provider": "provider",
        "resources": "resources",
        "license": "license",
        "accessibility": "accessibility",
        "programmingLanguages": "programmingLanguages",
        "description": "description",
        "specificApplication": "specificApplication",
        "technicalStandardsNorms": "technicalStandardsNorms",
        "yearOfRelease": "yearOfRelease",
        "usage": "usage",
        "associatedTools": "tools",
        "communicationMediumCategory": "communicationMediumCategory",
        "supportedTransmissionMediuems": "supportedTransmissionMediuems",
        "associatedStandards": "associatedStandards",
        "networkTopology": "networkTopology",
        "security": "security",
        "bandwidth": "bandwidth",
        "frequency": "frequency",
        "range": "range",
        "numberOfConnectedDevices": "numberOfConnectedDevices",
        "dataModelArchitecture": "dataModelArchitecture",
        "discovery": "discovery",
        "multiMaster": "multiMaster",
        "packetSize": "packetSize",
        "priorities": "priorities",
        "price": "price",
        "osiLayers": "osiLayers",
        "buildingAutomationLayer": "buildingAutomationLayer",
        "exampleProject": "exampleProject",
        "image": "image",
        "programmingLanguages": "programmingLanguages",
    }

    DATA_APP_DIR = "18_protocols"
    EXPORT_MODEL_OBJ = Protocol
