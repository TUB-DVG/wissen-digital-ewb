from datetime import (
    datetime,
    timedelta,
)
import pandas as pd

from common.data_import import DataImport
from tools_over.models import Focus
from .models import (
    Publication,
    Type,
)


class DataImportApp(DataImport):
    DJANGO_MODEL = "Publication"
    DJANGO_MODEL_OBJ = Publication
    DJANGO_APP = "publications"
    MAPPING_EXCEL_DB_EN = {
        "title__en": "title_en",
        "abstract__en": "abstract_en",
        "copyright__en": "copyright_en",
        # "Kurzbeschreibung der Wirkung__en": "effectDescription_en",
        # "Quelle / Hinweise__en": "furtherInformation_en",
    }
    MAPPING_EXCEL_DB = {
        "title": ("title", None),
        "copyright": ("abstract", None),
        "abstract": ("abstract", None),
        "url": ("url", None),
        "type": ("type", Type),
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
                readInValuesM2M[tableKey] = self.getM2MelementsQueryset(
                    m2mList, m2MModel
                )
            else:
                if row[header.index(tableKey)] == "":
                    readInValues[tableKey] = None
                else:
                    readInValues[tableKey] = row[header.index(tableKey)]

        obj = self.DJANGO_MODEL_OBJ(**readInValues)

        obj.focus.add(*focusElements)
        if self._englishHeadersPresent(header):
            self._importEnglishTranslation(
                obj, header, row, self.MAPPING_EXCEL_DB_EN
            )
        return obj, created
