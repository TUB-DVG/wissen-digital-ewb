from django.db import models

from common.data_import import DataImport
from tools_over.models import (
    ApplicationArea,
    Classification,
    Focus,
    LifeCyclePhase,
    Scale,
    TargetGroup,
    Accessibility,
)
from project_listing.models import Subproject
from common.models import License
from Datasets.models import Dataset, History


class DataImportApp(DataImport):
    """App specfific data-import class for the `Datasets`-app.


    Attributes:
        MAPPING_EXCEL_DB: dict
            Describes the mapping from a column in the xlsx-file to a attribute
            of the `collectedDatasets` data-class.

    """

    DJANGO_MODEL = "Dataset"
    DJANGO_MODEL_OBJ = Dataset
    DJANGO_APP = "Datasets"
    APP_HISTORY_MODEL_OBJ = History

    MAPPING_EXCEL_DB = {
        "name": ("name", None),
        "applicationArea": ("applicationArea", ApplicationArea),
        "classification": ("classification", Classification),
        "focus": ("focus", Focus),
        "lifeCyclePhase": ("lifeCyclePhase", LifeCyclePhase),
        "scale": ("lifeCyclePhase", Scale),
        "targetGroup": ("targetGroup", TargetGroup),
        "provider": ("provider", None),
        "resources": ("resources", None),
        "coverage": ("coverage", None),
        "resolution": ("resolution", None),
        # "comment": ("comment", False),
        "description": ("description", None),
        "availability": ("availability", None),
        "alternatives": ("alternatives", None),
        "developmentState": ("developmentState", None),
        "description": ("description", None),
        "furtherInformation": ("furtherInformation", None),
        "image": ("image", None),
        "lastUpdate": ("lastUpdate", None),
        "license": ("license", License),
        "licenseNotes": ("licenseNotes", None),
        "accessibility": ("accessibility", Accessibility),
        "yearOfRelease": ("yearOfRelease", None),
        "released": ("released", None),
        "releasedPlanned": ("releasedPlanned", None),
    }

    MAPPING_EXCEL_DB_EN = {
        "name__en": "name_en",
        "applicationArea__en": "applicationArea_en",
        "classification__en": "classification_en",
        "focus__en": "focus_en",
        "lifeCyclePhase__en": "lifeCyclePhase_en",
        "scale__en": "scale_en",
        "targetGroup__en": "targetGroup_en",
        "provider__en": "provider_en",
        "availability__en": "availability_en",
        "coverage__en": "coverage_en",
        "resolution__en": "resolution_en",
        # "comment__en": "comment_en",
        "furtherInformation__en": "furtherInformation_en",
        "lastUpdate__en": "lastUpdate_en",
        "license__en": "license_en",
        "licenseNotes__en": "licenseNotes_en",
        "accessibility__en": "accessibility_en",
        "description__en": "description_en",
    }

    def __init__(self, path_to_data_file):
        """Constructor of the app-specific data_import

        Calls the constructor of the parent class `DataImport`.
        The parent-class then handles the read in process of the
        file, whose file-path was given as `path_to_data_file`.

        path_to_data_file:  str
            Represents the file-path to the Data-File (xlsx or csv).
        """
        super().__init__(path_to_data_file)

    def getOrCreate(self, row: list, header: list, data: list) -> tuple:
        """Gets or Creates an object of type UserIntegration from the data in row

        This method feeds the data present in row into the django
        get_or_create-function, which returns an Object of Type
        UserIntegration according to the fed-data. Either this object
        corresponds to a new created-dataset in the database or
        the existing dataset is returned.

        Parameters:
        row:    list
            A dataset, represented by a list.
        header: list
            list of strings, which represent the header-columns.

        Returns:
        obj:    UserIntegration
            UserIntegration-object, represent the created or in database
            present UserIntegration-Dataset with the data from row.
        created:    bool
            Indicates, if the UserIntegration-object was created or not.
        """
        readInValues = {}
        readInValuesM2M = {}
        for tableTuple in self.MAPPING_EXCEL_DB:
            (tableKey, m2MModel) = self.MAPPING_EXCEL_DB[tableTuple]
            if isinstance(m2MModel, type) and issubclass(
                m2MModel, models.Model
            ):
                m2mList = self._processListInput(
                    row[header.index(tableKey)],
                    separator=";;",
                )
                m2mList = self._iterateThroughListOfStrings(m2mList, m2MModel)
                readInValuesM2M[tableKey] = self.getM2MelementsQueryset(
                    m2mList, m2MModel
                )
            else:
                if row[header.index(tableKey)] == "":
                    readInValues[tableKey] = None
                else:
                    readInValues[tableKey] = row[header.index(tableKey)]

        obj = self.DJANGO_MODEL_OBJ(
            name=readInValues["name"],
            provider=readInValues["provider"],
            resources=readInValues["resources"],
            coverage=readInValues["coverage"],
            description=readInValues["description"],
            availability=readInValues["availability"],
            developmentState=readInValues["developmentState"],
            furtherInformation=readInValues["furtherInformation"],
            image=readInValues["image"],
            lastUpdate=readInValues["lastUpdate"],
            licenseNotes=readInValues["licenseNotes"],
            yearOfRelease=readInValues["yearOfRelease"],
            released=readInValues["released"],
            releasedPlanned=readInValues["releasedPlanned"],
        )

        # check if the database already holds a dataset with the name already
        tupleOrNone = self._checkIfItemExistsInDB(
            row[header.index("name")], "name"
        )
        obj.save()
        for readInM2MKey in readInValuesM2M.keys():
            try:
                getattr(obj, readInM2MKey).set(readInValuesM2M[readInM2MKey])
            except:
                breakpoint()

        if self._englishHeadersPresent(header):
            self._importEnglishTranslation(
                obj, header, row, self.MAPPING_EXCEL_DB_EN
            )
        obj.save()

        if tupleOrNone is None:
            return obj, True

        return self._checkIfEqualAndUpdate(obj, tupleOrNone[1])
