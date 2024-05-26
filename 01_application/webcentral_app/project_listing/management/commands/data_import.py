"""Loads different types of Data into the Django-Database.

This module loads different types of Data into the Postgres-Database
via the Django-Application. Therefore it gets a .csv-file, which holds 
the datasets. 
`data_import` allows to load different kind of datasets
into the Database. The data-kind needs to be specified in the filename
of the .csv-file:
`enargus`: Enargus-Data
`modulzuordnung`: Modul-Data
`Tools`: Tools-Data
`schlagwoerter`: Schlagwörter-Data
`weatherdata`: Wheaterdata
If none of these sub-strings is present in the filename, the data can 
not be processed and an error is printed. 
The relational model of the database is composed of multiple tables,
which are connected via foreign-keys. The central table, which connects
the different parts together is the `Subproject`-table. It holds all the
foreign-keys, which point to the Enagus-Table, the 
Schlagwörter_erstichtung-table and so on. If a dataset inside the to be
loaded .csv-file contains a Förderkennzeichen (fkz), which is already 
present in the Subproject-table, but has differences in the other 
columns, an IntegrityError is thrown, because the data cannot be 
connected with the fkz. In this situation, the `compareForeignTables`-
method is called, which wlaks though all tables and builds an 
DatabaseDifference-Object, which holds the differences between
the currentState (dataset, which is currently connected to the 
fkz inside the database.) and the pendingState (dataset, which can 
not connected to the fkz, because the currentState is already 
connected to it.). 
At the moment, all DatabaseDifference-Objects are serialized
and written to a.YAML-File. The .yaml-file is named as the current
timestamp.
The `data_import`-Script can be started as a Django-Command. For
that, the current directory needs to be changed to the folder
containing the Django `manage.py`. From there, the following
command needs to be run:
```
    python3 manage.py data_import enargus_01.csv
```
This command loads the enargus_01.csv into the database. For
eventually upcoming Conflicts, a .yaml-file is created. 
The .yaml-file can then be modified to decide, if the currentState
should be kept while the pendingState is deleted, or 
the pendingState should be kept and the currentState should be
deleted. The modified file can then be used as an input for the
`execute_db_changes` command.
"""

import csv
from datetime import datetime, timedelta
import difflib
from encodings import utf_8
import os
import math

from django.apps import apps
from django.core.management.base import BaseCommand, CommandError
from django.db.models import Model
import numpy as np
import pandas as pd

from criteriaCatalog.models import (
    CriteriaCatalog,
    Topic,
    Tag,
)
from component_list.models import (
    Component,
    ComponentClass,
    Category,
    EnvironmentalImpact,
    DataSufficiency,
)

from businessModel.models import BusinessModel, UserIntegration

from project_listing.models import (
    Subproject,
    ModuleAssignment,
    Enargus,
    Address,
    GrantRecipient,
    ExecutingEntity,
    RAndDPlanningCategory,
    Person,
    FurtherFundingInformation,
)
from publications.models.publication import Publication
from publications.models.publication import Type

from django.db import IntegrityError
from keywords.models import (
    Keyword,
    KeywordRegisterFirstReview,
)
from tools_over.models import (
    Accessibility,
    ApplicationArea,
    Classification,
    Focus,
    Tools,
    Usage,
    TargetGroup,
    LifeCyclePhase,
    UserInterface,
    Scale,
)
from TechnicalStandards.models import (
    Norm,
    Protocol,
)
from use_cases.models import UseCase
from weatherdata_over.models import Weatherdata
from project_listing.DatabaseDifference import DatabaseDifference


class MultipleFKZDatasets(Exception):
    """Custom Exception, which is thrown when multiple changes for one
    Förderkennzeichen are written to .yaml-file.
    """


class Command(BaseCommand):
    """This class acts as a Django-Admin command. It can be executed with
    the manage.py by specifing the name of the modul (at the moment
    `data_import`). Furthermore a parameter needs to be present, which is
    the relative-path to a .csv-file, which holds datasets, which should
    be imported into the database.
    An execution could look like this:
    ```
        python3 manage.py data_import
        ../../02_work_doc/01_daten/01_prePro/enargus_csv_20230403.csv
    ```
    At the moment, the .csv-files need to be named acording to the data.
    it holds. (TODO: This has to be changed)

    enargus-data needs to have "enargus" in its filename.
    modulzurodnung-data needs to have "modul" in its filename.
    wheaterdata needs to have "wheaterdata" in its filename.
    schlagwoerter-data needs to have "schlagwoerter" in its filename.
    """

    def __init__(self) -> None:
        """Constructor of `data_import`-command

        This method serves as constructor for the Command-Class.
        It is used to create the Filename of the .YAML-File,
        which is a timestamp of the current datetime. Furthermore
        fkzWrittenToYAML is initialized as empty list,
        in which later every Förderkennzeichen(fkz) is saved,
        which produced an conflict with a dataset inside the database.

        Returns:
        None
        """
        super().__init__()
        self.fkzWrittenToYAML = []

    def getOrCreateFurtherFundingInformation(
        self,
        row: list,
        header: list,
    ) -> tuple:
        """Gets or Creates Research-Object according to row

        This method feeds the data present in row into the django
        get_or_create-function, which returns an Object of Type
        FurtherFundingInformation according to the fed-data. Either this object
        corresponds to a new created-dataset in the database or
        the existing dataset is returned.

        Parameters:
        row:    list
            A dataset, represented by a list.
        header: list
            list of strings, which represent the header-columns.

        Returns:
        obj:    FurtherFundingInformation
            FurtherFundingInformation-object, represent the created or in database
            present FurtherFundingInformation-Dataset with the data from row.
        created:    bool
            Indicates, if the FurtherFundingInformation-object was created or not.
        """
        federalMinistry = row[header.index("Bundesministerium")]
        projectBody = row[header.index("Projekttraeger")]
        supportProgram = row[header.index("Foerderprogramm")]
        researchProgram = row[header.index("Forschungsprogramm")]
        obj, created = FurtherFundingInformation.objects.get_or_create(
            fundedBy=federalMinistry,
            projectManagementAgency=projectBody,
            researchProgram=researchProgram,
            fundingProgram=supportProgram,
        )
        return obj, created

    def getOrCreateAdress(
        self,
        row: list,
        header: list,
        who: str,
    ) -> tuple:
        """Gets or Creates an object of type Address from the data in row

        This method feeds the data present in row into the django
        get_or_create-function, which returns an Object of Type
        Address according to the fed-data. Either this object
        corresponds to a new created-dataset in the database or
        the existing dataset is returned.

        Parameters:
        row:    list
            A dataset, represented by a list.
        header: list
            list of strings, which represent the header-columns.
        who:    str
            indicates the type of Adress. It can have the values `zwe`
            for zuwendungsempfaenger or `as` for ausfehrende Stelle.

        Returns:
        obj:    FurtherFundingInformation
            Address-object, represent the created or in database
            present FurtherFundingInformation-Dataset with the data from row.
        created:    bool
            Indicates, if the Address-object was created or not.
        """

        if who == "zwe":
            postalCode = row[header.index("PLZ_ZWE")]
            location = row[header.index("Ort_ZWE")]
            country = row[header.index("Land_ZWE")]
            adress = row[header.index("Adress_ZWE")]
        elif who == "as":
            postalCode = row[header.index("PLZ_AS")]
            location = row[header.index("Ort_AS")]
            country = row[header.index("Land_AS")]
            adress = row[header.index("Adress_AS")]

        obj, created = Address.objects.get_or_create(
            plz=postalCode,
            location=location,
            state=country,
            address=adress,
        )
        return obj, created

    def getOrCreateCriteriaCatalog(self, row: list, header: list) -> None:
        """
        Add entry (CriteriaCatalog) into the table or/and return entry key.
        """

        criteriaCatalogForTopic, _ = CriteriaCatalog.objects.get_or_create(
            name=row[header.index("katalog")], )

        try:
            if row[header.index("parentId")] == "":
                parentTopicOfCurrentTopic = None
            else:
                parentTopicOfCurrentTopic = Topic.objects.get(id=int(
                    row[header.index("parentId")]), )
        except Topic.DoesNotExist:
            parentTopicOfCurrentTopic = None

        obj, created = Topic.objects.get_or_create(
            id=row[header.index("id")],
            heading=row[header.index("ueberschrift")],
            text=row[header.index("text")],
            criteriaCatalog=criteriaCatalogForTopic,
            parent=parentTopicOfCurrentTopic,
            imageFilename=row[header.index("image")],
        )

        if row[header.index("tags")] != "" or row[header.index("tags")] == " ":
            tagList = row[header.index("tags")].split(",")
            for tag in tagList:
                tagObj, _ = Tag.objects.get_or_create(name=tag)
                obj.tag.add(tagObj)
            obj.save()

        # return obj, created

    def getOrCreatePerson(
        self,
        row: list,
        header: list,
    ) -> tuple:
        """Gets or Creates an object of type Person from the data in row

        This method feeds the data present in row into the django
        get_or_create-function, which returns an Object of Type
        Person according to the fed-data. Either this object
        corresponds to a new created-dataset in the database or
        the existing dataset is returned.

        Parameters:
        row:    list
            A dataset, represented by a list.
        header: list
            list of strings, which represent the header-columns.

        Returns:
        obj:    FurtherFundingInformation
            Person-object, represent the created or in database
            present FurtherFundingInformation-Dataset with the data from row.
        created:    bool
            Indicates, if the Person-object was created or not.
        """
        # content = row[number of the columns of the row]
        # decision kind of persion, where should the data read from,
        # maybe later needed
        name = row[header.index("Name_pl")]
        firstNameFromCSV = row[header.index("Vorname_pl")]
        titel = row[header.index("Titel_pl")]
        email = row[header.index("Email_pl")]
        obj, created = Person.objects.get_or_create(
            surname=name,
            firstName=firstNameFromCSV,
            title=titel,
            email=email,
        )
        return obj, created

    def getOrCreateUserIntegration(self, row: list, header: list) -> tuple:
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
        categoryShortDescription = row[header.index(
            "Kategorie_Kurzbeschreibung")]
        subCategory = row[header.index("Unterkategorie")]
        subCategoryShortDescription = row[header.index(
            "Unterkategorie_Kurzbeschreibung")]
        subtitle = row[header.index("Untertitel")]
        timeRequired = row[header.index("Zeitbedarf")]
        groupSize = row[header.index("Gruppengröße")]
        material = row[header.index("Material")]
        advantages = row[header.index("Vorteile")]
        disadvantages = row[header.index("Nachteile")]
        conductedBy = row[header.index("Durchgeführt von")]
        successFactors = row[header.index(
            "Erfolgsfaktoren für die Umsetzung der Methode")]
        goals = row[header.index("Ziele")]
        procedure = row[header.index("Ablauf")]
        specificGoals = row[header.index("Konkrete_Ziele")]
        specificProcedure = row[header.index("Konkreter_Ablauf")]

        obj, created = UserIntegration.objects.get_or_create(
            category=category,
            categoryShortDescription=categoryShortDescription,
            subCategory=subCategory,
            subCategoryShortDescription=subCategoryShortDescription,
            subtitle=subtitle,
            timeRequired=timeRequired,
            groupSize=groupSize,
            material=material,
            advantages=advantages,
            disadvantages=disadvantages,
            conductedBy=conductedBy,
            successFactors=successFactors,
            goals=goals,
            procedure=procedure,
            specificGoals=specificGoals,
            specificProcedure=specificProcedure,
        )
        return obj, created

    def getOrCreateBusinessModel(self, row: list, header: list) -> tuple:
        """Gets or Creates an object of type BusinessModel from the data in row

        This method feeds the data present in row into the django
        get_or_create-function, which returns an Object of Type
        BusinessModel according to the fed-data. Either this object
        corresponds to a new created-dataset in the database or
        the existing dataset is returned.

        Parameters:
        row:    list
            A dataset, represented by a list.
        header: list
            list of strings, which represent the header-columns.

        Returns:
        obj:    BusinessModel
            BusinessModel-object, represent the created or in database
            present BusinessModel-Dataset with the data from row.
        created:    bool
            Indicates, if the BusinessModel-object was created or not.
        """
        challenge = row[header.index("Herausfoderung")]
        shortDescription = row[header.index("Kurzbeschreibung")]
        property1 = row[header.index("Eigenschaft_1")]
        property1Text = row[header.index("Eigenschaft_1_Text")]
        property2 = row[header.index("Eigenschaft_2")]
        property2Text = row[header.index("Eigenschaft_2_Text")]
        property3 = row[header.index("Eigenschaft_3")]
        property3Text = row[header.index("Eigenschaft_3_Text")]
        property4 = row[header.index("Eigenschaft_4")]
        property4Text = row[header.index("Eigenschaft_4_Text")]
        property5 = row[header.index("Eigenschaft_5")]
        property5Text = row[header.index("Eigenschaft_5_Text")]

        obj, created = BusinessModel.objects.get_or_create(
            challenge=challenge,
            shortDescription=shortDescription,
            property1=property1,
            property1Text=property1Text,
            property2=property2,
            property2Text=property2Text,
            property3=property3,
            property3Text=property3Text,
            property4=property4,
            property4Text=property4Text,
            property5=property5,
            property5Text=property5Text,
        )
        return obj, created

    def getOrCreateRAndDPlanningCategory(
        self,
        row: list,
        header: list,
    ) -> tuple:
        """Gets or Creates an object of type RAndDPlanningCategory from the data in row

        This method feeds the data present in row into the django
        get_or_create-function, which returns an Object of Type
        RAndDPlanningCategory according to the fed-data. Either this object
        corresponds to a new created-dataset in the database or
        the existing dataset is returned.

        Parameters:
        row:    list
            A dataset, represented by a list.
        header: list
            list of strings, which represent the header-columns.

        Returns:
        obj:    FurtherFundingInformation
            RAndDPlanningCategory-object, represent the created or in database
            present FurtherFundingInformation-Dataset with the data from row.
        created:    bool
            Indicates, if the RAndDPlanningCategory-object was created or not.
        """
        # content = row[number of the columns of the row]
        textFromCSV = row[header.index("Leistungsplan_Sys_Text")]
        idFromCSV = row[header.index("Leistungsplan_Sys_Nr")]

        obj, created = RAndDPlanningCategory.objects.get_or_create(
            rAndDPlanningCategoryNumber=idFromCSV,
            rAndDPlanningCategoryText=textFromCSV,
        )
        return obj, created

    def getOrCreateGrantRecipient(
        self,
        row: list,
        header: list,
    ) -> tuple:
        """Gets or Creates an object of type GrantRecipient from row

        This method feeds the data present in row into the django
        get_or_create-function, which returns an Object of Type
        GrantRecipient according to the fed-data. Either this object
        corresponds to a new created-dataset in the database or
        the existing dataset is returned.

        Parameters:
        row:    list
            A dataset, represented by a list.
        header: list
            list of strings, which represent the header-columns.

        Returns:
        obj:    GrantRecipient
            GrantRecipient-object, represent the created or in database
            present FurtherFundingInformation-Dataset with the data from row.
        created:    bool
            Indicates, if the RAndDPlanningCategory-object was created or not.
        """
        objAnsZwe, _ = self.getOrCreateAdress(
            row,
            header,
            "zwe",
        )
        # doneeAdressId = objAnsZwe.anschrift_id

        # content = row[number of the columns of the row]
        nameFromCSV = row[header.index("Name_ZWE")]
        return GrantRecipient.objects.get_or_create(
            name=nameFromCSV,
            address=objAnsZwe,
        )

    def getOrCreateExecutingEntity(self, row, header):
        """Gets or Creates an object of type ExecutingEntity from row

        This method feeds the data present in row into the django
        get_or_create-function, which returns an Object of Type
        ExecutingEntity according to the fed-data. Either this object
        corresponds to a new created-dataset in the database or
        the existing dataset is returned.

        Parameters:
        row:    list
            A dataset, represented by a list.
        header: list
            list of strings, which represent the header-columns.

        Returns:
        obj:    ExecutingEntity
            Ausfuehrende_stelle-object, represent the created or in database
            present FurtherFundingInformation-Dataset with the data from row.
        created:    bool
            Indicates, if the ExecutingEntity-object was created or not.
        """
        objAnsAs, _ = self.getOrCreateAdress(row, header, "as")

        nameFromCSV = row[header.index("Name_AS")]
        return ExecutingEntity.objects.get_or_create(
            name=nameFromCSV,
            address=objAnsAs,
        )

    def getOrCreateEnvironmentalImpact(self, row: list, header: list) -> tuple:
        """Gets or Creates an object of type EnvironmentalImpact from row

        This method feeds the data present in row into the django
        get_or_create-function, which returns an Object of Type
        EnvironmentalImpact according to the fed-data. Either this object
        corresponds to a new created-dataset in the database or
        the existing dataset is returned.

        Parameters:
        row:    list
            A dataset, represented by a list.
        header: list
            list of strings, which represent the header-columns.

        Returns:
        obj:    EnvironmentalImpact
            EnvironmentalImpact-object, represent the created or in database
            present EnvironmentalImpact-Dataset with the data from row.
        created:    bool
            Indicates, if the EnvironmentalImpact-object was created or not.
        """
        category = row[header.index("Category")]
        description = row[header.index("Description")]
        nameDigitalApplication = row[header.index("Name_Digital_Application")]
        projectName = row[header.index("Project_Name")]
        fundingLabel = row[header.index("Funding_Label")]

        # check if the project is present in the Subproject-table:
        try:
            subprojectForeignObj = Subproject.objects.get(
                referenceNumber_id=fundingLabel)
        except Subproject.DoesNotExist:
            print(
                f"The specified funding-label {fundingLabel} is not present in the Subproject-table."
            )
            return None, None
        partner = row[header.index("Partner")]
        projectWebsite = row[header.index("Project_Website")]
        consortium = row[header.index("Consortium")]
        further = row[header.index("Further")]
        digitalApplications = row[header.index("Digital_applications")]
        goals = row[header.index("Goals")]
        strategies = row[header.index("Strategies")]
        relevance = row[header.index("Relevance")]
        image = row[header.index("Image")]
        problemStatementAndProblemGoals = row[header.index(
            "Problem_Statement_and_Problem_Goals")]
        implementationInTheProject = row[header.index(
            "Implementation_in_the_Project")]
        evaluation = row[header.index("Evaluation")]

        obj, created = EnvironmentalImpact.objects.get_or_create(
            category=category,
            description=description,
            name_digital_application=nameDigitalApplication,
            further=further,
            project_name=projectName,
            funding_label=subprojectForeignObj,
            partner=partner,
            project_website=projectWebsite,
            consortium=consortium,
            digitalApplications=digitalApplications,
            goals=goals,
            strategies=strategies,
            relevance=relevance,
            image=image,
            problem_statement_and_problem_goals=problemStatementAndProblemGoals,
            implementation_in_the_project=implementationInTheProject,
            evaluation=evaluation,
        )
        return obj, created

    def getOrCreateDataSufficiency(self, row: list, header: list) -> tuple:
        """Gets or Creates an object of type DataSufficiency from row

        This method feeds the data present in row into the django
        get_or_create-function, which returns an Object of Type
        DataSufficiency according to the fed-data. Either this object
        corresponds to a new created-dataset in the database or
        the existing dataset is returned.

        Parameters:
        row:    list
            A dataset, represented by a list.
        header: list
            list of strings, which represent the header-columns.

        Returns:
        obj:    DataSufficiency
            DataSufficiency-object, represent the created or in database
            present DataSufficiency-Dataset with the data from row.
        created:    bool
            Indicates, if the DataSufficiency-object was created or not.
        """
        strategyCategory = row[header.index("Strategiekategorie")]
        categoryShortDescription = row[header.index(
            "Kategorie_Kurzbeschreibung")]
        example1 = row[header.index("Beispiel_1")]
        example2 = row[header.index("Beispiel_2")]

        obj, created = DataSufficiency.objects.get_or_create(
            strategyCategory=strategyCategory,
            categoryShortDescription=categoryShortDescription,
            example1=example1,
            example2=example2,
        )
        return obj, created

    def getOrCreateEnargus(
        self,
        row: list,
        header: list,
    ) -> tuple:
        """Gets or Creates an object of type Enargus from row

        This method feeds the data present in row into the django
        get_or_create-function, which returns an Object of Type
        Enargus according to the fed-data. Either this object
        corresponds to a new created-dataset in the database or
        the existing dataset is returned.

        Parameters:
        row:    list
            A dataset, represented by a list.
        header: list
            list of strings, which represent the header-columns.

        Returns:
        obj:    Enargus
            Enargus-object, represent the created or in database
            present Enargus-Dataset with the data from row.
        created:    bool
            Indicates, if the Enargus-object was created or not.
        """
        objGrantRecipient, _ = self.getOrCreateGrantRecipient(row, header)
        objExecEntity, _ = self.getOrCreateExecutingEntity(row, header)
        objRAndDPlanning, _ = self.getOrCreateRAndDPlanningCategory(
            row, header)
        objPerson, _ = self.getOrCreatePerson(row, header)
        objFurtherFunding, _ = self.getOrCreateFurtherFundingInformation(
            row,
            header,
        )

        durationBegin = row[header.index("Laufzeitbeginn")]
        durationEnd = row[header.index("Laufzeitende")]
        theme = row[header.index("Thema")]
        clusterName = row[header.index("Verbundbezeichung")]
        fundingSum = float(row[header.index("Foerdersumme_EUR")])
        shortDescriptionDe = row[header.index("Kurzbeschreibung_de")]
        shortDescriptionEn = row[header.index("Kurzbeschreibung_en")]
        database = row[header.index("Datenbank")]
        obj, created = Enargus.objects.get_or_create(
            startDate=durationBegin,
            endDate=durationEnd,
            topics=theme,
            projectLead=objPerson,
            furtherFundingInformation=objFurtherFunding,
            rAndDPlanningCategory=objRAndDPlanning,
            grantRecipient=objGrantRecipient,
            executingEntity=objExecEntity,
            collaborativeProject=clusterName,
            appropriatedBudget=fundingSum,
            shortDescriptionDe=shortDescriptionDe,
            shortDescriptionEn=shortDescriptionEn,
            database=database,
        )
        return obj, created

    def getOrCreateModuleAssignment(
        self,
        row: list,
        header: list,
    ) -> tuple:
        """Gets or Creates an object of type ModuleAssignment from row

        This method feeds the data present in row into the django
        get_or_create-function, which returns an Object of Type
        ModuleAssignment according to the fed-data. Either this object
        corresponds to a new created-dataset in the database or
        the existing dataset is returned.

        Parameters:
        row:    list
            A dataset, represented by a list.
        header: list
            list of strings, which represent the header-columns.

        Returns:
        obj:    ModuleAssignment
            ModuleAssignment-object, represent the created or in database
            present ModuleAssignment-Dataset with the data from row.
        created:    bool
            Indicates, if the ModuleAssignment-object was created or not.
        """

        priority1FromCSV = row[header.index("modulzuordnung_ptj_1")]
        priority2FromCSV = row[header.index("modulzuordnung_ptj_2")]
        priority3FromCSV = row[header.index("modulzuordnung_ptj_3")]
        priority4FromCSV = row[header.index("modulzuordnung_ptj_4")]
        obj, created = ModuleAssignment.objects.get_or_create(
            priority1=priority1FromCSV,
            priority2=priority2FromCSV,
            priority3=priority3FromCSV,
            priority4=priority4FromCSV,
        )
        return obj, created

    def getOrCreateTools(
        self,
        row: list,
        header: list,
    ) -> tuple:
        """Gets or Creates an object of type Tools from row

        This method feeds the data present in row into the django
        get_or_create-function, which returns an Object of Type
        Tools according to the fed-data. Either this object
        corresponds to a new created-dataset in the database or
        the existing dataset is returned.

        Parameters:
        row:    list
            A dataset, represented by a list.
        header: list
            list of strings, which represent the header-columns.

        Returns:
        obj:    ToolsSubproject the Tools-object was created or not.
        """

        name = row[header.index("name")]
        shortDescription = row[header.index("shortDescription")]

        processedApplicationAreaList = self._correctReadInValue(
            row[header.index("applicationArea")])
        applicationAreaList = self._iterateThroughListOfStrings(
            processedApplicationAreaList, ApplicationArea)

        processedUsageList = self._correctReadInValue(
            row[header.index("usage")])
        usageList = self._iterateThroughListOfStrings(processedUsageList,
                                                      Usage)

        processedTargetGroup = self._correctReadInValue(
            row[header.index("targetGroup")])
        targetGroupList = self._iterateThroughListOfStrings(
            processedTargetGroup, TargetGroup)

        processedAccessibilityList = self._correctReadInValue(
            row[header.index("accessibility")])
        accessibilityList = self._iterateThroughListOfStrings(
            processedAccessibilityList, Accessibility)

        processedlifeCyclePhase = self._correctReadInValue(
            row[header.index("lifeCyclePhase")])
        lifeCyclePhaseList = self._iterateThroughListOfStrings(
            processedlifeCyclePhase, LifeCyclePhase)

        processedUserInterface = self._correctReadInValue(
            row[header.index("userInterface")])
        userInterfaceList = self._iterateThroughListOfStrings(
            processedUserInterface, UserInterface)

        lastUpdate = row[header.index("lastUpdate")]

        correctLastUpdateValues = ["unbekannt", "laufend"]
        if lastUpdate == "":
            lastUpdate = "unbekannt"
        if lastUpdate not in correctLastUpdateValues:
            if isinstance(lastUpdate, pd.Timestamp) or isinstance(
                    lastUpdate, datetime):
                date = lastUpdate.date()
            else:
                try:
                    # Try to parse the string as a date with time
                    date = datetime.strptime(lastUpdate, "%Y-%m-%d %H:%M:%S")
                except ValueError:
                    try:
                        # If that fails, try to parse it as a date without time
                        date = datetime.strptime(lastUpdate, "%Y-%m-%d")
                    except ValueError:
                        # If that also fails, return None
                        raise ValueError(
                            f"The tool {name} could not be imported, because the lastUpdate-Value is {lastUpdate}. Only 'unbekannt', 'laufend' or a date in the format 'YYYY-MM-DD' is allowed."
                        )

            # Return the date part of the datetime object as a string
            lastUpdate = date.strftime("%Y-%m-%d")

        license = row[header.index("license")]
        licenseNotes = row[header.index("licenseNotes")]
        furtherInfos = row[header.index("furtherInformation")]
        alternatives = row[header.index("alternatives")]
        processedSpecificApplicationList = self._correctReadInValue(
            row[header.index("specificApplication")])
        specificApplicationList = self._iterateThroughListOfStrings(
            processedSpecificApplicationList, Subproject)

        provider = row[header.index("provider")]
        imageName = row[header.index("image")]
        processedScaleList = self._correctReadInValue(
            row[header.index("scale")])

        scaleList = self._iterateThroughListOfStrings(processedScaleList,
                                                      Scale)
        released = row[header.index("released")]
        if released == "":
            released = None
        elif released == "unbekannt":
            released = None
        else:
            released = bool(int(released))

        releasedPlanned = row[header.index("releasedPlanned")]
        if releasedPlanned == "":
            releasedPlanned = None
        else:
            releasedPlanned = bool(int(releasedPlanned))

        yearOfRelease = row[header.index("yearOfRelease")]

        developmentState = row[header.index("developmentState")]
        if developmentState == "":
            developmentState = None
        else:
            developmentState = int(developmentState)

        processedTechnicalStandardsNorms = self._correctReadInValue(
            row[header.index("technicalStandardsNorms")])
        technicalStandardsNormsList = self._iterateThroughListOfStrings(
            processedTechnicalStandardsNorms, Norm)

        technicalStandardsProtocolsList = row[header.index(
            "technicalStandardsProtocols")].split(",")
        processedFocusList = self._correctReadInValue(
            row[header.index("focus")])
        focusList = self._iterateThroughListOfStrings(processedFocusList,
                                                      Focus)

        processedClassificationList = self._correctReadInValue(
            row[header.index("classification")])
        classificationList = self._iterateThroughListOfStrings(
            processedClassificationList, Classification)
        userInterfaceNotes = row[header.index("userInterfaceNotes")]
        programmingLanguages = row[header.index("programmingLanguages")]
        frameworksLibraries = row[header.index("frameworksLibraries")]
        databaseSystem = row[header.index("databaseSystem")]
        resources = row[header.index("resources")]

        focusElements = Focus.objects.filter(focus__in=focusList)
        classificationElements = Classification.objects.filter(
            classification__in=classificationList)
        applicationAreaElements = ApplicationArea.objects.filter(
            applicationArea__in=applicationAreaList)
        usageElements = Usage.objects.filter(usage__in=usageList)
        lifeCyclePhaseElements = LifeCyclePhase.objects.filter(
            lifeCyclePhase__in=lifeCyclePhaseList)
        userInterfaceElements = UserInterface.objects.filter(
            userInterface__in=userInterfaceList)
        targetGroupElements = TargetGroup.objects.filter(
            targetGroup__in=targetGroupList)
        scaleElements = Scale.objects.filter(scale__in=scaleList)
        accessibilityElements = Accessibility.objects.filter(
            accessibility__in=accessibilityList)
        specificApplicationElements = Subproject.objects.filter(
            referenceNumber_id__in=specificApplicationList)
        technicalStandardsNormsElements = Norm.objects.filter(
            name__in=technicalStandardsNormsList)
        technicalStandardsProtocolsElements = Protocol.objects.filter(
            name__in=technicalStandardsProtocolsList)
        obj, created = Tools.objects.get_or_create(
            name=name,
            shortDescription=shortDescription,
            applicationArea__in=applicationAreaElements,
            usage__in=usageElements,
            lifeCyclePhase__in=lifeCyclePhaseElements,
            userInterface__in=userInterfaceElements,
            userInterfaceNotes=userInterfaceNotes,
            programmingLanguages=programmingLanguages,
            frameworksLibraries=frameworksLibraries,
            databaseSystem=databaseSystem,
            scale__in=scaleElements,
            accessibility__in=accessibilityElements,
            targetGroup__in=targetGroupElements,
            lastUpdate=lastUpdate,
            license=license,
            licenseNotes=licenseNotes,
            furtherInformation=furtherInfos,
            alternatives=alternatives,
            specificApplication__in=specificApplicationElements,
            focus__in=focusElements,
            classification__in=classificationElements,
            provider=provider,
            image=imageName,
            released=released,
            releasedPlanned=releasedPlanned,
            resources=resources,
            yearOfRelease=yearOfRelease,
            developmentState=developmentState,
            technicalStandardsNorms__in=technicalStandardsNormsElements,
            technicalStandardsProtocols__in=technicalStandardsProtocolsElements,
        )
        if created:
            obj.focus.add(*focusElements)
            obj.classification.add(*classificationElements)
            obj.applicationArea.add(*applicationAreaElements)
            obj.usage.add(*usageElements)
            obj.lifeCyclePhase.add(*lifeCyclePhaseElements)
            obj.userInterface.add(*userInterfaceElements)
            obj.scale.add(*scaleElements)
            obj.accessibility.add(*accessibilityElements)
            obj.targetGroup.add(*targetGroupElements)
            obj.specificApplication.add(*specificApplicationElements)
            obj.technicalStandardsNorms.add(*technicalStandardsNormsElements)
            obj.technicalStandardsProtocols.add(
                *technicalStandardsProtocolsElements)
            obj.save()

        return obj, created

    def getOrCreateWeatherdata(
        self,
        row: list,
        header: list,
    ) -> tuple:
        """Gets or Creates an object of type Weatherdata from row

        This method feeds the data present in row into the django
        get_or_create-function, which returns an Object of Type
        Weatherdata according to the fed-data. Either this object
        corresponds to a new created-dataset in the database or
        the existing dataset is returned.

        Parameters:
        row:    list
            A dataset, represented by a list.
        header: list
            list of strings, which represent the header-columns.

        Returns:
        obj:    Weatherdata
            Weatherdata-object, represent the created or in database
            present Weatherdata-Dataset with the data from row.
        created:    bool
            Indicates, if the Weatherdata-object was created or not.
        """

        dataService = row[header.index("data_service")]
        shortDescription = row[header.index("short_description")]
        provider = row[header.index("provider")]
        furtherInfos = row[header.index("further_information")]
        dataUrl = row[header.index("data_url")]
        logoUrl = row[header.index("logo_url")]
        applications = row[header.index("applications")]
        lastUpdate = row[header.index("last_update")]
        license = row[header.index("license")]
        category = row[header.index("category")]
        longDescription = row[header.index("long_description")]

        obj, created = Weatherdata.objects.get_or_create(
            data_service=dataService,
            short_description=shortDescription,
            provider=provider,
            further_information=furtherInfos,
            data_url=dataUrl,
            logo_url=logoUrl,
            applications=applications,
            last_update=lastUpdate,
            license=license,
            category=category,
            long_description=longDescription,
        )
        return obj, created

    def getOrCreateUseCases(self, row, header):
        """create a UseCase object from row and header of a Spreadsheet"""
        itemCode = row[header.index("Item-Code")]
        useCase = row[header.index("Use-Case")]
        sriLevel = row[header.index("SRI-Zuordnung")]
        levelOfAction = row[header.index("Wirkebene")]
        detail = row[header.index("Detailgrad")]
        # focus = row[header.index('Perspektive')]
        effects = row[header.index(
            "Lfd Nr. Effekte dieser Perspektive bei dem jeweiligen Detailgrad"
        )]
        ratingOfEffect = row[header.index("Wertung des Effektes")]
        nameOfEffect = row[header.index("Name des Effekts")]
        shortDescriptionOfEffect = row[header.index(
            "Kurzbeschreibung der Wirkung")]
        source = row[header.index("Quelle / Hinweise")]
        icon = row[header.index("ICON")]

        focusList = row[header.index("Perspektive")].split(",")
        processedFocusList = self._correctReadInValue(
            row[header.index("Perspektive")])
        focusList = self._iterateThroughListOfStrings(processedFocusList,
                                                      Focus)
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
        return obj, created

    def getOrCreateComponent(self, row, header):
        categoryName = row[header.index("Category")]
        # category = self._correctReadInValue(categoryName)
        categoryStr = self._selectNearestMatch(categoryName, Category)
        category = Category.objects.get(category=categoryStr)
        # Add foreign key relation to category
        componentName = row[header.index("Component")]
        componentStr = self._selectNearestMatch(componentName, ComponentClass)
        component = ComponentClass.objects.get(componentClass=componentStr)
        description = row[header.index("Description")]
        try:
            energyConsumptionUsePhaseTotal = float(row[header.index(
                "Energy consumption Use Phase (total; in W)")])
        except ValueError:
            energyConsumptionUsePhaseTotal = None
        try:
            globalWarmingPotentialTotal = float(row[header.index(
                "Global warming potential (total; in kg CO2-e)")])
        except ValueError:
            globalWarmingPotentialTotal = None
        try:
            componentWeight = float(
                row[header.index("Component weight (in kg)")])
        except ValueError:
            componentWeight = None
        try:
            lifetime = float(row[header.index("Lifetime (in years)")])
        except ValueError:
            lifetime = None
        # lifetime = row[header.index("Lifetime (in years)")]
        try:
            energyConsumptionUsePhaseActive = float(row[header.index(
                "Energy consumption Use Phase (active; in W)")])
        except ValueError:
            energyConsumptionUsePhaseActive = None
        try:
            energyConsumptionUsePhasePassive = float(row[header.index(
                "Energy consumption Use Phase (passive; in W)")])
        except ValueError:
            energyConsumptionUsePhasePassive = None

        try:
            globalWarmingPotentialProduction = float(row[header.index(
                "Global warming potential (production; in kg CO2-e)")])
        except ValueError:
            globalWarmingPotentialProduction = None
        try:
            globalWarmingPotentialUsePhase = float(row[header.index(
                "Global warming potential (use phase; in kg CO2-e)")])
        except ValueError:
            globalWarmingPotentialUsePhase = None
        try:
            globalWarmingPotentialEndOfLife = float(row[header.index(
                "Global warming potential (end-of-life; in kg CO2-e)")])
        except ValueError:
            globalWarmingPotentialEndOfLife = None
        furtherInformationNotes = row[header.index(
            "Further information / notes")]
        sources = row[header.index("Sources")]
        obj, created = Component.objects.get_or_create(
            category=category,
            component=component,
            description=description,
            energyConsumptionUsePhaseTotal=energyConsumptionUsePhaseTotal,
            globalWarmingPotentialTotal=globalWarmingPotentialTotal,
            componentWeight=componentWeight,
            lifetime=lifetime,
            energyConsumptionUsePhaseActive=energyConsumptionUsePhaseActive,
            energyConsumptionUsePhasePassive=energyConsumptionUsePhasePassive,
            globalWarmingPotentialProduction=globalWarmingPotentialProduction,
            globalWarmingPotentialUsePhase=globalWarmingPotentialUsePhase,
            globalWarmingPotentialEndOfLife=globalWarmingPotentialEndOfLife,
            furtherInformationNotes=furtherInformationNotes,
            sources=sources,
        )

        return obj, created

    def getOrCreatePublications(self, row, header):
        """
        Add entry (Publications) into the table or/and return entry key.
        """
        type_ = row[header.index("type")]
        title = row[header.index("title")]
        copyright = row[header.index("copyright")]
        url = row[header.index("url")]
        abstract = row[header.index("abstract")]
        institution = row[header.index("institution")]
        authors = row[header.index("authors")]
        month = row[header.index("month")]
        year = row[header.index("year")]
        doi = row[header.index("doi")]
        keywords = row[header.index("keywords")]
        focus = row[header.index("focus")]
        journal = row[header.index("journal")]
        volume = row[header.index("volume")]
        number = row[header.index("number")]
        pages = row[header.index("pages")]
        pdf = row[header.index("pdf")]
        image = row[header.index("image")]

        focusList = row[header.index("focus")].split(",")
        processedFocusList = self._correctReadInValue(
            row[header.index("focus")])
        focusList = self._iterateThroughListOfStrings(processedFocusList,
                                                      Focus)
        focusElements = Focus.objects.filter(focus__in=focusList)

        typeORMObjList = Type.objects.filter(type=type_)
        if len(typeORMObjList) == 0:
            Type.objects.create(type=type_)

        typeORMObj = Type.objects.filter(type=type_)[0]

        if number == "":
            number = None

        if volume == "":
            volume = None

        if month == "":
            month = None
        else:
            month = int(month)

        if year == "":
            year = None
        else:
            year = int(year)

        obj, created = Publication.objects.get_or_create(
            type=typeORMObj,
            title=title,
            copyright=copyright,
            url=url,
            abstract=abstract,
            institution=institution,
            authors=authors,
            month=month,
            year=year,
            doi=doi,
            keywords=keywords,
            journal=journal,
            volume=volume,
            number=number,
            pages=pages,
            pdf=pdf,
            image=image,
        )
        obj.focus.add(*focusElements)
        return obj, created

    def getOrCreateKeyword(
        self,
        row: list,
        header: list,
        catchphraseKey: str,
    ) -> tuple:
        """Gets or Creates an object of type Keyword from row

        This method feeds the data present in row into the django
        get_or_create-function, which returns an Object of Type
        Keyword according to the fed-data. Either this object
        corresponds to a new created-dataset in the database or
        the existing dataset is returned.

        Parameters:
        row:    list
            A dataset, represented by a list.
        header: list
            list of strings, which represent the header-columns.

        Returns:
        obj:    Keyword
            Keyword-object, represent the created or in database
            present Keyword-Dataset with the data from row.
        created:    bool
            Indicates, if the Keyword-object was created or not.
        """
        # content = row[number of the columns of the row]
        keywordFromCSV = row[header.index(catchphraseKey)]
        obj, created = Keyword.objects.get_or_create(keyword=keywordFromCSV, )
        return obj, created

    def getOrCreateKeywordRegisterFirstReview(
        self,
        row: list,
        header: list,
    ) -> tuple:
        """Gets or Creates KeywordRegisterFirstReview from Row

        This method feeds the data present in row into
        `getOrCreateKeyword`, which returns either an object
        which corresponds to a newly created Dataset inside the
        Database or to an already existed Keyword. The returned
        Keyword-objects are then used to get or create a
        KeywordRegisterFirstReview-object.

        Parameters:
        row:    list
            A dataset, represented by a list.
        header: list
            list of strings, which represent the header-columns.

        Returns:
        obj:    KeywordRegisterFirstReview
            KeywordRegisterFirstReview-object, represent
            the created or in database present Keyword-Dataset
            with the data from row.
        created:    bool
            Indicates, if the KeywordRegisterFirstReview-object
            was created or not.
        """

        objKeyword1, _ = self.getOrCreateKeyword(
            row,
            header,
            "Schlagwort1",
        )
        objKeyword2, _ = self.getOrCreateKeyword(
            row,
            header,
            "Schlagwort2",
        )
        objKeyword3, _ = self.getOrCreateKeyword(
            row,
            header,
            "Schlagwort3",
        )
        objKeyword4, _ = self.getOrCreateKeyword(
            row,
            header,
            "Schlagwort4",
        )
        objKeyword5, _ = self.getOrCreateKeyword(
            row,
            header,
            "Schlagwort5",
        )
        objKeyword6, _ = self.getOrCreateKeyword(
            row,
            header,
            "Schlagwort6",
        )
        objKeyword7, _ = self.getOrCreateKeyword(
            row,
            header,
            "Schlagwort",
        )

        obj, created = KeywordRegisterFirstReview.objects.get_or_create(
            keyword1=objKeyword1,
            keyword2=objKeyword2,
            keyword3=objKeyword3,
            keyword4=objKeyword4,
            keyword5=objKeyword5,
            keyword6=objKeyword6,
            keyword7=objKeyword7,
        )
        return obj, created

    def addOrUpdateRowSubproject(
        self,
        row: list,
        header: list,
        source: str,
    ) -> tuple:
        """Gets or Creates Subproject-object from `row`

        This method adds a Subproject-object to the database, if it is
        not already present. If it is present, a `IntegrityError` is
        thrown by Django and is solved by calling `compareForeignTables`-
        which finds all the differencies in all Tables.

        Parameters:
        row:    list
            A dataset, represented by a list.
        header: list
            list of strings, which represent the header-columns.
        source: str
            String, which specifies the Source of the data. Possible
            values are 'enargus', 'modul', 'tools' or 'schlagwortregister'.

        Returns:
        obj:    KeywordRegisterFirstReview
            KeywordRegisterFirstReview-object, represent
            the created or in database present Schlagwort-Dataset
            with the data from row.
        created:    bool
            Indicates, if the KeywordRegisterFirstReview-object
            was created or not.
        """
        # fill table enargus or/and get the enargus_id
        if source == "enargus":
            obj, created = self.getOrCreateEnargus(row, header)
            enargus_id = obj.enargus_id
            fkz = row[header.index("FKZ")]
            try:
                if (len(
                        Subproject.objects.filter(
                            referenceNumber_id=fkz,
                            enargusData_id=enargus_id)) == 0):
                    Subproject.objects.create(
                        referenceNumber_id=fkz,
                        enargusData_id=enargus_id,
                    )
                    self.stdout.write(self.style.SUCCESS("added: %s" % fkz))
            except IntegrityError:
                currentStateTable = Subproject.objects.filter(
                    referenceNumber_id=fkz, )[0].enargusData
                unvisited = []
                visitedNames = []
                visitedNames.append("subproject")
                unvisited.append([
                    "enargusData",
                    currentStateTable,
                    obj,
                    "Subproject",
                ])
                if currentStateTable is None:
                    verbundbezeichungStr = None
                else:
                    verbundbezeichungStr = (
                        currentStateTable.collaborativeProject)
                self.compareForeignTables(
                    unvisited,
                    visitedNames,
                    {"referenceNumber_id": fkz},
                    verbundbezeichungStr,
                )

        elif source == "modul":
            moduleAssignmentObjNew, created = self.getOrCreateModuleAssignment(
                row,
                header,
            )
            fkz = row[header.index("FKZ")].strip()
            try:
                if (len(
                        Subproject.objects.filter(
                            referenceNumber_id=fkz,
                            moduleAssignment=moduleAssignmentObjNew,
                        )) == 0):
                    Subproject.objects.create(
                        referenceNumber_id=fkz,
                        moduleAssignment=moduleAssignmentObjNew,
                    )
                    self.stdout.write(self.style.SUCCESS("added: %s" % fkz))
            except IntegrityError:
                enargusDataObj = Subproject.objects.filter(
                    referenceNumber_id=fkz, )[0].enargusData

                ModuleAssignmentObj = Subproject.objects.filter(
                    referenceNumber_id=fkz, )[0].moduleAssignment

                unvisited = []
                visitedNames = []
                visitedNames.append("subproject")
                unvisited.append([
                    "moduleAssignment",
                    ModuleAssignmentObj,
                    moduleAssignmentObjNew,
                    "Subproject",
                ])
                if enargusDataObj is None:
                    collaborativeProjectText = None
                else:
                    collaborativeProjectText = (
                        enargusDataObj.collaborativeProject)
                self.compareForeignTables(
                    unvisited,
                    visitedNames,
                    {"referenceNumber_id": fkz},
                    collaborativeProjectText,
                )
        elif source == "schlagwortregister":
            (
                keywordRegisterFirstReviewObj,
                _,
            ) = self.getOrCreateKeywordRegisterFirstReview(
                row,
                header,
            )
            fkz = row[header.index("Förderkennzeichen (0010)")]
            try:
                if (len(
                        Subproject.objects.filter(
                            referenceNumber_id=fkz,
                            keywordsFirstReview=keywordRegisterFirstReviewObj,
                        )) == 0):
                    Subproject.objects.create(
                        referenceNumber_id=fkz,
                        keywordsFirstReview=keywordRegisterFirstReviewObj,
                    )
                    self.stdout.write(self.style.SUCCESS("added: %s" % fkz))
            except IntegrityError:
                currentPartEnargus = Subproject.objects.filter(
                    referenceNumber_id=fkz, )[0].enargusData

                currentObjTagRegisterFirstLook = Subproject.objects.filter(
                    referenceNumber_id=fkz, )[0].keywordsFirstReview
                unvisited = []
                visitedNames = []
                visitedNames.append("teilprojekt")
                unvisited.append([
                    "keywordsFirstReview",
                    currentObjTagRegisterFirstLook,
                    keywordRegisterFirstReviewObj,
                    "Subproject",
                ])
                if currentPartEnargus is None:
                    collaborativeProjectText = None
                else:
                    collaborativeProjectText = (
                        currentPartEnargus.collaborativeProject)

                self.compareForeignTables(
                    unvisited,
                    visitedNames,
                    {"referenceNumber_id": fkz},
                    collaborativeProjectText,
                )
        elif source == "tools":
            obj, created = self.getOrCreateTools(row, header)
            toolsID = obj.id
            toolsName = obj.name
            if len(Tools.objects.filter(name=toolsName)) > 1:
                currentStateTable = Tools.objects.filter(
                    name=toolsName).order_by("id")[0]
                unvisited = []
                visitedNames = []
                unvisited.append([
                    "Tools",
                    currentStateTable,
                    obj,
                    "Tools",
                ])

                self.compareForeignTables(
                    unvisited,
                    visitedNames,
                    {"name": obj.name},
                    obj.name,
                )

    def compareForeignTables(
        self,
        unvisited: list,
        visitedNames: list,
        identifer: dict,
        theme: str,
    ) -> None:
        """Finds all Differences for all Datasets, which point to the same fkz

        Starting from a Database-Conflict the method walks through
        all foreign-tables and compares the values of the two conflicting
        datasets. If the values are different for a attribute, they
        are saved inside an instance of the DatabaseDifference-class.
        At the moment the central table of the database is the
        `Subproject`-Table. New loaded Datasets can update values
        of one Subproject-Tuple, which is represented by a
        `Förderkennzeichen`. If

        unvisited:  list
            list of tables, which were not visited yet. As a first
            entry it contains the name of the Foreign-Table-Column,
            where the datasets are located, which produce a database
            conflict. The second entry holds the Dataset, which is
            currently connected to the fkz, the third entry the
            CSV-state, which is a pending update. The 4th entry
            contains the Name of the parent table, this is most
            likly always `Subproject`
        visitedNames:   list
            List of Tablename, which should not be visited again
        identifer:  dict
            Key-Value-Pair, which identifes the Förderkennzeichen,
            for which two different foreign-Datasets are present.
        theme:
            String, which shortly describes the Förderkennzeichen.
            The String is taken from `enargus.verbundbezeichnung`
            and can also be `None`

        Returns:
        None
        """

        diffCurrentObjDict = {}
        diffPendingObjDict = {}

        if identifer in self.fkzWrittenToYAML:
            raise MultipleFKZDatasets(
                f"""In the .csv-file are multiple datasets 
            with the same fkz {identifer} present. That can lead to problems 
            with tracking the database state and is therefore not supported. 
            Please find the rows in the .csv-file, and decide manually, which 
            dataset should be loaded into the database. The other dataset needs 
            to be deleted from the .csv-file. The data_import script can be 
            reexecuted after these steps.
            """)
        else:
            self.fkzWrittenToYAML.append(identifer)

        currentDBDifferenceObj = DatabaseDifference(
            identifer,
            theme,
        )
        while len(unvisited) > 0:
            currentEntryInUnvisited = unvisited.pop()

            currentForeignTableName = currentEntryInUnvisited[0]
            currentTableObj = currentEntryInUnvisited[1]
            pendingTableObj = currentEntryInUnvisited[2]
            if pendingTableObj is None:
                continue
            parentTableName = currentEntryInUnvisited[3]
            visitedNames.append(f"{parentTableName}.{currentForeignTableName}")
            if currentTableObj is None:
                diffCurrentObjDict[currentForeignTableName] = "None"
                diffPendingObjDict[currentForeignTableName] = ""
                currentDBDifferenceObj.addTable(
                    f"{parentTableName}.{currentForeignTableName}", )
                for columnName in pendingTableObj._meta.get_fields():
                    currentForeignTableStr = (
                        columnName.__str__().strip(">").split(".")[-1])
                    if not columnName.is_relation:
                        penTab = pendingTableObj.__getattribute__(
                            columnName.name)
                        diffPendingObjDict[currentForeignTableName] = (
                            diffPendingObjDict[currentForeignTableName] + "|" +
                            f" {columnName.name}: {str(penTab)}")

                        currentDBDifferenceObj.addDifference(
                            f"{parentTableName}.{currentForeignTableName}",
                            {currentForeignTableStr: None},
                            {
                                currentForeignTableStr:
                                str(
                                    pendingTableObj.__getattribute__(
                                        currentForeignTableStr))
                            },
                        )
                        listOfFieldsInCurrentTable = (
                            pendingTableObj._meta.get_fields())
                        for teilprojektField in listOfFieldsInCurrentTable:
                            currentForeignTableStr = (teilprojektField.__str__(
                            ).strip(">").split(".")[-1])
                            if (teilprojektField.is_relation and
                                    f"{parentTableName}.{currentForeignTableStr}"
                                    not in visitedNames
                                    and not teilprojektField.one_to_many):
                                try:
                                    pendingField = (
                                        pendingTableObj.__getattribute__(
                                            currentForeignTableStr, ))
                                except:
                                    pendingField = None
                                unvisited.append([
                                    currentForeignTableStr,
                                    None,
                                    pendingField,
                                    currentForeignTableName,
                                ])

            else:
                try:
                    listOfFieldsInCurrentTable = (
                        currentTableObj._meta.get_fields())
                except:
                    if len(currentTableObj) > 0:
                        listOfFieldsInCurrentTable = currentTableObj[
                            0]._meta.get_fields()
                    else:
                        listOfFieldsInCurrentTable = []
                if (f"{parentTableName}.{currentForeignTableName}"
                        not in diffCurrentObjDict.keys()):
                    currentDBDifferenceObj.addTable(
                        f"{parentTableName}.{currentForeignTableName}", )
                    diffCurrentObjDict[
                        f"{parentTableName}.{currentForeignTableName}"] = ""
                    diffPendingObjDict[
                        f"{parentTableName}.{currentForeignTableName}"] = ""

                for teilprojektField in listOfFieldsInCurrentTable:
                    currentForeignTableStr = (
                        teilprojektField.__str__().strip(">").split(".")[-1])

                    if (teilprojektField.is_relation
                            and f"{parentTableName}.{currentForeignTableStr}"
                            not in visitedNames
                            and not teilprojektField.one_to_many):
                        if teilprojektField.many_to_many:
                            if currentForeignTableStr != "tools":
                                try:
                                    unvisited.append([
                                        currentForeignTableStr,
                                        currentTableObj.__getattribute__(
                                            currentForeignTableStr).
                                        select_related(),
                                        pendingTableObj.__getattribute__(
                                            currentForeignTableStr).
                                        select_related(),
                                        teilprojektField.model.__name__,
                                    ])
                                except:
                                    pass
                        else:
                            try:
                                unvisited.append([
                                    currentForeignTableStr,
                                    currentTableObj.__getattribute__(
                                        currentForeignTableStr),
                                    pendingTableObj.__getattribute__(
                                        currentForeignTableStr),
                                    teilprojektField.model.__name__,
                                ])
                            except:
                                pass

                    elif not teilprojektField.is_relation:
                        foundDifference = False
                        strDifferencesPending = ""
                        strDifferencesCurrent = ""
                        if "QuerySet" in str(type(pendingTableObj)):
                            strCurrent = f" {currentForeignTableStr}: "
                            strPending = f" {currentForeignTableStr}: "
                            try:
                                pendingTableObj = pendingTableObj.order_by(
                                    "id")
                                currentTableObj = currentTableObj.order_by(
                                    "id")
                            except:
                                pendingTableObj = pendingTableObj.order_by(
                                    "referenceNumber_id")
                                currentTableObj = currentTableObj.order_by(
                                    "referenceNumber_id")

                            if len(currentTableObj) != len(pendingTableObj):
                                foundDifference = True
                            else:
                                for index, currentPendingObj in enumerate(
                                        pendingTableObj):
                                    foundCurrentObj = False
                                    if len(currentTableObj) >= index + 1:
                                        if currentPendingObj.__getattribute__(
                                                currentForeignTableStr
                                        ) != currentTableObj[
                                                index].__getattribute__(
                                                    currentForeignTableStr):
                                            foundDifference = True
                                            break
                                    else:
                                        foundDifference = True
                            if foundDifference:
                                for index, currentPendingObj in enumerate(
                                        pendingTableObj):
                                    strPending += f"{currentPendingObj.__getattribute__(currentForeignTableStr)}, "
                                    strDifferencesPending += f"{currentPendingObj.__getattribute__(currentForeignTableStr)}, "
                                for index, currentManyObj in enumerate(
                                        currentTableObj):
                                    strCurrent += f"{currentManyObj.__getattribute__(currentForeignTableStr)}, "
                                    strDifferencesCurrent += f"{currentManyObj.__getattribute__(currentForeignTableStr)}, "

                                lengthOfStr = np.array(
                                    [len(strCurrent),
                                     len(strPending)])
                                posOfMaxLengthStr = np.argmin(lengthOfStr)
                                numberOfCharacterDifference = np.abs(
                                    lengthOfStr[0] - lengthOfStr[1])
                                if posOfMaxLengthStr == 0:
                                    strCurrent += (
                                        numberOfCharacterDifference * " ")
                                else:
                                    strPending += (
                                        numberOfCharacterDifference * " ")

                                diffCurrentObjDict[
                                    f"{parentTableName}.{currentForeignTableName}"] = (
                                        diffCurrentObjDict[
                                            f"{parentTableName}.{currentForeignTableName}"]
                                        + "|" + strCurrent)
                                diffPendingObjDict[
                                    f"{parentTableName}.{currentForeignTableName}"] = (
                                        diffPendingObjDict[
                                            f"{parentTableName}.{currentForeignTableName}"]
                                        + "|" + strPending)
                                currentDBDifferenceObj.addDifference(
                                    f"{parentTableName}.{currentForeignTableName}",
                                    {
                                        currentForeignTableStr:
                                        strDifferencesCurrent
                                    },
                                    {
                                        currentForeignTableStr:
                                        strDifferencesPending
                                    },
                                )
                        else:
                            if str(
                                    pendingTableObj.__getattribute__(
                                        currentForeignTableStr)) != str(
                                            currentTableObj.__getattribute__(
                                                currentForeignTableStr)):
                                strCurrent = f" {currentForeignTableStr}: {str(currentTableObj.__getattribute__(currentForeignTableStr))}"
                                strPending = f" {currentForeignTableStr}: {str(pendingTableObj.__getattribute__(currentForeignTableStr))}"
                                lengthOfStr = np.array(
                                    [len(strCurrent),
                                     len(strPending)])
                                posOfMaxLengthStr = np.argmin(lengthOfStr)
                                numberOfCharacterDifference = np.abs(
                                    lengthOfStr[0] - lengthOfStr[1])
                                if posOfMaxLengthStr == 0:
                                    strCurrent += (
                                        numberOfCharacterDifference * " ")
                                else:
                                    strPending += (
                                        numberOfCharacterDifference * " ")

                                diffCurrentObjDict[
                                    f"{parentTableName}.{currentForeignTableName}"] = (
                                        diffCurrentObjDict[
                                            f"{parentTableName}.{currentForeignTableName}"]
                                        + "|" + strCurrent)
                                diffPendingObjDict[
                                    f"{parentTableName}.{currentForeignTableName}"] = (
                                        diffPendingObjDict[
                                            f"{parentTableName}.{currentForeignTableName}"]
                                        + "|" + strPending)
                                currentDBDifferenceObj.addDifference(
                                    f"{parentTableName}.{currentForeignTableName}",
                                    {
                                        currentForeignTableStr:
                                        str(
                                            currentTableObj.__getattribute__(
                                                currentForeignTableStr))
                                    },
                                    {
                                        currentForeignTableStr:
                                        str(
                                            pendingTableObj.__getattribute__(
                                                currentForeignTableStr))
                                    },
                                )

        # remove the file-extension
        filename = self.filename.split(".")[0]

        now = datetime.now()

        twoMinutesAgo = now - timedelta(minutes=2)

        # Get the list of files in the directory
        files = os.listdir(self.targetFolder)

        # Initialize the filename variable
        DBdifferenceFileName = None

        # Iterate over the files
        for file in files:
            # Get the full path of the file
            fullPath = os.path.join(self.targetFolder, file)

            # Get the modification time of the file
            modTime = datetime.fromtimestamp(os.path.getmtime(fullPath))

            # If the file was modified in the last 2 minutes, set the filename variable
            if modTime > twoMinutesAgo:
                DBdifferenceFileName = file
                break

        # If no file was modified in the last 2 minutes, create a new file
        if DBdifferenceFileName is None:
            dateString = now.strftime("%d%m%Y_%H%M%S")
            DBdifferenceFileName = f"{filename}_{dateString}.yaml"

        pathToFile = os.path.join(self.targetFolder, DBdifferenceFileName)
        currentDBDifferenceObj.writeToYAML(pathToFile)

    def readCSV(
        self,
        path: str,
    ) -> tuple:
        """This method reads the csv-file, and loads the content into
        the two variables header and data.

        Parameters:
        path:   str

        Returns:
        header: list
            List of headers from the csv-file.
        data:   list
        list, containing the rows from the csv-file.
        """
        with open(path, encoding="utf-8") as csv_file:
            reader = csv.reader(csv_file, delimiter=";")
            header = next(reader)
            data = []
            for row in reader:
                data.append(row)
        return header, data

    def readExcel(
        self,
        path: str,
    ) -> tuple:
        """This method reads the excel-file, and loads the content into
        the two variables header and data.

        Parameters:
        path:   str

        Returns:
        header: list
            List of headers from the excel-file.
        data:   list
            list, containing the rows from the excel-file.
        """
        df = pd.read_excel(path)
        df = df.fillna("")
        header = list(df.columns)
        data = df.values.tolist()
        return header, data

    def handle(
        self,
        *args: tuple,
        **options: dict,
    ) -> None:
        """This method is called from the manage.py when the 'data_import'
        command is called together with the manage.py.

        Parameters:
        *args:  tuple
            Tuple of arguments, which get unpacked.
        **options:  dict
            Dictionary, contains the parsed argument, given at the CLI
            when calling `python manage.py data_import`

        Returns:
        None
        """

        pathFile = options["pathCSV"][0]
        if pathFile.endswith(".csv"):
            header, data = self.readCSV(pathFile)
        elif pathFile.endswith(".xlsx"):
            header, data = self.readExcel(pathFile)
        else:
            CommandError(
                "Invalid file format. Please provide a .csv or .xlsx file.")
            return None
        pathStr, filename = os.path.split(pathFile)
        self.filename = filename
        self.targetFolder = options["targetFolder"][0]

        # header, data = self.readCSV(pathCSV)
        for row in data:
            if "modulzuordnung" in filename:
                self.addOrUpdateRowSubproject(row, header, "modul")
            elif "enargus" in filename:
                self.addOrUpdateRowSubproject(row, header, "enargus")
            elif "tool" in filename or "Tool" in filename:
                self.addOrUpdateRowSubproject(row, header, "tools")
            elif "schlagwoerter" in filename:
                self.addOrUpdateRowSubproject(row, header,
                                              "schlagwortregister")
            elif "weatherdata" in filename:
                self.getOrCreateWeatherdata(row, header)
            elif "publications" in filename:
                self.getOrCreatePublications(row, header)
            elif "use_cases" in filename:
                self.getOrCreateUseCases(row, header)
            elif "criteriaCatalog" in filename:
                self.getOrCreateCriteriaCatalog(row, header)
            elif "component" in filename:
                self.getOrCreateComponent(row, header)
            elif "environmentalImpact" in filename:
                self.getOrCreateEnvironmentalImpact(row, header)
            elif "DataSufficiency" in filename:
                self.getOrCreateDataSufficiency(row, header)
            elif "businessModels" in filename:
                self.getOrCreateBusinessModel(row, header)
            elif "userIntegration" in filename:
                self.getOrCreateUserIntegration(row, header)
            else:
                CommandError(
                    "Cant detect type of data. Please add 'modulzuordnung', 'enargus', 'Tools' or 'weatherdata' to Filename to make detection possible."
                )
                return None
        # self.stdout.write(self.style.SUCCESS('Successfully executed command'))

    def _correctReadInValue(self, readInString):
        """Correct the read in value from the csv-file.

        This method corrects the read in value from the csv-file,
        by removing whitespaces at the beginning and end of the
        string.

        readInString:   str
            String, which represents the read in value from the csv-file.
        """

        if isinstance(readInString, float) and math.isnan(readInString):
            return ""
        if readInString == "":
            return ""
        splitStringToSeeIfList = readInString.split(",")
        splitStringToSeeIfList = [
            item for item in splitStringToSeeIfList if item
        ]
        if len(splitStringToSeeIfList) > 0:
            for index, listElement in enumerate(splitStringToSeeIfList):
                if listElement[0] == " ":
                    listElement = listElement[1:]
                if listElement[-1] == " ":
                    listElement = listElement[:-1]
                splitStringToSeeIfList[index] = listElement
            return splitStringToSeeIfList
        else:
            if readInString[0] == " ":
                readInString = readInString[1:]
            if readInString[-1] == " ":
                readInString = readInString[:-1]
            return readInString

    def _selectNearestMatch(self, categoryString: str,
                            djangoModel: Model) -> str:
        """Return closest match for categoryString in djangoModel

        This method returns the closest match for `categoryString` in `djangoModel`
        by using the difflib.get_close_matches-function. Thereby the cutoff is set
        to 80 %. That means if the closest match is below 80 %, an error message
        is printed and an empty string is returned.

        categoryStr:    str
            String, which represents the category, which should be matched.
        djangoModel:    Model
            Django-Model, which represents the table, in which the closest match is searched.

        Returns:
        str
            String, which represents the closest match for `categoryString` in `djangoModel`.

        """

        # get names of all djangoModel-objects
        if djangoModel.__name__ == "Subproject":
            attributeNameInModel = "referenceNumber_id"
        elif djangoModel.__name__ == "Norm":
            attributeNameInModel = "title"
        else:
            attributeNameInModel = (djangoModel.__name__[0].lower() +
                                    djangoModel.__name__[1:])
        allNames = [
            x.__getattribute__(attributeNameInModel)
            for x in djangoModel.objects.all()
        ]

        # get the closest match
        listOfClosestMatches = difflib.get_close_matches(categoryString,
                                                         allNames,
                                                         n=1,
                                                         cutoff=0.8)
        if len(listOfClosestMatches) > 0:
            return listOfClosestMatches[0]
        else:
            if (djangoModel.__name__ != "Subproject"
                    and djangoModel.__name__ != "Norm"):
                try:
                    newlyCreatedRow = djangoModel.objects.create(
                        **{attributeNameInModel: categoryString})
                except:
                    breakpoint()
                self.stdout.write(
                    f"No nearest match for {categoryString} in {djangoModel} was found. {categoryString} is created inside of {djangoModel}",
                    ending="",
                )
                return newlyCreatedRow.__getattribute__(attributeNameInModel)

    def _iterateThroughListOfStrings(self, listOfStrings: list,
                                     djangoModel: Model):
        """ """
        listOfModifiedStrings = []
        for curretnCategoryString in listOfStrings:
            modifiedStr = self._selectNearestMatch(curretnCategoryString,
                                                   djangoModel)
            listOfModifiedStrings.append(modifiedStr)
        return listOfModifiedStrings

    def add_arguments(
        self,
        parser,
    ) -> None:
        """This method parses the arguments, which where given when
        calling the data_import-command together with the manage.py.
        The Arguments are then given to the handle-method, and can
        be accessed as python-variables.

        Parameters:
        parser: django.parser
        Django parser object, which handles the parsing of the command
        and arguments.

        Returns:
        None
        """
        parser.add_argument("pathCSV", nargs="+", type=str)
        parser.add_argument("targetFolder", nargs="+", type=str)
