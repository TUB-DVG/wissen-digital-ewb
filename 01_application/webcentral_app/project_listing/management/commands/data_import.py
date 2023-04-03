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

class Command(BaseCommand):
    """
    
    """

    def __init__(self):
        """
        
        """

        self.dataToBeComparedEnargus = []
        self.dataToBeComparedModul = []
        self.dataToBeComparedSchlagwort = []
        
        currentTimestamp = datetime.datetime.now()
        self.DBdifferenceFileName = (str(currentTimestamp.date()) 
            + str(currentTimestamp.time().hour) 
            + str(currentTimestamp.time().minute) 
            + str(currentTimestamp.time().second) 
            + ".yaml")



    def getOrCreateForschung(self, row, header):
        """
        add entry into table forschung or/and return entry key
        """
        # content = row[number of the columns of the row]
        bundesministerium = row[header.index('Bundesministerium')]
        projekttraeger = row[header.index('Projekttraeger')]
        foerderprogramm = row[header.index('Foerderprogramm')]
        forschungsprogramm = row[header.index('Forschungsprogramm')]
        obj, created = Forschung.objects.get_or_create(
            bundesministerium=bundesministerium,
            projekttraeger=projekttraeger,
            forschungsprogramm=forschungsprogramm,
            foerderprogramm=foerderprogramm,
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
            plz = row[header.index('PLZ_ZWE')]
            ort = row[header.index('Ort_ZWE')]
            land = row[header.index('Land_ZWE')]
            adresse = row[header.index('Adress_ZWE')]
        elif who == 'as':
            plz = row[header.index('PLZ_AS')]
            ort = row[header.index('Ort_AS')]
            land = row[header.index('Land_AS')]
            adresse = row[header.index('Adress_AS')]

        obj, created = Anschrift.objects.get_or_create(
            plz = plz,
            ort = ort,
            land = land,
            adresse = adresse
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
        vorname = row[header.index('Vorname_pl')]
        titel = row[header.index('Titel_pl')]
        email = row[header.index('Email_pl')]
        obj, created = Person.objects.get_or_create(
            name = name,
            vorname = vorname,
            titel = titel,
            email = email,
        )
        return obj, created

    def getOrCreateLeistungSys(self, row, header):
        """
        add entry into table leistung_sys or/and return entry key
        """
        # content = row[number of the columns of the row]
        leistungsplansystematikText = row[header.index('Leistungsplan_Sys_Text')]
        leistungsplansystematikNr = row[header.index('Leistungsplan_Sys_Nr')]

        obj, created = Leistung_sys.objects.get_or_create(
            leistungsplansystematik_nr =  leistungsplansystematikNr,
            leistungsplansystematik_text = leistungsplansystematikText
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
        zweAnsId = objAnsZwe.anschrift_id

        # content = row[number of the columns of the row]
        name = row[header.index('Name_ZWE')]
        obj, created = Zuwendungsempfaenger.objects.get_or_create(
            name = name,
            anschrift_id = zweAnsId
        )
        return obj, created

    def getOrCreateAusfuehrendeStelle(self, row, header):
        """
        add entry into table ausfuehrende_stelle or/and return entry key
        """
    # fill table anschrift in case of ausfuehrende_stelle
        # or/and get the anschrift_id
        objAnsAs, _ = self.getOrCreateAnschrift(row, header, 'as')
        asNsId = objAnsAs.anschrift_id

        # content = row[number of the columns of the row]
        name = row[header.index('Name_AS')]
        obj, created = Ausfuehrende_stelle.objects.get_or_create(
            name = name,
            anschrift_id = asNsId
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
        objPer, createdPer = self.getOrCreatePerson(row, header)
        personId = objPer.person_id

        # fill table forschung or/and get the forschung_id
        objFor, _ = self.getOrCreateForschung(row, header)
        forschungId = objFor.forschung_id

        laufzeitbeginn = row[header.index('Laufzeitbeginn')]
        laufzeitende = row[header.index('Laufzeitende')]
        thema = row[header.index('Thema')]
        verbundbezeichnung = row[header.index('Verbundbezeichung')]
        foerdersumme = float(row[header.index('Foerdersumme_EUR')])
        kurzbeschreibung_de = row[header.index('Kurzbeschreibung_de')]
        kurzbeschreibung_en = row[header.index('Kurzbeschreibung_en')]
        datenbank = row[header.index('Datenbank')]
        obj, created = Enargus.objects.get_or_create(
            laufzeitbeginn=laufzeitbeginn,
            laufzeitende=laufzeitende,
            thema=thema,
            # instead of using only the name of the feature in case
            # of foreigne keys use the name+_id, I dont know why
            projektleiter_id = personId,
            forschung_id = forschungId,
            leistungsplan_systematik_id = lpsNr,
            zuwendsempfanger_id = zwe_id,
            ausfuehrende_stelle_id = asId,
            verbundbezeichnung = verbundbezeichnung,
            foerdersumme = foerdersumme,
            kurzbeschreibung_de = kurzbeschreibung_de,
            kurzbeschreibung_en = kurzbeschreibung_en,
            datenbank = datenbank,
        )
        return obj, created

    def getOrCreateModulenZuordnung(self, row, header):
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

    def getOrCreateTools(self, row, header):
        """
        add entry into table Tools or/and return entry key
        """
        # content = row[number of the columns of the row]

        bezeichung = row[header.index('Tool')]
        kurzbe = row[header.index('Kurzbeschreibung')]
        anwendBereich = row[header.index('Anwendungsbereich')]
        kategorie = row[header.index('Kategorie')]
        lebenszy = row[header.index('Lebenszyklusphase')]
        nutzersch = row[header.index('Nutzerschnittstelle')]
        zielgruppe = row[header.index('Zielgruppe')]
        lastUpdate= row[header.index('letztes Update')]
        license = row[header.index('Lizenz')]
        weitereInfos = row[header.index('weitere Informationen')]
        alternativen = row[header.index('Alternativen')]
        konkAnwEwb = row[header.index('konkrete Anwendung in EWB Projekten')]
        nutzerbewertung = row[header.index('Nutzerbewertungen')]


        obj, created = Tools.objects.get_or_create(
            bezeichnung = bezeichung,
            kurzbeschreibung = kurzbe,
            anwendungsbereich = anwendBereich,
            kategorie = kategorie,
            lebenszyklusphase = lebenszy,
            nutzerschnittstelle = nutzersch,
            zielgruppe = zielgruppe,
            letztes_update = letztesUpdate,
            lizenz = license,
            weitere_informationen = weitereInfos,
            alternativen = alternativen,
            konk_anwendung = konkAnwEwb,
            # nutzerbewertungen = nutzerbewertung
        )
        return obj, created

    def getOrCreateWeatherdata(self, row, header):
        """
        add entry into table Weatherdata or/and return entry key
        """
        # content = row[number of the columns of the row]

        dataService = row[header.index('data_service')]
        shortDescription = row[header.index('short_description')]
        provider = row[header.index('provider')]
        furtherInfos = row[header.index('further_information')]
        dataUrl = row[header.index('data_url')]
        logoUrl = row[header.index('logo_url')]
        applications = row[header.index('applications')]
        lastUpdate= row[header.index('last_update')]
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

    def getOrCreateSchlagwort(self, row, header, schlagwortKey):
        """
        add entry into table schlagwort or/and return entry key
        """
        # content = row[number of the columns of the row]
        schlagwort = row[header.index(schlagwortKey)]
        obj, created = Schlagwort.objects.get_or_create(
            schlagwort = schlagwort
        )
        return obj, created

    def getOrCreateSchlagwortregister(self, row, header):
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

    def addOrUpdateRowTeilprojekt(self, row, header, source):
        """add or update one row of the database, but without foreign key 
        connections

        source cases:
        - 'enargus' : read data from enargus xml via csv file (here csv will loaded)
        - 'modul' : read data from 'verteiler xlsx' via csv file (here csv will loaded)

        """
        # fill table enargus or/and get the enargus_id
        if source == 'enargus':
            obj, created = self.get_or_create_enargus(row, header)
            enargus_id = obj.enargus_id
            fkz = row[header.index('FKZ')]

        # breakpoint()
            
            try:
                if len(Teilprojekt.objects.filter(fkz=fkz, enargus_daten_id= enargus_id)) == 0:
                    Teilprojekt.objects.create(fkz=fkz,
                                            enargus_daten_id= enargus_id)
                    print('added: %s' %fkz)
            except IntegrityError:
                currentStateTable = Teilprojekt.objects.filter(fkz=fkz)[0].enargus_daten
                unvisited = []
                visitedNames = []
                visitedNames.append("teilprojekt")
                unvisited.append(["Enargus", currentStateTable, obj, "Teilprojekt"])

                self.compareForeignTables(unvisited, visitedNames, {"fkz": fkz}, currentStateTable.thema)

        elif source == 'modul':
            obj, created = self.get_or_create_modulen_zuordnung(row, header)
            mod_id = obj.mod_id
            fkz = row[header.index('FKZ')].strip()
            try:
                if len(Teilprojekt.objects.filter(fkz=fkz, zuordnung_id=mod_id)) == 0:
                    Teilprojekt.objects.create(fkz=fkz,
                                            zuordnung_id= mod_id)
                    print('added: %s' %fkz)
            except IntegrityError:
                
                currentTeilprojektObj = Teilprojekt.objects.filter(fkz=fkz)[0].zuordnung
                unvisited = []
                visitedNames = []
                visitedNames.append("teilprojekt")
                unvisited.append(["zuordnung", currentTeilprojektObj, obj, "Teilprojekt"])
                self.compareForeignTables(unvisited, visitedNames, {"fkz": fkz}, currentTeilprojektObj.thema)
        elif source == 'schlagwortregister':
            obj, created = self.get_or_create_schlagwortregister(row, header)
            schlagwortregister_id = obj.schlagwortregister_id
            fkz = row[header.index('Förderkennzeichen (0010)')]
            try:
                if len(Teilprojekt.objects.filter(fkz=fkz, schlagwortregister_erstsichtung_id = schlagwortregister_id)) == 0:
                    Teilprojekt.objects.create(fkz=fkz,
                                            schlagwortregister_erstsichtung_id = schlagwortregister_id)
                    print('added: %s' %fkz)
            except IntegrityError:
                currentObjSchlagwortregisterErstsichtung = Teilprojekt.objects.filter(fkz=fkz)[0].schlagwortregister_erstsichtung
                unvisited = []
                visitedNames = []
                visitedNames.append("teilprojekt")
                unvisited.append(["schlagwortregister_erstsichtung", currentObjSchlagwortregisterErstsichtung, obj, "Teilprojekt"])
                self.compareForeignTables(unvisited, visitedNames, {"fkz": fkz}, currentObjSchlagwortregisterErstsichtung.thema)
        
    def compareForeignTables(self, unvisited: list, visitedNames: list, identifer: dict, theme: str):
        """
        
        """
        visited = []
        
        diffCurrentObjDict = {}
        diffPendingObjDict = {}
        # with open(self.DBdifferenceFileName, 'a') as stream:
        #     yaml.dump(f"Conflict found for: {identifer}", stream)

        # with open("hallo.csv", "a") as f:
        #     f.write(f"Conflict found for: {identifer}\n")

        currentDBDifferenceObj = DatabaseDifference(identifer, theme)
        while len(unvisited) > 0:
            #depth += 1
            
            currentEntryInUnvisited = unvisited.pop()
            
            currentForeignTableName = currentEntryInUnvisited[0]
            currentTableObj = currentEntryInUnvisited[1]
            pendingTableObj = currentEntryInUnvisited[2]
            parentTableName = currentEntryInUnvisited[3]
            #currentObj.__getattribute__(currentForeignTableName)
            # if parentName != None:
            #     treeOfTablesCurrent.create_node(currentForeignTableName, currentForeignTableName, parent=parentName, data=currentObj.__getattribute__(currentForeignTableName))
            #     treeOfTablesPending.create_node(currentForeignTableName, currentForeignTableName, data=obj) 
            # else:
            #     treeOfTablesCurrent.create_node(unvisited[0], unvisited[0], data=currentObj.__getattribute__(unvisited[0]))
            #     treeOfTablesPending.create_node(unvisited[0], unvisited[0], data=obj)
            
            #visited.append(f"{parentTableName}.{currentEntryInUnvisited}")
            # if currentForeignTableName != "anschrift":
            visitedNames.append(f"{parentTableName}.{currentForeignTableName}")
            #currentTableObj = treeOfTablesCurrent.get_node(currentForeignTableName).data
            if currentTableObj is None:
                diffCurrentObjDict[currentForeignTableName] = "None"
                diffPendingObjDict[currentForeignTableName] = ""
                for columnName in pendingTableObj._meta.get_fields():
                    if not columnName.is_relation:
                       
                       diffPendingObjDict[currentForeignTableName] = diffPendingObjDict[currentForeignTableName] + "|" + f" {columnName.name}: {str(pendingTableObj.__getattribute__(columnName.name))}"
            else:
                listOfFieldsInCurrentTable = currentTableObj._meta.get_fields()
                
                if f"{parentTableName}.{currentForeignTableName}" not in diffCurrentObjDict.keys():
                    # new code fragment
                    currentDBDifferenceObj.addTable(f"{parentTableName}.{currentForeignTableName}")
                    # end of new code fragment
                    diffCurrentObjDict[f"{parentTableName}.{currentForeignTableName}"] = ""
                    diffPendingObjDict[f"{parentTableName}.{currentForeignTableName}"] = ""

                for teilprojektField in listOfFieldsInCurrentTable:
                    currentForeignTableStr = teilprojektField.__str__().strip(">").split(".")[-1]
                    if teilprojektField.is_relation and f"{parentTableName}.{currentForeignTableStr}" not in visitedNames and not teilprojektField.one_to_many:
                        #pdb.set_trace()
                        try:
                            #pdb.set_trace()
                            #parentTableName = currentTableObj.__doc__.split("(")[0]
                            unvisited.append([currentForeignTableStr, currentTableObj.__getattribute__(currentForeignTableStr), pendingTableObj.__getattribute__(currentForeignTableStr), currentForeignTableName])
                        except:
                            pass
                    elif not teilprojektField.is_relation:
                        #pdb.set_trace()
                        #currentForeignTableStr = teilprojektField.__str__().strip(">").split(".")[-1]
                        try:
                            #pdb.set_trace()
                            if str(pendingTableObj.__getattribute__(currentForeignTableStr)) != str(currentTableObj.__getattribute__(currentForeignTableStr)):
                                #pdb.set_trace()
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
                                # new code fragment
                                currentDBDifferenceObj.addDifference(f"{parentTableName}.{currentForeignTableName}", {currentForeignTableStr: str(currentTableObj.__getattribute__(currentForeignTableStr))}, {currentForeignTableStr: str(pendingTableObj.__getattribute__(currentForeignTableStr))})   
                                # end of new codefragment         
                        except:
                            pass
                
                # if diffCurrentObjDict[f"{parentTableName}.{currentForeignTableName}"] == "":
                #     diffCurrentObjDict.pop(f"{parentTableName}.{currentForeignTableName}")
                #     diffPendingObjDict.pop(f"{parentTableName}.{currentForeignTableName}")


        # with open("hallo.csv", "a") as f:
        #     for numberOfWrittenTableDiffs, currentTableEntry in enumerate(diffCurrentObjDict.keys()):
        #             f.write(f"  {currentTableEntry}\n")
        #             f.write(f"      {diffCurrentObjDict[currentTableEntry]}\n")
        #             f.write(f"      {diffPendingObjDict[currentTableEntry]}\n")
        #     f.write(f"Current: 10\n")
        #     f.write(f"Pending: 10\n")
        
        currentDBDifferenceObj.writeToYAML(self.DBdifferenceFileName)
        # with open(self.DBdifferenceFileName, 'a') as stream:
        #     yaml.dump(currentDBDifferenceObj, stream)


    def _getNonRelatingFields(self, currentDatasetInForeignTable):
        """
        
        """
        listOfNonrelationalFields = []
        for currentField in currentDatasetInForeignTable._meta.get_fields():
            if not currentField.is_relational:
                listOfNonrelationalFields.append(currentField)

        return listOfNonrelationalFields



    def _checkDifference(self, currentDatasetInForeignTable, pendingDatasetInForeignTable):
        """
        
        """
        nameOfCurrentTable = currentDatasetInForeignTable.__str__().split(".")[1]

        nonRelationalFields = self._getNonRelatingFields(currentDatasetInForeignTable)
        dictOfCurrentState = {}
        dictOfPendingState = {}

        dictOfCurrentState[nameOfCurrentTable] = {}
        dictOfPendingState[nameOfCurrentTable] = {}

        for field in nonRelationalFields:
            if currentDatasetInForeignTable.__getattribute__(field) != pendingDatasetInForeignTable.__getattribute__(field):
                dictOfCurrentState[field] = currentDatasetInForeignTable.__getattribute__(field)
                dictOfPendingState[field] = pendingDatasetInForeignTable.__getattribute__(field)
        
        return dictOfCurrentState, dictOfPendingState

    def csv2m4db_enargus(self, path):
        """EnArgus csv-file into BF M4 Django database, hard coded"""
        with open(path) as csv_file:
            reader = csv.reader(csv_file, delimiter=';')
            header = next(reader)
            data = []
            for row in reader:
                data.append(row)
                self.add_or_update_row_teilprojekt(row, header, 'enargus')
        return header, data

    def csv2m4db_modul(self, path):
        """Modul csv-file into BF M4 Django database, hard coded"""
        with open(path) as csv_file:
            reader = csv.reader(csv_file, delimiter=';')
            header = next(reader)
            data = []
            for row in reader:
                # print(row[header.index('FKZ')])
                data.append(row)
                self.add_or_update_row_teilprojekt(row, header, 'modul')
        return header, data

    def read_print_csv(self, path):
        """Test function EnArgus csv-file into BF M4 Django database, hard coded"""
        with open(path) as csv_file:
            reader = csv.reader(csv_file, delimiter=';')
            header = next(reader)
            data = []
            for row in reader:
                data.append(row)
                # print(row[header.index('FKZ')])
        return header, data

    def csv2m4db_tools(self, path):
        """tools Uebersicht csv-file into BF M4 Django database, hard coded"""
        with open(path, encoding='utf-8') as csv_file:
            reader = csv.reader(csv_file, delimiter=';')
            header = next(reader)
            data = []
            for row in reader:
                print(row[header.index('Tool')])
                data.append(row)
                # breakpoint()
                self.get_or_create_tools(row, header)
        return header, data

    def csv2m4db_weatherdata(self, path):
        """Weatherdata csv-file into BF M4 Django database, hard coded"""
        with open(path, encoding='utf-8') as csv_file:
            reader = csv.reader(csv_file, delimiter=';')
            header = next(reader)
            data = []
            for row in reader:
                print(row[header.index('data_service')])
                data.append(row)
                # breakpoint()
                self.get_or_create_weatherdata(row, header)
        return header, data


    def csv2m4db_schlagwortregister_erstsichtung(self, path):
        """Weatherdata csv-file into BF M4 Django database, hard coded"""
        with open(path, encoding='utf-8') as csv_file:
            reader = csv.reader(csv_file, delimiter=';')
            header = next(reader)
            data = []
            for row in reader:
                print(row[header.index('Förderkennzeichen (0010)')])
                data.append(row)
                # breakpoint()
                # get_or_create_schlagwortregister(row, header)
                self.add_or_update_row_teilprojekt(row, header, 'schlagwortregister')
        return header, data
    
    def handle(self, *args, **options):
        """
        
        """
        #pdb.set_trace()
        pathCSV=options["pathCSV"][0]
        pathStr, filename = os.path.split(pathCSV)
        if "modulzuordnung" in filename:
            header, data = self.csv2m4db_modul(pathCSV)
        elif "enargus" in filename:
            header, data = self.csv2m4db_enargus(pathCSV)
        elif "Tools" in filename:
            header, data = self.csv2m4db_tools(pathCSV)
        elif "schlagwoerter" in filename:
            header, data = self.csv2m4db_schlagwortregister_erstsichtung(pathCSV)
        elif "weatherdata" in filename:
            header, data = self.csv2m4db_weatherdata(pathCSV)
        else:
            print(f"Cant detect type of data. Please add 'modulzuordnung', 'enargus', 'Tools' or 'weatherdata' to Filename to make detection possible.")
    
    def add_arguments(self, parser):
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
