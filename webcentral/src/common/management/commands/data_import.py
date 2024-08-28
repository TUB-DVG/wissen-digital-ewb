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
import importlib
import os
import math

from django.core.management.base import BaseCommand, CommandError
from django.db.models import Model
from django.conf import settings
import numpy as np
import pandas as pd

from criteria_catalog.models import (
    CriteriaCatalog,
    Topic,
    Tag,
)
from component_list.models import (
    Component,
    ComponentClass,
    Category,
)
from positive_environmental_impact.models import EnvironmentalImpact
from data_sufficiency.models import (
    DataSufficiency,
)

from businessModel.models import (
    BusinessModel,
)

from user_integration.models import (
    ProArgument,
    ConArgument,
    Literature,
    ProcedureItem,
    UserEngagement,
)

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
            row[header.index("focus")]
        )
        focusList = self._iterateThroughListOfStrings(processedFocusList, Focus)
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
        obj, created = Keyword.objects.get_or_create(
            keyword=keywordFromCSV,
        )
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
                if (
                    len(
                        Subproject.objects.filter(
                            referenceNumber_id=fkz, enargusData_id=enargus_id
                        )
                    )
                    == 0
                ):
                    Subproject.objects.create(
                        referenceNumber_id=fkz,
                        enargusData_id=enargus_id,
                    )
                    self.stdout.write(self.style.SUCCESS("added: %s" % fkz))
            except IntegrityError:
                currentStateTable = Subproject.objects.filter(
                    referenceNumber_id=fkz,
                )[0].enargusData
                unvisited = []
                visitedNames = []
                visitedNames.append("subproject")
                unvisited.append(
                    [
                        "enargusData",
                        currentStateTable,
                        obj,
                        "Subproject",
                    ]
                )
                if currentStateTable is None:
                    verbundbezeichungStr = None
                else:
                    verbundbezeichungStr = (
                        currentStateTable.collaborativeProject
                    )
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
                if (
                    len(
                        Subproject.objects.filter(
                            referenceNumber_id=fkz,
                            moduleAssignment=moduleAssignmentObjNew,
                        )
                    )
                    == 0
                ):
                    Subproject.objects.create(
                        referenceNumber_id=fkz,
                        moduleAssignment=moduleAssignmentObjNew,
                    )
                    self.stdout.write(self.style.SUCCESS("added: %s" % fkz))
            except IntegrityError:
                enargusDataObj = Subproject.objects.filter(
                    referenceNumber_id=fkz,
                )[0].enargusData

                ModuleAssignmentObj = Subproject.objects.filter(
                    referenceNumber_id=fkz,
                )[0].moduleAssignment

                unvisited = []
                visitedNames = []
                visitedNames.append("subproject")
                unvisited.append(
                    [
                        "moduleAssignment",
                        ModuleAssignmentObj,
                        moduleAssignmentObjNew,
                        "Subproject",
                    ]
                )
                if enargusDataObj is None:
                    collaborativeProjectText = None
                else:
                    collaborativeProjectText = (
                        enargusDataObj.collaborativeProject
                    )
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
                if (
                    len(
                        Subproject.objects.filter(
                            referenceNumber_id=fkz,
                            keywordsFirstReview=keywordRegisterFirstReviewObj,
                        )
                    )
                    == 0
                ):
                    Subproject.objects.create(
                        referenceNumber_id=fkz,
                        keywordsFirstReview=keywordRegisterFirstReviewObj,
                    )
                    self.stdout.write(self.style.SUCCESS("added: %s" % fkz))
            except IntegrityError:
                currentPartEnargus = Subproject.objects.filter(
                    referenceNumber_id=fkz,
                )[0].enargusData

                currentObjTagRegisterFirstLook = Subproject.objects.filter(
                    referenceNumber_id=fkz,
                )[0].keywordsFirstReview
                unvisited = []
                visitedNames = []
                visitedNames.append("teilprojekt")
                unvisited.append(
                    [
                        "keywordsFirstReview",
                        currentObjTagRegisterFirstLook,
                        keywordRegisterFirstReviewObj,
                        "Subproject",
                    ]
                )
                if currentPartEnargus is None:
                    collaborativeProjectText = None
                else:
                    collaborativeProjectText = (
                        currentPartEnargus.collaborativeProject
                    )

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
                    name=toolsName
                ).order_by("id")[0]
                unvisited = []
                visitedNames = []
                unvisited.append(
                    [
                        "Tools",
                        currentStateTable,
                        obj,
                        "Tools",
                    ]
                )

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
            """
            )
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
                    f"{parentTableName}.{currentForeignTableName}",
                )
                for columnName in pendingTableObj._meta.get_fields():
                    currentForeignTableStr = (
                        columnName.__str__().strip(">").split(".")[-1]
                    )
                    if not columnName.is_relation:
                        penTab = pendingTableObj.__getattribute__(
                            columnName.name
                        )
                        diffPendingObjDict[currentForeignTableName] = (
                            diffPendingObjDict[currentForeignTableName]
                            + "|"
                            + f" {columnName.name}: {str(penTab)}"
                        )

                        currentDBDifferenceObj.addDifference(
                            f"{parentTableName}.{currentForeignTableName}",
                            {currentForeignTableStr: None},
                            {
                                currentForeignTableStr: str(
                                    pendingTableObj.__getattribute__(
                                        currentForeignTableStr
                                    )
                                )
                            },
                        )
                        listOfFieldsInCurrentTable = (
                            pendingTableObj._meta.get_fields()
                        )
                        for teilprojektField in listOfFieldsInCurrentTable:
                            currentForeignTableStr = (
                                teilprojektField.__str__()
                                .strip(">")
                                .split(".")[-1]
                            )
                            if (
                                teilprojektField.is_relation
                                and f"{parentTableName}.{currentForeignTableStr}"
                                not in visitedNames
                                and not teilprojektField.one_to_many
                            ):
                                try:
                                    pendingField = (
                                        pendingTableObj.__getattribute__(
                                            currentForeignTableStr,
                                        )
                                    )
                                except:
                                    pendingField = None
                                unvisited.append(
                                    [
                                        currentForeignTableStr,
                                        None,
                                        pendingField,
                                        currentForeignTableName,
                                    ]
                                )

            else:
                try:
                    listOfFieldsInCurrentTable = (
                        currentTableObj._meta.get_fields()
                    )
                except:
                    if len(currentTableObj) > 0:
                        listOfFieldsInCurrentTable = currentTableObj[
                            0
                        ]._meta.get_fields()
                    else:
                        listOfFieldsInCurrentTable = []
                if (
                    f"{parentTableName}.{currentForeignTableName}"
                    not in diffCurrentObjDict.keys()
                ):
                    currentDBDifferenceObj.addTable(
                        f"{parentTableName}.{currentForeignTableName}",
                    )
                    diffCurrentObjDict[
                        f"{parentTableName}.{currentForeignTableName}"
                    ] = ""
                    diffPendingObjDict[
                        f"{parentTableName}.{currentForeignTableName}"
                    ] = ""

                for teilprojektField in listOfFieldsInCurrentTable:
                    currentForeignTableStr = (
                        teilprojektField.__str__().strip(">").split(".")[-1]
                    )

                    if (
                        teilprojektField.is_relation
                        and f"{parentTableName}.{currentForeignTableStr}"
                        not in visitedNames
                        and not teilprojektField.one_to_many
                    ):
                        if teilprojektField.many_to_many:
                            if currentForeignTableStr != "tools":
                                try:
                                    unvisited.append(
                                        [
                                            currentForeignTableStr,
                                            currentTableObj.__getattribute__(
                                                currentForeignTableStr
                                            ).select_related(),
                                            pendingTableObj.__getattribute__(
                                                currentForeignTableStr
                                            ).select_related(),
                                            teilprojektField.model.__name__,
                                        ]
                                    )
                                except:
                                    pass
                        else:
                            try:
                                unvisited.append(
                                    [
                                        currentForeignTableStr,
                                        currentTableObj.__getattribute__(
                                            currentForeignTableStr
                                        ),
                                        pendingTableObj.__getattribute__(
                                            currentForeignTableStr
                                        ),
                                        teilprojektField.model.__name__,
                                    ]
                                )
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
                                pendingTableObj = pendingTableObj.order_by("id")
                                currentTableObj = currentTableObj.order_by("id")
                            except:
                                pendingTableObj = pendingTableObj.order_by(
                                    "referenceNumber_id"
                                )
                                currentTableObj = currentTableObj.order_by(
                                    "referenceNumber_id"
                                )

                            if len(currentTableObj) != len(pendingTableObj):
                                foundDifference = True
                            else:
                                for index, currentPendingObj in enumerate(
                                    pendingTableObj
                                ):
                                    foundCurrentObj = False
                                    if len(currentTableObj) >= index + 1:
                                        if currentPendingObj.__getattribute__(
                                            currentForeignTableStr
                                        ) != currentTableObj[
                                            index
                                        ].__getattribute__(
                                            currentForeignTableStr
                                        ):
                                            foundDifference = True
                                            break
                                    else:
                                        foundDifference = True
                            if foundDifference:
                                for index, currentPendingObj in enumerate(
                                    pendingTableObj
                                ):
                                    strPending += f"{currentPendingObj.__getattribute__(currentForeignTableStr)}, "
                                    strDifferencesPending += f"{currentPendingObj.__getattribute__(currentForeignTableStr)}, "
                                for index, currentManyObj in enumerate(
                                    currentTableObj
                                ):
                                    strCurrent += f"{currentManyObj.__getattribute__(currentForeignTableStr)}, "
                                    strDifferencesCurrent += f"{currentManyObj.__getattribute__(currentForeignTableStr)}, "

                                lengthOfStr = np.array(
                                    [len(strCurrent), len(strPending)]
                                )
                                posOfMaxLengthStr = np.argmin(lengthOfStr)
                                numberOfCharacterDifference = np.abs(
                                    lengthOfStr[0] - lengthOfStr[1]
                                )
                                if posOfMaxLengthStr == 0:
                                    strCurrent += (
                                        numberOfCharacterDifference * " "
                                    )
                                else:
                                    strPending += (
                                        numberOfCharacterDifference * " "
                                    )

                                diffCurrentObjDict[
                                    f"{parentTableName}.{currentForeignTableName}"
                                ] = (
                                    diffCurrentObjDict[
                                        f"{parentTableName}.{currentForeignTableName}"
                                    ]
                                    + "|"
                                    + strCurrent
                                )
                                diffPendingObjDict[
                                    f"{parentTableName}.{currentForeignTableName}"
                                ] = (
                                    diffPendingObjDict[
                                        f"{parentTableName}.{currentForeignTableName}"
                                    ]
                                    + "|"
                                    + strPending
                                )
                                currentDBDifferenceObj.addDifference(
                                    f"{parentTableName}.{currentForeignTableName}",
                                    {
                                        currentForeignTableStr: strDifferencesCurrent
                                    },
                                    {
                                        currentForeignTableStr: strDifferencesPending
                                    },
                                )
                        else:
                            if str(
                                pendingTableObj.__getattribute__(
                                    currentForeignTableStr
                                )
                            ) != str(
                                currentTableObj.__getattribute__(
                                    currentForeignTableStr
                                )
                            ):
                                strCurrent = f" {currentForeignTableStr}: {str(currentTableObj.__getattribute__(currentForeignTableStr))}"
                                strPending = f" {currentForeignTableStr}: {str(pendingTableObj.__getattribute__(currentForeignTableStr))}"
                                lengthOfStr = np.array(
                                    [len(strCurrent), len(strPending)]
                                )
                                posOfMaxLengthStr = np.argmin(lengthOfStr)
                                numberOfCharacterDifference = np.abs(
                                    lengthOfStr[0] - lengthOfStr[1]
                                )
                                if posOfMaxLengthStr == 0:
                                    strCurrent += (
                                        numberOfCharacterDifference * " "
                                    )
                                else:
                                    strPending += (
                                        numberOfCharacterDifference * " "
                                    )

                                diffCurrentObjDict[
                                    f"{parentTableName}.{currentForeignTableName}"
                                ] = (
                                    diffCurrentObjDict[
                                        f"{parentTableName}.{currentForeignTableName}"
                                    ]
                                    + "|"
                                    + strCurrent
                                )
                                diffPendingObjDict[
                                    f"{parentTableName}.{currentForeignTableName}"
                                ] = (
                                    diffPendingObjDict[
                                        f"{parentTableName}.{currentForeignTableName}"
                                    ]
                                    + "|"
                                    + strPending
                                )
                                currentDBDifferenceObj.addDifference(
                                    f"{parentTableName}.{currentForeignTableName}",
                                    {
                                        currentForeignTableStr: str(
                                            currentTableObj.__getattribute__(
                                                currentForeignTableStr
                                            )
                                        )
                                    },
                                    {
                                        currentForeignTableStr: str(
                                            pendingTableObj.__getattribute__(
                                                currentForeignTableStr
                                            )
                                        )
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

    def _checkIfInInstalledApps(self, type_of_data):
        """Check if user given argument `type_of_data` matches
        one of the installed apps. If it does, check if a `data_import`-module
        is present in that app.
        """
        installed_django_apps = settings.INSTALLED_APPS
        app_names = [app.split(".")[0] for app in installed_django_apps]
        if type_of_data in app_names:
            if (
                importlib.util.find_spec(type_of_data + ".data_import")
                is not None
            ):
                return importlib.import_module(type_of_data + ".data_import")
        raise CommandError(
            "specified type_of_data has no corresponding app or has no data_import.py in the app."
        )

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
        filePathToData = options["pathCSV"][0]

        type_of_data = options["type_of_data"][0]
        data_import_module = self._checkIfInInstalledApps(type_of_data)

        # else:
        #     raise CommandError(
        #         "Invalid file format. Please provide a .csv or .xlsx file.")
        # pathStr, filename = os.path.split(filePathToData)
        # self.filename = filename
        # self.targetFolder = options["targetFolder"][0]

        appDataImportObj = data_import_module.DataImportApp(filePathToData)
        header, data = appDataImportObj.load()
        appDataImportObj.importList(header, data)

    def _processListInput(self, inputStr):
        """Process a cell, which includes a list of elements"""
        returnList = []
        for element in inputStr.split(";"):
            if not self._checkIfOnlyContainsSpaces(element):
                returnList.append(element)

        return returnList

    def _checkIfOnlyContainsSpaces(self, inputStr):
        """Check if the inputStr only contains whitespaces.

        This method checks if the inputStr only contains whitespaces.
        If this is the case, the method returns True, otherwise False.

        Parameters:
        inputStr:   str
            String, which should be checked, if it only contains whitespaces.

        Returns:
        bool
            True, if the inputStr only contains whitespaces, otherwise False.
        """
        return all(x.isspace() for x in inputStr)

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

    def _selectNearestMatch(
        self, categoryString: str, djangoModel: Model
    ) -> str:
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
            attributeNameInModel = (
                djangoModel.__name__[0].lower() + djangoModel.__name__[1:]
            )
        allNames = [
            x.__getattribute__(attributeNameInModel)
            for x in djangoModel.objects.all()
        ]

        # get the closest match
        listOfClosestMatches = difflib.get_close_matches(
            categoryString, allNames, n=1, cutoff=0.8
        )
        if len(listOfClosestMatches) > 0:
            return listOfClosestMatches[0]
        else:
            if (
                djangoModel.__name__ != "Subproject"
                and djangoModel.__name__ != "Norm"
            ):
                try:
                    newlyCreatedRow = djangoModel.objects.create(
                        **{attributeNameInModel: categoryString}
                    )
                except:
                    breakpoint()
                self.stdout.write(
                    f"No nearest match for {categoryString} in {djangoModel} was found. {categoryString} is created inside of {djangoModel}",
                    ending="",
                )
                return newlyCreatedRow.__getattribute__(attributeNameInModel)

    def _iterateThroughListOfStrings(
        self, listOfStrings: list, djangoModel: Model
    ):
        """ """
        listOfModifiedStrings = []
        for curretnCategoryString in listOfStrings:
            modifiedStr = self._selectNearestMatch(
                curretnCategoryString, djangoModel
            )
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
        parser.add_argument("type_of_data", nargs="+", type=str)

        parser.add_argument("pathCSV", nargs="+", type=str)
        # parser.add_argument("targetFolder", nargs="+", type=str)
