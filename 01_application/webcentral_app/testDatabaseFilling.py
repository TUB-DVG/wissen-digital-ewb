"""

"""
import datetime
import importlib
import time
import os
import pdb



from django.test import TransactionTestCase
from django.core import management
from django.db.utils import IntegrityError
import yaml

from project_listing.models import (
    Teilprojekt,
    Schlagwortregister_erstsichtung,
)
from project_listing.management.commands.data_import import (
    Command, 
    MultipleFKZDatasets,
)

class checkDifferencesInDatabase(TransactionTestCase):
    """Testing of `data_import.py` and `execute_db_changes.py` 
    
    This class holds different Testcases and helper-methods.
    The testcases aim to test the data_import in the database and the 
    handling of dataset-conflicts. A dataset conflict is present,
    when for one Förderkennzeichen (fkz) two different datasets are 
    present in the database. This can happen, when a dataset in the
    database with a specific fkz (hereafter current/currentState) is
    updated by a dataset with the same fkz, but with at least one
    difference in the rows (hereafter pendingState or CSV-State).
    On an apparance of such a Conflict the `data_import.py` creates 
    an .yaml-file in which the conflicts are shown. The user then 
    needs to decide, which state should be kept, and which discarded.
    """

    def testLoadingTwoTimesTheSameDataset(self):
        """This method tests what happens, if 2 times the same dataset 
        is loaded into the DB. It loads the .csv file at 
        "testData/enargus_testDatabaseFile.csv" two times in a row,
        and checks each time if only one dataset is present in the 
        datasbe and that its the one, represented by the first dataset
        inside the .csv-file.
        
        """

        fileNameContainingTestData = "testData/enargus_testDatabaseFile.csv"

        dataImportCommand = Command()
        header, data = dataImportCommand.readCSV(fileNameContainingTestData)

        management.call_command('data_import', fileNameContainingTestData)

        # only one Teilprojekt should be present in the test-database:
        self.assertTrue(len(Teilprojekt.objects.all()) == 1)
        
        # check if the dataset was corretly loaded into the DB:
        testDatasetFromDB = Teilprojekt.objects.filter(fkz=data[0][0])[0]

        testDatasetEnargus = testDatasetFromDB.enargus_daten

        self.assertTrue(str(testDatasetEnargus.laufzeitbeginn) == data[0][1])
        self.assertTrue(str(testDatasetEnargus.laufzeitende) == data[0][2])
        self.assertTrue(str(testDatasetEnargus.datenbank) == data[0][3])
        self.assertTrue(str(testDatasetEnargus.thema) == data[0][4])

        # check what happens, if two times the same dataset is loaded:
        management.call_command('data_import', fileNameContainingTestData)

        # still only one dataset should be present in the database:
        self.assertTrue(len(Teilprojekt.objects.all()) == 1)

        # check if the dataset was corretly loaded into the DB:
        testDatasetFromDB = Teilprojekt.objects.filter(fkz=data[0][0])[0]  
        
        testDatasetEnargus = testDatasetFromDB.enargus_daten

        self.assertTrue(str(testDatasetEnargus.laufzeitbeginn) == data[0][1])
        self.assertTrue(str(testDatasetEnargus.laufzeitende) == data[0][2])
        self.assertTrue(str(testDatasetEnargus.datenbank) == data[0][3])
        self.assertTrue(str(testDatasetEnargus.thema) == data[0][4])

        time.sleep(1)

    def testSameFKZTwoTimesInCSV(self):
        """Tests, if MultipleFKZDatasets-Exception is raised.
        
        This method tests the behaviour of the `data_import` if the same
        FKZ (Förderkennzeichen) is present multiple times in the 
        .csv-file and every dataset is different. Such a case could
        lead to a wrong representation of the Database by the 
        .yaml-file and therefore raises the User defined 
        MultipleFKZDatasets-Exception.
        """

        csvFileToBeLoaded = "testData/enargus_testMultipleTimesSameDataset.csv"
        try:
            management.call_command('data_import', csvFileToBeLoaded)
        except MultipleFKZDatasets:
            time.sleep(1)
            return
        
        self.assertTrue(False)

    
    def testIfYAMLRepresentsDBState(self) -> None:
        """This method tests if the Database State-Differences, which are 
        specified in the .yaml file, are acutally present in the Database.
        Therefore it loads two .csv files, which include different 
        datasets for the same Förderkennziffer (fkz). This should produce
        a .yaml-file, which shows the differences. Th

        Returns: 
        None
        """

        fileNameContainingTestData = "testData/enargus_testDatabaseFile.csv"
        management.call_command('data_import', fileNameContainingTestData)

        fileNameModifiedTestData = "testData/enargus_testDatabaseFileModified.csv"
        management.call_command('data_import', fileNameModifiedTestData)
        
        newestFileName = self._getNewestYAML()

        listOfDBDifferenceObjs = []

        with open(newestFileName, "r") as file:
            for databaseDifferenceObj in yaml.load_all(file, Loader=yaml.Loader):
                databaseDifferenceObj.postprocessAfterReadIn()
                listOfDBDifferenceObjs.append(databaseDifferenceObj)
            
        for databaseDiffObj in listOfDBDifferenceObjs:
            nestedDictContainingDiffs = databaseDiffObj.differencesSortedByTable
            dictMappingToTable = self._getTablesFromDiffDataStructure(
                nestedDictContainingDiffs
            ) 
            self._checkIfDifferencesFromYAMLAreInDB(
                nestedDictContainingDiffs, 
                dictMappingToTable
            )
        
        time.sleep(1)

    def testExecuteDatabaseChangeskeepCurrent(self):
        """Tests`execute_db_changes`, whereby `keepCurrentState` set to True
 
        
        """

        loadInitialStateOfDB = "testData/enargus_load10Datasets.csv"
        management.call_command('data_import', loadInitialStateOfDB)

        updateDatasetInDB = "testData/enargus_testExecuteDBchanges.csv"
        management.call_command('data_import', updateDatasetInDB)

        newestYAMLFileName = self._getNewestYAML()
        nameYAMLFileAfterUserInput = newestYAMLFileName[0:-5] + "Curr.yml"

        with open(newestYAMLFileName, "r") as file:
            for databaseDifferenceObj in yaml.load_all(file, Loader=yaml.Loader):
                databaseDifferenceObj.postprocessAfterReadIn()

                databaseDifferenceObj.keepCurrentState = True
                databaseDifferenceObj.keepPendingState = False
                databaseDifferenceObj.writeToYAML(nameYAMLFileAfterUserInput)

        
        management.call_command(
            'execute_db_changes', 
            nameYAMLFileAfterUserInput,
        )

        with open(nameYAMLFileAfterUserInput, "r") as file:
            for currentDifferenceObj in yaml.load_all(file, Loader=yaml.Loader):
                currentDifferenceObj.postprocessAfterReadIn()
                differencesStruct = currentDifferenceObj.differencesSortedByTable
                self._checkIfDifferencesFromYAMLAreInDB(
                    differencesStruct,
                    self._getTablesFromDiffDataStructure(differencesStruct),
                    currentDifferenceObj.keepCurrentState,
                    currentDifferenceObj.keepPendingState,
                )
        
        time.sleep(1)

    def testExecuteDatabaseChangeskeepCSV(self):
        """Tests`execute_db_changes`, whereby `keepPendingState` set to True 
        
        """
        loadInitialStateOfDB = "testData/enargus_load10Datasets.csv"
        management.call_command('data_import', loadInitialStateOfDB)

        updateDatasetInDB = "testData/enargus_testExecuteDBchanges.csv"
        management.call_command('data_import', updateDatasetInDB)

        newestYAMLFileName = self._getNewestYAML()
        nameYAMLFileAfterUserInput = newestYAMLFileName[0:-5] + "CSV.yml"

        with open(newestYAMLFileName, "r") as file:
            for databaseDifferenceObj in yaml.load_all(file, Loader=yaml.Loader):
                databaseDifferenceObj.postprocessAfterReadIn()

                databaseDifferenceObj.keepCurrentState = False
                databaseDifferenceObj.keepPendingState = True
                databaseDifferenceObj.writeToYAML(nameYAMLFileAfterUserInput)

        
        management.call_command(
            'execute_db_changes', 
            nameYAMLFileAfterUserInput,
        )

        with open(nameYAMLFileAfterUserInput, "r") as file:
            for currentDifferenceObj in yaml.load_all(file, Loader=yaml.Loader):
                currentDifferenceObj.postprocessAfterReadIn()
                differencesStruct = currentDifferenceObj.differencesSortedByTable
                self._checkIfDifferencesFromYAMLAreInDB(
                    differencesStruct,
                    self._getTablesFromDiffDataStructure(differencesStruct),
                    currentDifferenceObj.keepCurrentState,
                    currentDifferenceObj.keepPendingState,
                )             
        
        time.sleep(1)

    def testModulZuordnungLoadSimpleDataset(self):
        """Load Modulzuordnung-Data, Test if .YAML file is created on conflict.
        
        """

        simpleModulzurodnungDatasets = "testData/modulzuordnung_simpleLoading.csv"
        management.call_command("data_import", simpleModulzurodnungDatasets)

        simpleModulzurodnungDatasets = "testData/modulzuordnung_simpleEdits.csv"
        management.call_command("data_import", simpleModulzurodnungDatasets)

        newestYAMLFile = self._getNewestYAML()

        with open(newestYAMLFile, "r") as file:
            for currentDifferenceObj in yaml.load_all(file, Loader=yaml.Loader):
                currentDifferenceObj.postprocessAfterReadIn()
                differencesStruct = currentDifferenceObj.differencesSortedByTable
                self._checkIfDifferencesFromYAMLAreInDB(
                    differencesStruct,
                    self._getTablesFromDiffDataStructure(differencesStruct),
                )                           

        time.sleep(1)
    
    # def testLoadingAndUpdatingTools(self):
    #     """ Loads and updates Tools
        
    #     """
    #     simpleModulzurodnungDatasets = "testData/Tools_simpleDatasets.csv"
    #     management.call_command("data_import", simpleModulzurodnungDatasets)

    #     simpleModulzurodnungDatasets = "testData/Tools_simpleDatasetsModified.csv"
    #     management.call_command("data_import", simpleModulzurodnungDatasets)

    #     newestYAMLFile = self._getNewestYAML()

    #     with open(newestYAMLFile, "r") as file:
    #         for currentDifferenceObj in yaml.load_all(file, Loader=yaml.Loader):
    #             currentDifferenceObj.postprocessAfterReadIn()
    #             differencesStruct = currentDifferenceObj.differencesSortedByTable
    #             self._checkIfDifferencesFromYAMLAreInDB(
    #                 differencesStruct,
    #                 self._getTablesFromDiffDataStructure(differencesStruct),
    #             )                           

    #     time.sleep(1)

    def testLoadingAndUpdatingTags(self):
        """ Loads and updates Schlagwörter
        
        """

        #management.call_command("migrate")

        simpleModulzurodnungDatasets = "testData/schlagwoerter_simpleTestData.csv"
        management.call_command("data_import", simpleModulzurodnungDatasets)

        simpleModulzurodnungDatasets = "testData/schlagwoerter_simpleTestDataModified.csv"
        management.call_command("data_import", simpleModulzurodnungDatasets)
        newestYAMLFile = self._getNewestYAML()

        with open(newestYAMLFile, "r") as file:
            for currentDifferenceObj in yaml.load_all(file, Loader=yaml.Loader):
                currentDifferenceObj.postprocessAfterReadIn()
                differencesStruct = currentDifferenceObj.differencesSortedByTable
                self._checkIfDifferencesFromYAMLAreInDB(
                    differencesStruct,
                    self._getTablesFromDiffDataStructure(differencesStruct),
                )                           

        time.sleep(1) 

        exportFileKeepCurrent = newestYAMLFile[:-5] + "keepCurr.yml"

        # change each DifferenceObject to keep-Current-DB-State
        with open(newestYAMLFile, "r") as file:
            for currentDifferenceObj in yaml.load_all(file, Loader=yaml.Loader):
                currentDifferenceObj.postprocessAfterReadIn()
                differencesStruct = currentDifferenceObj.differencesSortedByTable
                currentDifferenceObj.keepCurrentState = True
                currentDifferenceObj.keepPendingState = False
                currentDifferenceObj.writeToYAML(exportFileKeepCurrent)

        # keep the current state for all Diffs and delete the CSV-state:
        management.call_command("execute_db_changes", exportFileKeepCurrent)
        with open(exportFileKeepCurrent, "r") as file:
            for currentDifferenceObj in yaml.load_all(file, Loader=yaml.Loader):
                currentDifferenceObj.postprocessAfterReadIn()
                differencesStruct = currentDifferenceObj.differencesSortedByTable
                self._checkIfDifferencesFromYAMLAreInDB(
                    differencesStruct,
                    self._getTablesFromDiffDataStructure(differencesStruct),
                    currentDifferenceObj.keepCurrentState,
                    currentDifferenceObj.keepPendingState,
                ) 
        
        time.sleep(1)

        # load again the csv-state, but discard now the current-state:
        simpleModulzurodnungDatasets = "testData/schlagwoerter_simpleTestDataModified.csv"
        management.call_command("data_import", simpleModulzurodnungDatasets)
        newestYAMLFile = self._getNewestYAML()

        exportFileKeepCSV = newestYAMLFile[:-5] + "keepCSV.yml"

        # change each DifferenceObject to keep-Current-DB-State
        with open(newestYAMLFile, "r") as file:
            for currentDifferenceObj in yaml.load_all(file, Loader=yaml.Loader):
                currentDifferenceObj.postprocessAfterReadIn()
                differencesStruct = currentDifferenceObj.differencesSortedByTable
                currentDifferenceObj.keepCurrentState = False
                currentDifferenceObj.keepPendingState = True
                currentDifferenceObj.writeToYAML(exportFileKeepCSV)

        management.call_command("execute_db_changes", exportFileKeepCSV)
        with open(exportFileKeepCSV, "r") as file:
            for currentDifferenceObj in yaml.load_all(file, Loader=yaml.Loader):
                currentDifferenceObj.postprocessAfterReadIn()
                differencesStruct = currentDifferenceObj.differencesSortedByTable
                self._checkIfDifferencesFromYAMLAreInDB(
                    differencesStruct,
                    self._getTablesFromDiffDataStructure(differencesStruct),
                    currentDifferenceObj.keepCurrentState,
                    currentDifferenceObj.keepPendingState,
                ) 
        
        time.sleep(1)



    def _checkIfDifferencesFromYAMLAreInDB(
            self, 
            nestedDictContainingDiffs: dict, 
            dictMappingToTable: dict,
            keepCurrentState=None,
            keepPendingState=None,
    ) -> None:
        """This method tests, if the two Database-states descried in the
        .yaml file are acutally present in the Database.

        nestedDictContainingDiffs:  dict
            Nested Dictionary containing the current DB-state and the 
            CSV-state.
        dictMappingToTable: dict
            Dictionary, which does a mapping between the entries of  
            nestedDictContainingDiffs and the actual Modelnames.
        
        Returns:
        None
        """
        allModels = importlib.import_module("project_listing.models")

        for tableDictKey in list(nestedDictContainingDiffs.keys()):

            tableName = dictMappingToTable[tableDictKey]
            dictOfDifferences = nestedDictContainingDiffs[tableDictKey]
            currentDBStateInTable = dictOfDifferences["currentState"]
            CSVState = dictOfDifferences["pendingState"]
            
            if "schlagwortregister_erstsichtung" in tableDictKey.split(".")[1]:
                schlagwortregisterIDcurrent =  nestedDictContainingDiffs[tableDictKey]["currentState"]["schlagwortregister_id"]
            # check if both states are present in the DB, 
            # like they are shown in the .yaml-file:
            currentTableModel = allModels.__getattribute__(tableName) 
            if keepCurrentState == None and keepPendingState == None:
                if len(currentTableModel.objects.filter(**currentDBStateInTable)) != 1 or len(currentTableModel.objects.filter(**CSVState)) != 1:
                    pdb.set_trace()
                self.assertTrue(
                    len(currentTableModel.objects.filter(**currentDBStateInTable)) == 1,
                )
                self.assertTrue(
                    len(currentTableModel.objects.filter(**CSVState)) == 1,
                )

            
            elif keepCurrentState == True and keepPendingState == False:
                self.assertTrue(
                    len(currentTableModel.objects.filter(**currentDBStateInTable)) == 1,
                    "User specified to keep current-state of Database, \
                    but current state is not present in database anymore!",
                )
                self.assertTrue(
                    len(currentTableModel.objects.filter(**CSVState)) == 0,
                    "User specified to keep current state, \
                    but csv-state was not removed from Database!",
                )
            elif keepCurrentState == False and keepPendingState == True:
                
                if "Schlagwort" in str(currentTableModel) and not "Schlagwortregister_erstsichtung" in str(currentTableModel):
                    #pdb.set_trace()
                    tagToBeChecked = currentDBStateInTable["schlagwort_id"]
                    for numberPosition in range(1, 7):
                        dictCurrTagNum = {f"schlagwort_{numberPosition}_id": tagToBeChecked}
                        queryForCurrTag = Schlagwortregister_erstsichtung.objects.filter(**dictCurrTagNum)
                        for query in queryForCurrTag:
                            if query.schlagwortregister_id == int(schlagwortregisterIDcurrent):
                                self.assertTrue(False)
                    
                else:               
                    self.assertTrue(
                        len(currentTableModel.objects.filter(**currentDBStateInTable)) == 0,
                        "User specified to remove current state from DB, \
                    but current state is still present!",
                    )               
                if len(currentTableModel.objects.filter(**currentDBStateInTable)) != 0 or len(currentTableModel.objects.filter(**CSVState)) != 1:
                    pdb.set_trace()

                self.assertTrue(
                    len(currentTableModel.objects.filter(**CSVState)) == 1,
                    "User specified to keep csv-state, \
                    but csv-state is not present in Database!",
                )
            else:
                self.assertTrue(
                    keepCurrentState ^ keepPendingState,
                    "One state must be kept and one state must be discarded",    
                )                                   


    def _getNewestYAML(self) -> str:
        """This method is a helper function for the Testcases. It iterates 
        through all .yaml files in the current directory and searches for 
        the one, which has the newest timestamp. If the timestamp of the 
        newest .yaml file is older than 2 minutes, the assert staatement 
        raises and error.

        Returns: 
        newestFileName: str
            string, which represents the name of the newest .yaml file.
        """

        fileContents = os.listdir()
        #newest = datetime.datetime(year=2000, month=1, day=1, hour=12, minute=0)
        newest = 0
        newestFileName = ""
        for currentFilename in fileContents:
            if ".yaml" in currentFilename:


                fileWithoutExtension = currentFilename[0:-5]

                if int(fileWithoutExtension) > newest:
                    newest = int(fileWithoutExtension)
                    newestFileName = currentFilename
        
        # check, if the timestamp of the newly created file, lies in the last
        # 2 minutes:
        currentTime = datetime.datetime.now()
        
        #pdb.set_trace()
        self.assertTrue(
            newest + 2*60 > currentTime.timestamp(), 
            "Newest .YAML-File has an too old Timestamp!",
        )

        return newestFileName

    def _getTablesFromDiffDataStructure(
            self, 
            nestedDictContainingDiffs: dict,
    ) -> dict:
        """This method is a helper-function to get the Tablenames from the 
        Database-Difference-Object, in which differences between the current 
        state and the .csv-state are present.
        
        nestedDictContainingDiffs:  dict
            Nested Dictionary containing as keys the tables, in which 
            Differences are present, and as values another Dictionary, 
            which contains as keys the field-names and as values the 
            values, which are present in the DB-state respectivly in 
            the .csv-state.
        
        Returns:
        returnDict:   dict
            List of tables of type string, in which the differences are 
            present.    
        """
        allModels = importlib.import_module("project_listing.models")
        allAttrOfModels = dir(allModels)
        returnDict = {}
        for currentTableKey in list(nestedDictContainingDiffs.keys()):
            for attributeName in allAttrOfModels:
                tableName = currentTableKey.split(".")[1]
                if (
                    tableName.lower() in attributeName.lower() 
                    or attributeName.lower() in tableName.lower()
                ):
                    
                    returnDict[currentTableKey] = attributeName
    
        return returnDict