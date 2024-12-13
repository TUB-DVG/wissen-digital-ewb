from datetime import (
    datetime,
    timedelta,
)
from django.db import models
import pandas as pd

from common.data_import import DataImport
from common.models import Focus
from .models import (
    Publication,
    Type,
    History,
)


class DataImportApp(DataImport):
    DJANGO_MODEL = "Publication"
    DJANGO_MODEL_OBJ = Publication
    DJANGO_APP = "publications"
    APP_HISTORY_MODEL_OBJ = History
    MAPPING_EXCEL_DB_EN = {
        "title__en": "title_en",
        "abstract__en": "abstract_en",
        "copyright__en": "copyright_en",
        "focus__en": "focus_en",
        # "Kurzbeschreibung der Wirkung__en": "effectDescription_en",
        # "Quelle / Hinweise__en": "furtherInformation_en",
    }
    MAPPING_EXCEL_DB = {
        "title": ("title", None),
        "copyright": ("abstract", None),
        "abstract": ("abstract", None),
        "url": ("url", None),
        "type": ("type", Type),
        "focus": ("focus", Focus),
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

    def getOrCreate(self, row: list, header: list, data: list):
        """create a UseCase object from row and header of a Spreadsheet"""
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
                if m2MModel != Type:
                    readInValuesM2M[tableKey] = self.getM2MelementsQueryset(
                        m2mList, m2MModel
                    )
                else:
                    readInValues[tableKey] = self.getM2MelementsQueryset(
                        m2mList, m2MModel
                    )
            else:
                if row[header.index(tableKey)] == "":
                    readInValues[tableKey] = None
                else:
                    readInValues[tableKey] = row[header.index(tableKey)]

        obj = self.DJANGO_MODEL_OBJ(**readInValues)

        tupleOrNone = self._checkIfItemExistsInDB(
            row[header.index("title")], "title"
        )

        obj.save()
        obj.focus.add(*readInValuesM2M["focus"])
        if self._englishHeadersPresent(header):
            self._importEnglishTranslation(
                obj, header, row, self.MAPPING_EXCEL_DB_EN
            )
        if tupleOrNone is None:
            return obj, True
        idOfAlreadyPresentTool = tupleOrNone[0]
        return self._checkIfEqualAndUpdate(obj, tupleOrNone[1])
