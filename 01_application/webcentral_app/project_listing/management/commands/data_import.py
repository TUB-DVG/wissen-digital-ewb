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
containing the Django `manage.py`. From there, te following 
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
import pdb
from encodings import utf_8
import os
import datetime

from django.core.management.base import BaseCommand
import numpy as np

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
    IntegrityError,
)
from keywords.models import (
    Keyword,
    KeywordRegisterFirstReview,
)
from tools_over.models import Tools
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
        currentTimestamp = datetime.datetime.now()
        self.DBdifferenceFileName = (str(int(currentTimestamp.timestamp())) 
                                    + ".yaml"
        )

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
        federalMinistry = row[header.index('Bundesministerium')]
        projectBody = row[header.index('Projekttraeger')]
        supportProgram = row[header.index('Foerderprogramm')]
        researchProgram = row[header.index('Forschungsprogramm')]
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

        if who == 'zwe':
            postalCode = row[header.index('PLZ_ZWE')]
            location = row[header.index('Ort_ZWE')]
            country = row[header.index('Land_ZWE')]
            adress = row[header.index('Adress_ZWE')]
        elif who == 'as':
            postalCode = row[header.index('PLZ_AS')]
            location = row[header.index('Ort_AS')]
            country = row[header.index('Land_AS')]
            adress = row[header.index('Adress_AS')]

        obj, created = Address.objects.get_or_create(
            plz=postalCode,
            location=location,
            state=country,
            address=adress,
        )
        return obj, created

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
        name = row[header.index('Name_pl')]
        firstNameFromCSV = row[header.index('Vorname_pl')]
        titel = row[header.index('Titel_pl')]
        email = row[header.index('Email_pl')]
        obj, created = Person.objects.get_or_create(
            surname=name,
            firstName=firstNameFromCSV,
            title=titel,
            email=email,
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
        textFromCSV = row[header.index('Leistungsplan_Sys_Text')]
        idFromCSV = row[header.index('Leistungsplan_Sys_Nr')]

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
            'zwe',
        )
        # doneeAdressId = objAnsZwe.anschrift_id

        # content = row[number of the columns of the row]
        nameFromCSV = row[header.index('Name_ZWE')]
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
        objAnsAs, _ = self.getOrCreateAdress(row, header, 'as')

        nameFromCSV = row[header.index('Name_AS')]
        return ExecutingEntity.objects.get_or_create(
            name=nameFromCSV,
            address=objAnsAs,
        )

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
        objRAndDPlanning, _ = self.getOrCreateRAndDPlanningCategory(row, header)
        objPerson, _ = self.getOrCreatePerson(row, header)
        objFurtherFunding, _ = self.getOrCreateFurtherFundingInformation(
            row, 
            header,
        )

        durationBegin = row[header.index('Laufzeitbeginn')]
        durationEnd = row[header.index('Laufzeitende')]
        theme = row[header.index('Thema')]
        clusterName = row[header.index('Verbundbezeichung')]
        fundingSum = float(row[header.index('Foerdersumme_EUR')])
        shortDescriptionDe = row[header.index('Kurzbeschreibung_de')]
        shortDescriptionEn = row[header.index('Kurzbeschreibung_en')]
        database = row[header.index('Datenbank')]
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

        priority1FromCSV = row[header.index('modulzuordnung_ptj_1')]
        priority2FromCSV = row[header.index('modulzuordnung_ptj_2')]
        priority3FromCSV = row[header.index('modulzuordnung_ptj_3')]
        priority4FromCSV = row[header.index('modulzuordnung_ptj_4')]
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

        description = row[header.index('Tool')]
        shortDesciption = row[header.index('Kurzbeschreibung')]
        applicationArea = row[header.index('Anwendungsbereich')]
        category = row[header.index('Kategorie')]
        lifeCyclePhase = row[header.index('Lebenszyklusphase')]
        userInterface = row[header.index('Nutzerschnittstelle')]
        targetGroup = row[header.index('Zielgruppe')]
        lastUpdate= row[header.index('letztes Update')]
        license = row[header.index('Lizenz')]
        furtherInfos = row[header.index('weitere Informationen')]
        alternatives = row[header.index('Alternativen')]
        concreteApplication = row[
            header.index('konkrete Anwendung in EWB Projekten')
        ]

        obj, created = Tools.objects.get_or_create(
            name=description,
            shortDescription=shortDesciption,
            applicationArea=applicationArea,
            usage=category,
            lifeCyclePhase=lifeCyclePhase,
            userInterface=userInterface,
            targetGroup=targetGroup,
            lastUpdate=lastUpdate,
            licence=license,
            furtherInformation=furtherInfos,
            alternatives=alternatives,
            specificApplication=concreteApplication,
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

        dataService = row[header.index('data_service')]
        shortDescription = row[header.index('short_description')]
        provider = row[header.index('provider')]
        furtherInfos = row[header.index('further_information')]
        dataUrl = row[header.index('data_url')]
        logoUrl = row[header.index('logo_url')]
        applications = row[header.index('applications')]
        lastUpdate = row[header.index('last_update')]
        license = row[header.index('license')]
        category = row[header.index('category')]
        longDescription = row[header.index('long_description')]

        obj, created = Weatherdata.objects.get_or_create(
            data_service = dataService,
            short_description = shortDescription,
            provider = provider,
            further_information = furtherInfos,
            data_url = dataUrl,
            logo_url = logoUrl,
            applications = applications,
            last_update = lastUpdate,
            license = license,
            category = category,
            long_description = longDescription
        )
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
            'Schlagwort1',
        )
        objKeyword2, _ = self.getOrCreateKeyword(
            row, 
            header, 
            'Schlagwort2',
        )
        objKeyword3, _ = self.getOrCreateKeyword(
            row, 
            header, 
            'Schlagwort3',
        )
        objKeyword4, _ = self.getOrCreateKeyword(
            row, 
            header, 
            'Schlagwort4',
        )        
        objKeyword5, _ = self.getOrCreateKeyword(
            row, 
            header, 
            'Schlagwort5',
        )
        objKeyword6, _ = self.getOrCreateKeyword(
            row, 
            header, 
            'Schlagwort6',
        )
        objKeyword7, _ = self.getOrCreateKeyword(
            row, 
            header, 
            'Schlagwort',
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
            values are 'enargus', 'modul' or 'schlagwortregister'.

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
        if source == 'enargus':
            obj, created = self.getOrCreateEnargus(row, header)
            enargus_id = obj.enargus_id
            fkz = row[header.index('FKZ')]            
            try:
                if len(Subproject.objects.filter(
                    referenceNumber_id=fkz, 
                    enargusData_id=enargus_id
                )) == 0:
                    Subproject.objects.create(
                        referenceNumber_id=fkz,
                        enargusData_id= enargus_id,
                    )
                    print('added: %s' %fkz)
            except IntegrityError:
                currentStateTable = Subproject.objects.filter(
                    referenceNumber_id=fkz,
                )[0].enargusData
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
                    verbundbezeichungStr = currentStateTable.collaborativeProject
                self.compareForeignTables(
                    unvisited, 
                    visitedNames, 
                    {"referenceNumber_id": fkz}, 
                    verbundbezeichungStr,
                )


        elif source == 'modul':
            moduleAssignmentObjNew, created = self.getOrCreateModuleAssignment(
                row, 
                header,
            )
            #modId = obj.moduleAssignment_id
            fkz = row[header.index('FKZ')].strip()
            try:
                if len(Subproject.objects.filter(
                    referenceNumber_id=fkz, 
                    moduleAssignment=moduleAssignmentObjNew,
                )) == 0:
                    Subproject.objects.create(
                        referenceNumber_id=fkz,
                        moduleAssignment=moduleAssignmentObjNew,
                    )
                    print('added: %s' %fkz)
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
                unvisited.append([
                    "moduleAssignment", 
                    ModuleAssignmentObj, 
                    moduleAssignmentObjNew, 
                    "Subproject",
                ])
                if enargusDataObj is None:
                    collaborativeProjectText = None
                else:
                    collaborativeProjectText = enargusDataObj.collaborativeProject
                self.compareForeignTables(
                    unvisited, 
                    visitedNames, 
                    {"referenceNumber_id": fkz}, 
                    collaborativeProjectText,
                )
        elif source == 'schlagwortregister':
            keywordRegisterFirstReviewObj, _ = self.getOrCreateKeywordRegisterFirstReview(
                row, 
                header,
            )
            fkz = row[header.index('Förderkennzeichen (0010)')]
            try:
                if len(Subproject.objects.filter(
                    referenceNumber_id=fkz, 
                    keywordsFirstReview=keywordRegisterFirstReviewObj,
                )) == 0:
                    Subproject.objects.create(
                        referenceNumber_id=fkz,
                        keywordsFirstReview=keywordRegisterFirstReviewObj,
                    )
                    print('added: %s' %fkz)
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
                unvisited.append([
                    "keywordsFirstReview", 
                    currentObjTagRegisterFirstLook, 
                    keywordRegisterFirstReviewObj, 
                    "Subproject",
                ])
                if currentPartEnargus is None:
                    collaborativeProjectText = None
                else:
                    collaborativeProjectText = currentPartEnargus.collaborativeProject
                
                
                self.compareForeignTables(
                    unvisited, 
                    visitedNames, 
                    {"referenceNumber_id": fkz}, 
                    collaborativeProjectText,
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
            raise MultipleFKZDatasets(f"""In the .csv-file are multiple datasets 
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
                    f"{parentTableName}.{currentForeignTableName}",
                )
                for columnName in pendingTableObj._meta.get_fields():
                    currentForeignTableStr = columnName.__str__().strip(">").\
                        split(".")[-1]
                    if not columnName.is_relation:
                        penTab = pendingTableObj.__getattribute__(columnName.name)
                        diffPendingObjDict[currentForeignTableName] = (
                           diffPendingObjDict[currentForeignTableName] 
                           + "|" 
                           + f" {columnName.name}: {str(penTab)}"
                        )

                        currentDBDifferenceObj.addDifference(
                            f"{parentTableName}.{currentForeignTableName}", 
                            {currentForeignTableStr: None}, 
                            {currentForeignTableStr: 
                             str(pendingTableObj.__getattribute__(currentForeignTableStr))},
                             )
                        listOfFieldsInCurrentTable = pendingTableObj._meta.get_fields()
                        for teilprojektField in listOfFieldsInCurrentTable:
                            
                            currentForeignTableStr = teilprojektField.__str__()\
                                .strip(">").split(".")[-1]
                            if (
                                teilprojektField.is_relation 
                                and f"{parentTableName}.{currentForeignTableStr}" not in visitedNames 
                                and not teilprojektField.one_to_many
                            ):
                                try: 
                                    pendingField = pendingTableObj.__getattribute__(
                                        currentForeignTableStr,
                                    )
                                except:
                                    pendingField = None
                                unvisited.append([
                                    currentForeignTableStr, 
                                    None, 
                                    pendingField, 
                                    currentForeignTableName,
                                ])     
                  
            else:
                listOfFieldsInCurrentTable = currentTableObj._meta.get_fields()
                
                if f"{parentTableName}.{currentForeignTableName}" not in diffCurrentObjDict.keys():
                    currentDBDifferenceObj.addTable(
                        f"{parentTableName}.{currentForeignTableName}",
                    )
                    diffCurrentObjDict[f"{parentTableName}.{currentForeignTableName}"] = ""
                    diffPendingObjDict[f"{parentTableName}.{currentForeignTableName}"] = ""

                for teilprojektField in listOfFieldsInCurrentTable:
                    currentForeignTableStr = teilprojektField.__str__().strip(">").split(".")[-1]
                    
                    if (
                        teilprojektField.is_relation 
                        and f"{parentTableName}.{currentForeignTableStr}" not in visitedNames 
                        and not teilprojektField.one_to_many
                    ):
                        try:
                            unvisited.append([
                                currentForeignTableStr, 
                                currentTableObj.__getattribute__(currentForeignTableStr), 
                                pendingTableObj.__getattribute__(currentForeignTableStr), 
                                teilprojektField.model.__name__,
                            ])
                        except:
                            pass
                    elif not teilprojektField.is_relation:
                        try:
                            if (
                                str(pendingTableObj\
                                    .__getattribute__(currentForeignTableStr)) 
                                != str(currentTableObj\
                                       .__getattribute__(currentForeignTableStr))
                                ):
                                strCurrent = f" {currentForeignTableStr}: {str(currentTableObj.__getattribute__(currentForeignTableStr))}"
                                strPending = f" {currentForeignTableStr}: {str(pendingTableObj.__getattribute__(currentForeignTableStr))}"
                                lengthOfStr = np.array([len(strCurrent), len(strPending)])
                                posOfMaxLengthStr = np.argmin(lengthOfStr)
                                numberOfCharacterDifference = np.abs(lengthOfStr[0] - lengthOfStr[1])
                                if posOfMaxLengthStr == 0:
                                    strCurrent += numberOfCharacterDifference*" "
                                else:
                                    strPending += numberOfCharacterDifference*" "
                            
                                diffCurrentObjDict[
                                    f"{parentTableName}.{currentForeignTableName}"
                                ] = (diffCurrentObjDict[f"{parentTableName}.{currentForeignTableName}"] 
                                    + "|" 
                                    + strCurrent
                                )
                                diffPendingObjDict[
                                    f"{parentTableName}.{currentForeignTableName}"
                                ] = (diffPendingObjDict[f"{parentTableName}.{currentForeignTableName}"] 
                                     + "|" 
                                     + strPending
                                )
                                currentDBDifferenceObj.addDifference(
                                    f"{parentTableName}.{currentForeignTableName}", 
                                    {currentForeignTableStr: 
                                     str(currentTableObj.__getattribute__(currentForeignTableStr))}, 
                                    {currentForeignTableStr: 
                                     str(pendingTableObj.__getattribute__(currentForeignTableStr))},
                                )   
                        except:
                            pass
        
        pathToFile = os.path.join(self.targetFolder, self.DBdifferenceFileName)   
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
        with open(path, encoding='utf-8') as csv_file:
            reader = csv.reader(csv_file, delimiter=';')
            header = next(reader)
            data = []
            for row in reader:
                data.append(row)
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
        pathCSV = options["pathCSV"][0]
        pathStr, filename = os.path.split(pathCSV)

        self.targetFolder = options["targetFolder"][0]

        header, data = self.readCSV(pathCSV)
        for row in data:

            if "modulzuordnung" in filename:
                self.addOrUpdateRowSubproject(row, header, 'modul')
            elif "enargus" in filename:
                self.addOrUpdateRowSubproject(row, header, 'enargus')
            elif "Tools" in filename:
                self.getOrCreateTools(row, header)
            elif "schlagwoerter" in filename:
                print(row[header.index('Förderkennzeichen (0010)')])
                self.addOrUpdateRowSubproject(row, header, 'schlagwortregister')
            elif "weatherdata" in filename:
                print(row[header.index('data_service')])
                self.getOrCreateWeatherdata(row, header)
            else:
                print(f"Cant detect type of data. Please add 'modulzuordnung', \
                    'enargus', 'Tools' or 'weatherdata' to Filename to make \
                    detection possible."
                )
                return None
    
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
        parser.add_argument('pathCSV', nargs='+', type=str) 
        parser.add_argument("targetFolder", nargs="+", type=str)