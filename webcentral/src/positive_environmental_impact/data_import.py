from datetime import (
    datetime,
    timedelta,
)
import pandas as pd

from common.data_import import DataImport

from .models import *


class DataImportApp(DataImport):
    DJANGO_MODEL = "EnvironmentalImpact"
    DJANGO_APP = "positive_environmental_impact"
    MAPPING_EXCEL_DB_EN = {
        "Category__en": "category_en",
        "Description__en": "description_en",
        "Name_Digital_Application__en": "name_digital_application_en",
        "Projektname__en": "project_name_en",
        "Goals__en": "goals_en",
        "Digital_applications__en": "digitalApplications_en",
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
        category = row[header.index("Category")]
        description = row[header.index("Description")]
        nameDigitalApplication = row[header.index("Name_Digital_Application")]
        projectname = row[header.index("Projektname")]
        fundingLabel = row[header.index("Funding_Label")]
        duration = row[header.index("Duration")]
        partner = row[header.index("Partner")]
        projectWebsite = row[header.index("Project_Website")]
        consortium = row[header.index("Consortium")]
        further = row[header.index("Further")]
        digitalApplications = row[header.index("Digital_applications")]
        goals = row[header.index("Goals")]
        strategies = row[header.index("Strategies")]
        relevance = row[header.index("Relevance")]
        image = row[header.index("Image")]
        problemStatementAndProblemGoals = row[
            header.index("Problem_Statement_and_Problem_Goals")
        ]
        implementationInTheProject = row[
            header.index("Implementation_in_the_Project")
        ]
        evaluation = row[header.index("Evaluation")]
        projectName = row[header.index("Project_Name")]
        weiterführendeLiteratur = row[header.index("Weiterführende Literatur")]
        duration = row[header.index("Duration")]

        obj, created = EnvironmentalImpact.objects.get_or_create(
            category_de=category,
            description_de=description,
            name_digital_application_de=nameDigitalApplication,
            project_name_de=projectname,
            partner_de=partner,
            project_website=projectWebsite,
            consortium_de=consortium,
            further_de=further,
            digitalApplications_de=digitalApplications,
            goals_de=goals,
            strategies_de=strategies,
            relevance_de=relevance,
            image=image,
            problem_statement_and_problem_goals_de=problemStatementAndProblemGoals,
            implementation_in_the_project_de=implementationInTheProject,
            evaluation_de=evaluation,
            duration=duration,
        )
        fundingLabelList = self._processListInput(
            row[header.index("Funding_Label")], ";;"
        )
        fundingLabelObjList = [
            Subproject.objects.get_or_create(referenceNumber_id=fkzItem)[0]
            for fkzItem in fundingLabelList
        ]
        literatureStr = row[header.index("Weiterführende Literatur")]
        literatureObjsList = self._importLiterature(literatureStr)
        obj.literature.add(*literatureObjsList)

        # for literatureElement in literatureList:
        #     splittedLiteratureElement = literatureElement.split("((")
        #     literatureString = splittedLiteratureElement[0]
        #     literatureIdentifer = splittedLiteratureElement[1].replace(
        #         "))", "")
        #     literatureObj, _ = Literature.objects.get_or_create(
        #         literature=literatureString,
        #         linkName=literatureIdentifer,
        #     )
        #     literatureObjsList.append(literatureObj)
        obj.funding_label.add(*fundingLabelObjList)
        # obj.literature.add(*literatureObjsList)

        if self._englishHeadersPresent(header):
            self._getOrCreateEnglishTranslation(row, header, data, obj)

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

        if self._englishHeadersPresent(header):
            obj = self._importEnglishTranslation(
                obj, header, row, self.MAPPING_EXCEL_DB_EN
            )
        obj.save()

    # def _getOrCreateEnglishTranslation(self, row: list, header: list, data: list, environmentalimpactObj):
    #     """
    #
    #     """
    #     for mappingKey in self.MAPPING_EXCEL_DB_EN.keys():
    #         # attributeNameWithoutEn = self.MAPPING_EXCEL_DB_EN[mappingKey].remove("__en")
    #         # if hasattr(obj, attributeNameWithoutEn)
    #         try:
    #             setattr(environmentalimpactObj, self.MAPPING_EXCEL_DB_EN[mappingKey], row[header.index(mappingKey)])
    #         except:
    #             breakpoint()
    #     environmentalimpactObj.save()
    #

    def _englishHeadersPresent(self, header: list) -> bool:
        """Check if english translation headers are present in the
        list of headers. If yes, then return `True` otherwise `False`

        """
        for headerItem in header:
            if "__en" in headerItem:
                return True

        return False
