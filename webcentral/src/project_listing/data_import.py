"""App specific dataImport class for the app `prject_listing`

"""
from common.data_import import DataImport
from .models import (
    Address,
    Enargus,
    ExecutingEntity,
    FurtherFundingInformation,
    GrantRecipient,
    RAndDPlanningCategory,
    Subproject,
    Person,
)


class DataImportApp(DataImport):
    """Class definition of App specific data import class `DataImportApp`.
    Inherits from general data import class `DataImport`.

    """
    DJANGO_APP = "project_listing"
    DJANGO_MODEL = "Subproject"
    MAPPING_EXCEL_DB_EN = {
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
        self.dictIdentifier = None


    def getOrCreate(self, row: list, header: list, data: list) -> None:
        """
        Add entry Subproject into the table or/and return entry key.
        """

        # get the subproject for the enargus dataset:

        self.dictIdentifier = row[header.index("FKZ")]
        subprojectObj, created = self.getOrCreateSubproject(header, row)

        enargusObj = None
        if created is False:
            enargusObj = subprojectObj.enargusData
            self.diffStrDict[subprojectObj.referenceNumber_id] = ""

        objGrantRecipient, _ = self.getOrCreateGrantRecipient(
            row, header, getattr(enargusObj, "objGrantRecipient", None)
        )
        objExecEntity, _ = self.getOrCreateExecutingEntity(
            row, header, getattr(enargusObj, "executingEntity", None)
        )
        objRAndDPlanning, _ = self.getOrCreateRAndDPlanningCategory(
            row, header, getattr(enargusObj, "rAndDPlanningCategory", None)
        )
        objPerson, _ = self.getOrCreatePerson(
            row, header, getattr(enargusObj, "projectLead", None)
        )
        objFurtherFunding, _ = self.getOrCreateFurtherFundingInformation(
            row, header, getattr(enargusObj, "furtherFundingInformation", None)
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

        subprojectObj.enargusData = obj
        subprojectObj.save()

        if enargusObj is not None:
            self._compareDjangoOrmObj(Enargus, enargusObj, obj)

        if (
            enargusObj is not None
            and self.diffStrDict[self.dictIdentifier] != ""
        ):
            self._writeDiffStrToDB()

        return obj, created

    def getOrCreateGrantRecipient(
        self,
        row: list,
        header: list,
        oldRecipientObj: GrantRecipient,
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
        oldAddressObj = None
        if oldRecipientObj is not None:
            oldAddressObj = oldRecipientObj.address

        objAnsZwe, _ = self.getOrCreateAdress(
            row,
            header,
            "zwe",
            oldAddressObj,
        )
        # doneeAdressId = objAnsZwe.anschrift_id

        # content = row[number of the columns of the row]
        nameFromCSV = row[header.index("Name_ZWE")]
        newGrantRecipientObj, created = GrantRecipient.objects.get_or_create(
            name=nameFromCSV,
            address=objAnsZwe,
        )

        if oldRecipientObj is not None:
            self._compareDjangoOrmObj(
                GrantRecipient, oldRecipientObj, newGrantRecipientObj
            )

        return newGrantRecipientObj, created

    def getOrCreateExecutingEntity(self, row, header, oldExecutingEntityObj):
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
        oldAddressObj = None
        if oldExecutingEntityObj is not None:
            oldAddressObj = oldExecutingEntityObj.address

        objAnsAs, _ = self.getOrCreateAdress(row, header, "as", oldAddressObj)

        nameFromCSV = row[header.index("Name_AS")]
        newExecutingEntityObj, created = ExecutingEntity.objects.get_or_create(
            name=nameFromCSV,
            address=objAnsAs,
        )

        if oldExecutingEntityObj is not None:
            self._compareDjangoOrmObj(
                ExecutingEntity, oldExecutingEntityObj, newExecutingEntityObj
            )

        return newExecutingEntityObj, created

    def getOrCreateSubproject(self, header, row):
        """Get the `Subproject` ORM-object for a `referernceNumberId`.

        """
        referernceNumberId = row[header.index("FKZ")]
        obj, created = Subproject.objects.get_or_create(
            referenceNumber_id=referernceNumberId,
        )

        return obj, created

    def getOrCreateRAndDPlanningCategory(
        self,
        row: list,
        header: list,
        oldRandDobj,
    ) -> tuple:
        """Gets or Creates an object of type RAndDPlanningCategory from the 
        data in row.

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

        if oldRandDobj is not None:
            self._compareDjangoOrmObj(RAndDPlanningCategory, oldRandDobj, obj)

        return obj, created

    def getOrCreatePerson(
        self,
        row: list,
        header: list,
        oldPersonObj: Person,
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
        if oldPersonObj is not None:
            self._compareDjangoOrmObj(Person, oldPersonObj, obj)

        return obj, created

    def getOrCreateFurtherFundingInformation(
        self,
        row: list,
        header: list,
        oldFundingObj: FurtherFundingInformation,
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
            FurtherFundingInformation-object, represent the created or in 
            database present FurtherFundingInformation-Dataset with the data 
            from row.
        created:    bool
            Indicates, if the FurtherFundingInformation-object was created or 
            not.
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

        if oldFundingObj is not None:
            self._compareDjangoOrmObj(
                FurtherFundingInformation, oldFundingObj, obj
            )

        return obj, created

    def getOrCreateAdress(
        self,
        row: list,
        header: list,
        who: str,
        oldObj: Address,
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
        else:
            postalCode = ""
            location = ""
            country = ""
            adress = ""

        obj, created = Address.objects.get_or_create(
            plz=postalCode,
            location=location,
            state=country,
            address=adress,
        )

        if oldObj is not None:
            self._compareDjangoOrmObj(Address, oldObj, obj)

        return obj, created
