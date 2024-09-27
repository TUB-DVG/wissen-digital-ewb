from datetime import (
    datetime,
    timedelta,
)
import pandas as pd

from common.data_import import DataImport
from tools_over.models import Focus
from .models import (
    UseCase,
)


class DataImportApp(DataImport):
    DJANGO_MODEL = "Publication"
    DJANGO_APP = "publications"
    MAPPING_EXCEL_DB_EN = {
        "Wirkebene__en": "levelOfAction_en",
        "Detailgrad__en": "degreeOfDetail_en",
        "Name des Effekts__en": "effectName_en",
        "Kurzbeschreibung der Wirkung__en": "effectDescription_en",
        "Quelle / Hinweise__en": "furtherInformation_en",
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
        itemCode = row[header.index("Item-Code")]
        useCase = row[header.index("Use-Case")]
        sriLevel = row[header.index("SRI-Zuordnung")]
        levelOfAction = row[header.index("Wirkebene")]
        detail = row[header.index("Detailgrad")]
        # focus = row[header.index('Perspektive')]
        effects = row[
            header.index(
                "Lfd Nr. Effekte dieser Perspektive bei dem jeweiligen Detailgrad"
            )
        ]
        ratingOfEffect = row[header.index("Wertung des Effektes")]
        nameOfEffect = row[header.index("Name des Effekts")]
        shortDescriptionOfEffect = row[
            header.index("Kurzbeschreibung der Wirkung")
        ]
        source = row[header.index("Quelle / Hinweise")]
        icon = row[header.index("ICON")]

        focusList = row[header.index("Perspektive")].split(",")
        processedFocusList = self._correctReadInValue(
            row[header.index("Perspektive")]
        )
        focusList = self._iterateThroughListOfStrings(processedFocusList, Focus)
        focusElements = Focus.objects.filter(focus__in=focusList)

        obj, created = UseCase.objects.get_or_create(
            item_code=itemCode,
            useCase=useCase,
            sriLevel=sriLevel,
            levelOfAction=levelOfAction,
            degreeOfDetail=detail,
            idPerspectiveforDetail=effects,
            effectEvaluation=ratingOfEffect,
            effectName=nameOfEffect,
            effectDescription=shortDescriptionOfEffect,
            furtherInformation=source,
            icon=icon,
        )

        obj.focus.add(*focusElements)
        if self._englishHeadersPresent(header):
            self._importEnglishTranslation(
                obj, header, row, self.MAPPING_EXCEL_DB_EN
            )
        return obj, created
