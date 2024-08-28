from datetime import (
    datetime,
    timedelta,
)
import pandas as pd

from common.data_import import DataImport

from .models import DataSufficiency


class DataImportApp(DataImport):

    MAPPING_EXCEL_DB_EN = {
        "Category__en": "category_en",
        "Description__en": "description_en",
        "Name_Digital_Application__en": "name_digital_application_en",
        "Project_Name__en": "project_name_en",
        "Partner__en": "partner_en",
        "Consortium__en": "consortium_en",
        # "Additional_Digital_Application(s)__en": "digitalApplications_en",
        "Strategies__en": "strategies_en",
        "Relevance__en": "relevance_en",
        "Problem_Statement_and_Problem_Goals__en": "problem_statement_and_problem_goals_en",
        "Implementation_in_the_Project__en": "implementation_in_the_project_en",
        "Evaluation__en": "evaluation_en",
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
        strategyCategory = row[header.index("Strategiekategorie")]
        categoryShortDescription = row[
            header.index("Kategorie_Kurzbeschreibung_Teaser")
        ]
        categoryLongDescription = row[
            header.index("Kategorie_Kurzbeschreibung_Lang")
        ]
        example1 = row[header.index("Beispiel_1")]
        example2 = row[header.index("Beispiel_2")]
        example1Heading = row[header.index("Beispiel_1_Überschrift")]
        example2Heading = row[header.index("Beispiel_2_Überschrift")]

        obj, created = DataSufficiency.objects.get_or_create(
            strategyCategory=strategyCategory,
            categoryShortDescription=categoryShortDescription,
            categoryLongDescription_de=categoryLongDescription,
            example1=example1,
            example2=example2,
            example1Heading=example1Heading,
            example2Heading=example2Heading,
        )

        literatureStr = row[header.index("Literatur")]
        literatureObjsList = self._importLiterature(literatureStr)
        obj.literature.add(*literatureObjsList)

        # if self._englishHeadersPresent(header):
        #    self._getOrCreateEnglishTranslation(row, header, data, obj)
        #

    def _getOrCreateEnglishTranslation(
        self, row: list, header: list, data: list, environmentalimpactObj
    ):
        """ """
        for mappingKey in self.MAPPING_EXCEL_DB_EN.keys():
            # attributeNameWithoutEn = self.MAPPING_EXCEL_DB_EN[mappingKey].remove("__en")
            # if hasattr(obj, attributeNameWithoutEn)
            try:
                setattr(
                    environmentalimpactObj,
                    self.MAPPING_EXCEL_DB_EN[mappingKey],
                    row[header.index(mappingKey)],
                )
            except:
                breakpoint()
        environmentalimpactObj.save()

    def _englishHeadersPresent(self, header: list) -> bool:
        """Check if english translation headers are present in the
        list of headers. If yes, then return `True` otherwise `False`

        """
        for headerItem in header:
            if "__en" in headerItem:
                return True
