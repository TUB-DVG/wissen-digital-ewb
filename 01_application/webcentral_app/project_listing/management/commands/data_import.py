"""This Module should serve as an 
update for the `data_import.py` file. 
It uses the .csv import-functionality. 

"""

import csv
import pdb
from encodings import utf_8
import os
import datetime

from django.core.management.base import BaseCommand
import numpy as np

from project_listing.models import *
from tools_over.models import *
from weatherdata_over.models import *
from schlagwoerter.models import *
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
    they hold. (TODO: This has to be changed)

    enargus-data needs to have "enargus" in its filename.
    modulzurodnung-data needs to have "modul" in its filename.
    wheaterdata needs to have "wheaterdata" in its filename.
    schlagwoerter-data needs to have "schlagwoerter" in its filename.
    """

    def __init__(self):
        """
        
        """        
        currentTimestamp = datetime.datetime.now()
        #pdb.set_trace()
        self.DBdifferenceFileName = str(int(currentTimestamp.timestamp())) + ".yaml"
        # self.DBdifferenceFileName = (str(currentTimestamp.date()) 
        #     + str(currentTimestamp.time().hour) 
        #     + str(currentTimestamp.time().minute) 
        #     + str(currentTimestamp.time().second) 
        #     + ".yaml")
        self.fkzWrittenToYAML = []



    def getOrCreateForschung(self, row, header):
        """
        add entry into table forschung or/and return entry key
        """
        # content = row[number of the columns of the row]
        federalMinistry = row[header.index('Bundesministerium')]
        projectBody = row[header.index('Projekttraeger')]
        supportProgram = row[header.index('Foerderprogramm')]
        researchProgram = row[header.index('Forschungsprogramm')]
        obj, created = Forschung.objects.get_or_create(
            bundesministerium=federalMinistry,
            projekttraeger=projectBody,
            forschungsprogramm=researchProgram,
            foerderprogramm=supportProgram,
        )
        return obj, created

    def getOrCreateAnschrift(self, row, header, who):
        """
        add entry into table anschrift or/and return entry key

        who options:
        - 'zwe' : zuwendungsempfaenger
        - 'as' : ausfehrende Stelle
        """
        # content = row[number of the columns of the row]
        # decision kind of persion, where should the data read from, 
        # maybe later needed
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

        obj, created = Anschrift.objects.get_or_create(
            plz = postalCode,
            ort = location,
            land = country,
            adresse = adress,
        )
        return obj, created

    def getOrCreatePerson(self, row, header):
        """
        add entry into table person or/and return entry key
        """
        # content = row[number of the columns of the row]
        # decision kind of persion, where should the data read from, 
        # maybe later needed
        name = row[header.index('Name_pl')]
        surname = row[header.index('Vorname_pl')]
        titel = row[header.index('Titel_pl')]
        email = row[header.index('Email_pl')]
        obj, created = Person.objects.get_or_create(
            name = name,
            vorname = surname,
            titel = titel,
            email = email,
        )
        return obj, created

    def getOrCreateLeistungSys(self, row, header):
        """
        add entry into table leistung_sys or/and return entry key
        """
        # content = row[number of the columns of the row]
        benefitPlanSystematicText = row[header.index('Leistungsplan_Sys_Text')]
        benefitPlanSystematicNr = row[header.index('Leistungsplan_Sys_Nr')]

        obj, created = Leistung_sys.objects.get_or_create(
            leistungsplansystematik_nr =  benefitPlanSystematicNr,
            leistungsplansystematik_text = benefitPlanSystematicText
        )
        return obj, created

    def getOrCreateZuwendungsempfaenger(self, row, header):
        """
        add entry into table zuwendungsempfaenger or/and return entry key
        """
    # fill table anschrift in case of zuwendungsempfaenger
        # or/and get the anschrift_id
        objAnsZwe, _ = self.getOrCreateAnschrift(
            row, 
            header, 
            'zwe',
        )
        doneeAdressId = objAnsZwe.anschrift_id

        # content = row[number of the columns of the row]
        name = row[header.index('Name_ZWE')]
        obj, created = Zuwendungsempfaenger.objects.get_or_create(
            name = name,
            anschrift_id = doneeAdressId,
        )
        return obj, created

    def getOrCreateAusfuehrendeStelle(self, row, header):
        """
        add entry into table ausfuehrende_stelle or/and return entry key
        """
    # fill table anschrift in case of ausfuehrende_stelle
        # or/and get the anschrift_id
        objAnsAs, _ = self.getOrCreateAnschrift(row, header, 'as')
        addressId = objAnsAs.anschrift_id

        # content = row[number of the columns of the row]
        name = row[header.index('Name_AS')]
        obj, created = Ausfuehrende_stelle.objects.get_or_create(
            name = name,
            anschrift_id = addressId,
        )
        return obj, created

    def getOrCreateEnargus(self, row, header):
        """
        add entry into table enargus or/and return entry key
        """
        # content = row[number of the columns of the row]
        # print(forschung_id)

        # fill table zuwendungsempfaenger or/and get the zuwendungsempfaenger_id
        objZwe, _ = self.getOrCreateZuwendungsempfaenger(row, header)
        zwe_id = objZwe.zuwendungsempfaenger_id

        # fill table ausfuehrende_stelle or/and get the ausfuehrende_stelle_id
        objAs, _ = self.getOrCreateAusfuehrendeStelle(row, header)
        asId = objAs.ausfuehrende_stelle_id

        # fill table leistung_sys or/and get the leistungsplansystematik_nr
        objLps, _ = self.getOrCreateLeistungSys(row, header)
        lpsNr = objLps.leistungsplansystematik_nr

        # fill table person or/and get the person_id
        objPer, _ = self.getOrCreatePerson(row, header)
        personId = objPer.person_id

        # fill table forschung or/and get the forschung_id
        objFor, _ = self.getOrCreateForschung(row, header)
        forschungId = objFor.forschung_id

        durationBegin = row[header.index('Laufzeitbeginn')]
        durationEnd = row[header.index('Laufzeitende')]
        theme = row[header.index('Thema')]
        clusterName = row[header.index('Verbundbezeichung')]
        fundingSum = float(row[header.index('Foerdersumme_EUR')])
        shortDescriptionDe = row[header.index('Kurzbeschreibung_de')]
        shortDescriptionEn = row[header.index('Kurzbeschreibung_en')]
        database = row[header.index('Datenbank')]
        obj, created = Enargus.objects.get_or_create(
            laufzeitbeginn=durationBegin,
            laufzeitende=durationEnd,
            thema=theme,
            # instead of using only the name of the feature in case
            # of foreigne keys use the name+_id, I dont know why
            projektleiter_id = personId,
            forschung_id = forschungId,
            leistungsplan_systematik_id = lpsNr,
            zuwendsempfanger_id = zwe_id,
            ausfuehrende_stelle_id = asId,
            verbundbezeichnung = clusterName,
            foerdersumme = fundingSum,
            kurzbeschreibung_de = shortDescriptionDe,
            kurzbeschreibung_en = shortDescriptionEn,
            datenbank = database,
        )
        return obj, created

    def getOrCreateModulenZuordnung(self, row, header) -> tuple:
        """
        add entry into table modulen_zuordnung_ptj or/and return entry key
        """
        # content = row[number of the columns of the row]

        priority1 = row[header.index('modulzuordnung_ptj_1')]
        priority2 = row[header.index('modulzuordnung_ptj_2')]
        priority3 = row[header.index('modulzuordnung_ptj_3')]
        priority4 = row[header.index('modulzuordnung_ptj_4')]
        obj, created = Modulen_zuordnung_ptj.objects.get_or_create(
            priority_1 = priority1,
            priority_2 = priority2,
            priority_3 = priority3,
            priority_4 = priority4
        )
        return obj, created

    def getOrCreateTools(self, row, header) -> tuple:
        """
        add entry into table Tools or/and return entry key
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
            bezeichnung = description,
            kurzbeschreibung = shortDesciption,
            anwendungsbereich = applicationArea,
            kategorie = category,
            lebenszyklusphase = lifeCyclePhase,
            nutzerschnittstelle = userInterface,
            zielgruppe = targetGroup,
            letztes_update = lastUpdate,
            lizenz = license,
            weitere_informationen = furtherInfos,
            alternativen = alternatives,
            konk_anwendung = concreteApplication,
        )
        return obj, created

    def getOrCreateWeatherdata(self, row, header) -> tuple:
        """
        add entry into table Weatherdata or/and return entry key
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

    def getOrCreateSchlagwort(self, row, header, schlagwortKey) -> tuple:
        """
        add entry into table schlagwort or/and return entry key
        """
        # content = row[number of the columns of the row]
        schlagwort = row[header.index(schlagwortKey)]
        obj, created = Schlagwort.objects.get_or_create(
            schlagwort = schlagwort
        )
        return obj, created

    def getOrCreateSchlagwortregister(self, row, header) -> tuple:
        """
        add entry into table Weatherdata or/and return entry key
        """
        
        objSchlagwort1, _ = self.getOrCreateSchlagwort(
            row, 
            header, 
            'Schlagwort1',
        )
        schlagwort1Id = objSchlagwort1.schlagwort_id

        objSchlagwort2, _ = self.getOrCreateSchlagwort(
            row, 
            header, 
            'Schlagwort2',
        )
        schlagwort2Id = objSchlagwort2.schlagwort_id

        objSchlagwort3, _ = self.getOrCreateSchlagwort(
            row, 
            header, 
            'Schlagwort3',
        )
        schlagwort3Id = objSchlagwort3.schlagwort_id

        objSchlagwort4, _ = self.getOrCreateSchlagwort(
            row, 
            header, 
            'Schlagwort4',
        )
        schlagwort4Id = objSchlagwort4.schlagwort_id
        
        objSchlagwort5, _ = self.getOrCreateSchlagwort(
            row, 
            header, 
            'Schlagwort5',
        )
        schlagwort5Id = objSchlagwort5.schlagwort_id
        
        objSchlagwort6, _ = self.getOrCreateSchlagwort(
            row, 
            header, 
            'Schlagwort6',
        )
        schlagwort6Id = objSchlagwort6.schlagwort_id
        
        objSchlagwort7, _ = self.getOrCreateSchlagwort(
            row, 
            header, 
            'Schlagwort',
        )
        schlagwort7Id = objSchlagwort7.schlagwort_id
        

        obj, created = Schlagwortregister_erstsichtung.objects.get_or_create(
            schlagwort_1_id = schlagwort1Id,
            schlagwort_2_id = schlagwort2Id,
            schlagwort_3_id = schlagwort3Id,
            schlagwort_4_id = schlagwort4Id,
            schlagwort_5_id = schlagwort5Id,
            schlagwort_6_id = schlagwort6Id,
            schlagwort_7_id = schlagwort7Id,
        )
        return obj, created

    def addOrUpdateRowTeilprojekt(self, row, header, source) -> tuple:
        """add or update one row of the database, but without foreign key 
        connections

        source cases:
        - 'enargus' : read data from enargus xml via csv file 
        (here csv will loaded)
        - 'modul' : read data from 'verteiler xlsx' via csv file 
        (here csv will loaded)

        """
        # fill table enargus or/and get the enargus_id
        if source == 'enargus':
            obj, created = self.getOrCreateEnargus(row, header)
            enargus_id = obj.enargus_id
            fkz = row[header.index('FKZ')]            
            try:
                if len(Teilprojekt.objects.filter(
                    fkz=fkz, 
                    enargus_daten_id=enargus_id
                )) == 0:
                    Teilprojekt.objects.create(fkz=fkz,
                                            enargus_daten_id= enargus_id)
                    print('added: %s' %fkz)
            except IntegrityError:
                currentStateTable = Teilprojekt.objects.filter(fkz=fkz)[0].\
                    enargus_daten
                unvisited = []
                visitedNames = []
                visitedNames.append("teilprojekt")
                unvisited.append([
                    "Enargus", 
                    currentStateTable, 
                    obj, 
                    "Teilprojekt",
                ])

                self.compareForeignTables(
                    unvisited, 
                    visitedNames, 
                    {"fkz": fkz}, 
                    currentStateTable.verbundbezeichnung,
                )

        elif source == 'modul':
            obj, created = self.getOrCreateModulenZuordnung(row, header)
            modId = obj.mod_id
            fkz = row[header.index('FKZ')].strip()
            try:
                if len(Teilprojekt.objects.filter(
                    fkz=fkz, 
                    zuordnung_id=modId
                )) == 0:
                    Teilprojekt.objects.create(
                        fkz=fkz,
                        zuordnung_id= modId
                    )
                    print('added: %s' %fkz)
            except IntegrityError:
                enargusDaten = Teilprojekt.objects.filter(fkz=fkz)[0].enargus_daten
                zuordnungObj = Teilprojekt.objects.filter(fkz=fkz)[0].zuordnung
                unvisited = []
                visitedNames = []
                visitedNames.append("teilprojekt")
                unvisited.append([
                    "zuordnung", 
                    zuordnungObj, 
                    obj, 
                    "Teilprojekt",
                ])
                if enargusDaten is None:
                    verbundbezeichung = None
                else:
                    verbundbezeichung = enargusDaten.verbundbezeichnung
                self.compareForeignTables(
                    unvisited, 
                    visitedNames, 
                    {"fkz": fkz}, 
                    verbundbezeichung,
                )
        elif source == 'schlagwortregister':
            obj, _ = self.getOrCreateSchlagwortregister(row, header)
            tagRegisterId = obj.schlagwortregister_id
            fkz = row[header.index('Förderkennzeichen (0010)')]
            try:
                if len(Teilprojekt.objects.filter(
                    fkz=fkz, 
                    schlagwortregister_erstsichtung_id = tagRegisterId,
                )) == 0:
                    Teilprojekt.objects.create(
                        fkz=fkz,
                        schlagwortregister_erstsichtung_id = tagRegisterId,
                    )
                    print('added: %s' %fkz)
            except IntegrityError:
                currentPartEnargus = Teilprojekt.objects.filter(fkz=fkz)[0].enargus_daten
                currentObjTagRegisterFirstLook = Teilprojekt.objects.filter(
                    fkz=fkz,
                )[0].schlagwortregister_erstsichtung
                unvisited = []
                visitedNames = []
                visitedNames.append("teilprojekt")
                unvisited.append([
                    "schlagwortregister_erstsichtung", 
                    currentObjTagRegisterFirstLook, 
                    obj, 
                    "Teilprojekt",
                ])
                if currentPartEnargus is None:
                    verbundbezeichnung = None
                else:
                    verbundbezeichnung = currentPartEnargus.verbundbezeichnung
                self.compareForeignTables(
                    unvisited, 
                    visitedNames, 
                    {"fkz": fkz}, 
                    verbundbezeichnung,
                )
        
    def compareForeignTables(
            self, 
            unvisited: list, 
            visitedNames: list, 
            identifer: dict, 
            theme: str,
        ) -> None:
        """Starting from a Database-Conflict the method walks through 
        all foreign-tables and compares the values of the two conflicting 
        datasets. If the values are different for a attribute, they
        are saved inside an instance of the DatabaseDifference-class.
        
        At the moment the central table of the database is the 
        `Teilprojekt`-Table. New loaded Datasets can update values 
        of one Teilprojekt-Tuple, which is represented by a 
        `Förderkennzeichen`. If 

        unvisited:  list
            list of tables, which were not visited yet. As a first 
            entry it contains the name of the table, 
            where the datasets are located, which produce a database
            conflict. The second entry holds a object  
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

        currentDBDifferenceObj = DatabaseDifference(identifer, theme)
        while len(unvisited) > 0:
            #depth += 1
            
            currentEntryInUnvisited = unvisited.pop()
            
            currentForeignTableName = currentEntryInUnvisited[0]
            currentTableObj = currentEntryInUnvisited[1]
            pendingTableObj = currentEntryInUnvisited[2]
            parentTableName = currentEntryInUnvisited[3]
            visitedNames.append(f"{parentTableName}.{currentForeignTableName}")
            if currentTableObj is None:
                diffCurrentObjDict[currentForeignTableName] = "None"
                diffPendingObjDict[currentForeignTableName] = ""
                for columnName in pendingTableObj._meta.get_fields():
                    if not columnName.is_relation:
                       
                       diffPendingObjDict[currentForeignTableName] = (
                           diffPendingObjDict[currentForeignTableName] 
                           + "|" 
                           + f" {columnName.name}: {str(pendingTableObj.__getattribute__(columnName.name))}"
                        )
            else:
                listOfFieldsInCurrentTable = currentTableObj._meta.get_fields()
                
                if f"{parentTableName}.{currentForeignTableName}" not in diffCurrentObjDict.keys():
                    currentDBDifferenceObj.addTable(f"{parentTableName}.{currentForeignTableName}")
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
                                currentForeignTableName,
                            ])
                        except:
                            pass
                    elif not teilprojektField.is_relation:
                        try:
                            if (
                                str(pendingTableObj.__getattribute__(currentForeignTableStr)) 
                                != str(currentTableObj.__getattribute__(currentForeignTableStr))
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
                            
                                diffCurrentObjDict[f"{parentTableName}.{currentForeignTableName}"] = diffCurrentObjDict[f"{parentTableName}.{currentForeignTableName}"] + "|" + strCurrent
                                diffPendingObjDict[f"{parentTableName}.{currentForeignTableName}"] = diffPendingObjDict[f"{parentTableName}.{currentForeignTableName}"] + "|" + strPending
                                currentDBDifferenceObj.addDifference(
                                    f"{parentTableName}.{currentForeignTableName}", 
                                    {currentForeignTableStr: str(currentTableObj.__getattribute__(currentForeignTableStr))}, 
                                    {currentForeignTableStr: str(pendingTableObj.__getattribute__(currentForeignTableStr))},
                                )   
                        except:
                            pass
                
        currentDBDifferenceObj.writeToYAML(self.DBdifferenceFileName)


    def readCSV(self, path: str) -> tuple:
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

    def handle(self, *args, **options):
        """This method is called from the manage.py when the 'data_import'
        command is called together with the manage.py.
        
        """
        #pdb.set_trace()
        pathCSV=options["pathCSV"][0]
        pathStr, filename = os.path.split(pathCSV)

        header, data = self.readCSV(pathCSV)
        for row in data:

            if "modulzuordnung" in filename:
                self.addOrUpdateRowTeilprojekt(row, header, 'modul')
            elif "enargus" in filename:
                self.addOrUpdateRowTeilprojekt(row, header, 'enargus')
            elif "Tools" in filename:
                self.getOrCreateTools(row, header)
            elif "schlagwoerter" in filename:
                print(row[header.index('Förderkennzeichen (0010)')])
                self.addOrUpdateRowTeilprojekt(row, header, 'schlagwortregister')
            elif "weatherdata" in filename:
                print(row[header.index('data_service')])
                self.getOrCreateWeatherdata(row, header)
            else:
                print(f"Cant detect type of data. Please add 'modulzuordnung', \
                    'enargus', 'Tools' or 'weatherdata' to Filename to make \
                    detection possible."
                )
                return None
    
    def add_arguments(self, parser):
        """This method parses the arguments, which where given when 
        calling the data_import-command together with the manage.py.
        The Arguments are then given to the handle-method, and can
        be accessed as python-variables.

        Parameters:
        parser: django.parser
        Django parser object, which handles the parsing of the command
        and arguments.
        
        """
        parser.add_argument('pathCSV', nargs='+', type=str) 



# Script area (here you find examples to use the functions ahead)
#classObj = DataImport()
# ## Example add/update Enargus data
# path_csv_enargus='../../02_work_doc/01_daten/01_prePro/enargus_csv_20220902.csv'
# header, data = classObj.csv2m4db_enargus(path_csv_enargus)

# ## Example add/update Modul-Zuordnung data
# path_csv_modul='../../02_work_doc/01_daten/01_prePro/modulzuordnung_csv_20220829.csv'
# header, data = classObj.csv2m4db_modul(path_csv_modul)
# #pdb.set_trace()
# ## Example add/update Tool Uebersichts table
# path_csv_tools='../../02_work_doc/01_daten/02_toolUebersicht/2022_02_22_EWB_Tools_Uebersicht.csv'
# header, data = classObj.csv2m4db_tools(path_csv_tools)
# #pdb.set_trace()
# ## Example add/update Weatherdata table
# path_csv_weatherdata='../../02_work_doc/01_daten/03_weatherdata/2022_03_31_weatherdata.csv'
# header, data = classObj.csv2m4db_weatherdata(path_csv_weatherdata)
#pdb.set_trace()
## Example add/update Schlagwoerter table
# path_csv_schlagwoerter='../../02_work_doc/01_daten/04_schlagwoerter/ZE_fuer_BF_enargus_ergaenzt_Auswahl_rst_fc.csv'
# header, data = classObj.csv2m4db_schlagwortregister_erstsichtung(path_csv_schlagwoerter)
