from .models import *
from common.data_import import DataImport

class DataImportApp(DataImport):
    DJANGO_APP = "project_listing"
    DJANGO_MODEL = "Subproject"
    MAPPING_EXCEL_DB_EN = {
        # "ueberschrift__en": "heading_en",
        # "text__en": "text_en",
        # "tags__en": "tags_en",
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
    
    def getOrCreate(self, row: list, header: list, data: list) -> None:
        """
        Add entry Subproject into the table or/and return entry key.
        """
       
        # get the subproject for the enargus dataset:

        subprojectObj, created = self.getOrCreateSubproject(header, row)
        
        enargusObj = None
        if created == False:
            enargusObj = subprojectObj.enargus

        objGrantRecipient, _ = self.getOrCreateGrantRecipient(row, header, enargusObj)
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
            self._compareDjangoOrmObj(GrantRecipient, oldRecipientObj, newGrantRecipientObj)
        
        return newGrantRecipientObj, created


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

    def getOrCreateSubproject(self, header, row):
        """

        """
        referernceNumberId = row[header.index("FZK")]
        obj, created = Subproject.objects.get_or_create(
            referernceNumber_id=referernceNumberId,
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

        obj, created = Address.objects.get_or_create(
            plz=postalCode,
            location=location,
            state=country,
            address=adress,
        )
        
        if oldObj is not None:
            self._compareDjangoOrmObj(Address, oldObj, obj)

        return obj, created


