from django.db import models

from common.data_import import DataImport
from businessModel.models import BusinessModel, History


class DataImportApp(DataImport):
    """App specfific data-import class for the `Datasets`-app.


    Attributes:
        MAPPING_EXCEL_DB: dict
            Describes the mapping from a column in the xlsx-file to a attribute
            of the `collectedDatasets` data-class.

    """

    DJANGO_MODEL = "BusinessModel"
    DJANGO_MODEL_OBJ = BusinessModel
    APP_HISTORY_MODEL_OBJ = History
    DJANGO_APP = "businessModel"

    MAPPING_EXCEL_DB = {
        "challenge": ("challenge", None),
        "shortDescription": ("shortDescription", None),
        "property1": ("property1", None),
        "property1Text": ("property1Text", None),
        "property2": ("property2", None),
        "property2Text": ("property2Text", None),
        "property3": ("property3", None),
        "property3Text": ("property3Text", None),
        "property4": ("property4", None),
        "property4Text": ("property4Text", None),
        "property5": ("property5", None),
        "property5Text": ("property5Text", None),
        "imageIcon": ("imageIcon", None),
        "imageIconSelected": ("imageIconSelected", None),
    }

    MAPPING_EXCEL_DB_EN = {
        "challenge__en": "challenge_en",
        "shortDescription__en": "shortDescription_en",
        "property1__en": "property1_en",
        "property1Text__en": "property1Text_en",
        "property2__en": "property2_en",
        "property2Text__en": "property2Text_en",
        "property3__en": "property3_en",
        "property3Text__en": "property3Text_en",
        "property4__en": "property4_en",
        "property4Text__en": "property4Text_en",
        "property5__en": "property5_en",
        "property5Text__en": "property5Text_en",
        "imageIcon__en": "imageIcon_en",
        "imageIconSelected__en": "imageIconSelected_en",
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

        obj = self.DJANGO_MODEL_OBJ(**readInValues)
        tupleOrNone = self._checkIfItemExistsInDB(
            row[header.index("challenge")], "challenge"
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
