from datetime import (
    datetime,
    timedelta,
)
import pandas as pd

from common.data_import import DataImport

from .models import *


class DataImportApp(DataImport):
    DJANGO_APP = "user_integration"
    DJANGO_MODEL = "UserEngagement"
    MAPPING_EXCEL_DB_EN = {
        "Unterkategorie__en": "category_en",
        "Kategorie_Kurzbeschreibung__en": "categoryShortDescription_en",
        "Unterkategorie_Kurzbeschreibung__en": "subCategoryShortDescription_en",
        "Unterkategorie_Kurzbeschreibung__en": "subCategoryShortDescription_en",
        "Zeitbedarf__en": "timeRequired_en",
        "Gruppengröße__en": "groupSize_en",
        "Material__en": "material_en",
        "Ziele__en": "goals_en",
        "Good-Practice-Beispiel__en": "goodPracticeExample_en",
        "Vorteile__en": "proArgument_en",
        "Nachteile__en": "conArgument_en",
        "Ablauf__en": "procedureItem_en",
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
        category = row[header.index("Kategorie")]
        categoryShortDescription = row[
            header.index("Kategorie_Kurzbeschreibung")
        ]
        subCategory = row[header.index("Unterkategorie")]
        subCategoryShortDescription = row[
            header.index("Unterkategorie_Kurzbeschreibung")
        ]
        subtitle = row[header.index("Untertitel")]
        timeRequired = row[header.index("Zeitbedarf")]
        groupSize = row[header.index("Gruppengröße")]
        material = row[header.index("Material")]
        goals = row[header.index("Ziele")]
        goodPracticeExample = row[header.index("Good-Practice-Beispiel")]
        obj, created = UserEngagement.objects.get_or_create(
            category=category,
            categoryShortDescription=categoryShortDescription,
            subCategory=subCategory,
            subCategoryShortDescription=subCategoryShortDescription,
            subtitle=subtitle,
            timeRequired=timeRequired,
            groupSize=groupSize,
            material=material,
            goals=goals,
            goodPracticeExample=goodPracticeExample,
        )
        procedureList = self._processListInput(
            row[header.index("Ablauf")], ";;"
        )
        procedureObjList = [
            ProcedureItem.objects.get_or_create(procedureItem=procedure)[0]
            for procedure in procedureList
        ]
        conArgumentsList = self._processListInput(
            row[header.index("Nachteile")], ";;"
        )
        conObjsList = [
            ConArgument.objects.get_or_create(conArgument=conArgElement)[0]
            for conArgElement in conArgumentsList
        ]
        proArgumentsList = self._processListInput(
            row[header.index("Vorteile")], ";;"
        )
        proObjsList = [
            ProArgument.objects.get_or_create(proArgument=proArgElement)[0]
            for proArgElement in proArgumentsList
        ]
        literatureList = self._processListInput(
            row[header.index("Literatur")], ";;"
        )
        literatureObjsList = []
        for literatureElement in literatureList:
            splittedLiteratureElement = literatureElement.split("((")
            literatureString = splittedLiteratureElement[0]
            literatureIdentifer = splittedLiteratureElement[1].replace("))", "")
            literatureObj, _ = Literature.objects.get_or_create(
                literature=literatureString,
                linkName=literatureIdentifer,
            )
            literatureObjsList.append(literatureObj)
        obj.procedureItem.add(*procedureObjList)
        obj.proArgument.add(*proObjsList)
        obj.conArgument.add(*conObjsList)
        obj.literature.add(*literatureObjsList)
        if self._englishHeadersPresent(header):
            self._importEnglishTranslation(
                obj, header, row, self.MAPPING_EXCEL_DB_EN
            )
        return obj, created
