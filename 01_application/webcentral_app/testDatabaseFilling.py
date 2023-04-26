"""

"""
import datetime
import importlib
import time
import os
import pdb
import random


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

    def testSameFKZTwoTimesInCSV(self):
        """Tests, if MultipleFKZDatasets-Exception is raised.
        
        This method tests the behaviour of the `data_import` if the same
        FKZ (Förderkennzeichen) is present multiple times in the 
        .csv-file and every dataset is different. Such a case could
        lead to a wrong representation of the Database by the 
        .yaml-file and therefore raises the User defined 
        MultipleFKZDatasets-Exception.
        """

        csvFileToBeLoaded = "../../02_work_doc/10_test/04_testData/enargus_testMultipleTimesSameDataset.csv"
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

        fileNameContainingTestData = "../../02_work_doc/10_test/04_testData/enargus_testDatabaseFile.csv"
        management.call_command('data_import', fileNameContainingTestData)

        fileNameModifiedTestData = "../../02_work_doc/10_test/04_testData/enargus_testDatabaseFileModified.csv"
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

        loadInitialStateOfDB = "../../02_work_doc/10_test/04_testData/enargus_load10Datasets.csv"
        management.call_command('data_import', loadInitialStateOfDB)

        updateDatasetInDB = "../../02_work_doc/10_test/04_testData/enargus_testExecuteDBchanges.csv"
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
        loadInitialStateOfDB = "../../02_work_doc/10_test/04_testData/enargus_load10Datasets.csv"
        management.call_command('data_import', loadInitialStateOfDB)

        updateDatasetInDB = "../../02_work_doc/10_test/04_testData/enargus_testExecuteDBchanges.csv"
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
        
        choiceKeepDBOrCSV = [(True, False), (False, True)]
        choiceToBeKept = random.choice(choiceKeepDBOrCSV)

        simpleModulzurodnungDatasets = \
            "../../02_work_doc/10_test/04_testData/modulzuordnung_simpleLoading.csv"
        management.call_command("data_import", simpleModulzurodnungDatasets)
        time.sleep(1)
        simpleModulzurodnungDatasetsModified = "../../02_work_doc/10_test/04_testData/modulzuordnung_simpleEdits.csv"
        management.call_command("data_import", simpleModulzurodnungDatasetsModified)

        newestYAMLFileName = self._getNewestYAML()
        nameYAMLFileAfterUserInput = newestYAMLFileName[0:-5] + "Curr.yml"

        with open(newestYAMLFileName, "r") as file:
            for currentDifferenceObj in yaml.load_all(file, Loader=yaml.Loader):
                currentDifferenceObj.postprocessAfterReadIn()
                differencesStruct = currentDifferenceObj.differencesSortedByTable
                self._checkIfDifferencesFromYAMLAreInDB(
                    differencesStruct,
                    self._getTablesFromDiffDataStructure(differencesStruct),
                )                           
                currentDifferenceObj.keepCurrentState = choiceToBeKept[0]
                currentDifferenceObj.keepPendingState = choiceToBeKept[1]
                currentDifferenceObj.writeToYAML(nameYAMLFileAfterUserInput)

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




    def testLoadingAndUpdatingTags(self) -> None:
        """ Loads and updates Schlagwörter

        This method tests, if a .YAML-file is created, when two .csv-
        files with the same Förderkennzeichen but differences in the 
        datasets are loaded. It then tests, if the .YAML-File 
        represents the state in the Database (if current and pending
        dataset are present in the database like they are written in 
        the .YAML-File). 
        After that, a new .YAML-File is created, and the 
        Database-Differences from the previous .YAML-File 
        are written there, but the Flag to keep the current-state is
        updated. The .YAML-File is then given to the `excute_db_changes`.
        This should delete all datasets, which were present in the YAML
        File and were marked as pending. 
        After that, it is tested if the curretn state is still prsesent
        and the pending state is deleted.
        The same procedure is done, but now the pending state is marked
        to be kept and the current state is marked to be deleted. After
        execution of `execute_db_changes` it is tested, if the commits
        are present in the database.
        
        """
        
        choiceKeepDBOrCSV = [(True, False), (False, True)]
        choiceToBeKept = random.choice(choiceKeepDBOrCSV)

        simpleTagsDatasets = \
            "../../02_work_doc/10_test/04_testData/schlagwoerter_simpleTestData.csv"
        management.call_command("data_import", simpleTagsDatasets)

        simpleTagsModifiedDataset = \
            "../../02_work_doc/10_test/04_testData/schlagwoerter_simpleTestDataModified.csv"
        management.call_command("data_import", simpleTagsModifiedDataset)
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
                currentDifferenceObj.keepCurrentState = choiceToBeKept[0]
                currentDifferenceObj.keepPendingState = choiceToBeKept[1]
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
        schlagwortregisterIDcurrent = None
        for tableDictKey in list(nestedDictContainingDiffs.keys()):

            tableName = dictMappingToTable[tableDictKey]
            dictOfDifferences = nestedDictContainingDiffs[tableDictKey]
            currentDBStateInTable = dictOfDifferences["currentState"]
            CSVState = dictOfDifferences["pendingState"]
            
            if "schlagwortregister_erstsichtung" in tableDictKey.split(".")[1]:
                if not keepCurrentState and keepCurrentState is not None:
                    schlagwortregisterIDcurrent =  nestedDictContainingDiffs\
                        [tableDictKey]["currentState"]["schlagwortregister_id"]
                elif not keepPendingState and keepPendingState is not None:
                    schlagwortregisterIDcurrent =  nestedDictContainingDiffs\
                        [tableDictKey]["pendingState"]["schlagwortregister_id"]
                    
            # check if both states are present in the DB, 
            # like they are shown in the .yaml-file:
            currentTableModel = allModels.__getattribute__(tableName)
            if (keepCurrentState == None 
                and keepPendingState == None 
            ):
                self._doAssertation(
                    currentTableModel, 
                    currentDBStateInTable, 
                    1, 
                    "", 
                    schlagwortregisterIDcurrent
                )
                self._doAssertation(
                    currentTableModel, 
                    CSVState, 
                    1, 
                    "", 
                    schlagwortregisterIDcurrent,
                )

            elif keepCurrentState == True and keepPendingState == False:
                self._doAssertation(
                    currentTableModel, 
                    currentDBStateInTable, 
                    1, 
                    "User specified to keep current-state of Database, \
                    but current state is not present in database anymore!", 
                    schlagwortregisterIDcurrent,
                )
                
                self._doAssertation(
                    currentTableModel, 
                    CSVState, 
                    0, 
                    "User specified to keep current state, \
but csv-state was not removed from Database!",
                    schlagwortregisterIDcurrent,
                )

            elif keepCurrentState == False and keepPendingState == True:
                       
                self._doAssertation(
                    currentTableModel, 
                    currentDBStateInTable, 
                    0,                         
                    "User specified to remove current state from DB, \
                    but current state is still present!", 
                    schlagwortregisterIDcurrent,
                )
                self._doAssertation(
                    currentTableModel, 
                    CSVState, 
                    1,                     
                    "User specified to keep csv-state, \
                    but csv-state is not present in Database!", 
                    schlagwortregisterIDcurrent,
                )                       
            else:
                self.assertTrue(
                    keepCurrentState ^ keepPendingState,
                    "One state must be kept and one state must be discarded",    
                )                                   

    def _doAssertation(
            self, 
            currentTableModel, 
            stateDict, 
            lengthOfQuerySet, 
            assertationMessage, 
            schlagwortregisterIDcurrent
        ):
        """
        
        """
        
        if not self._checkIfIDisNone(stateDict):
            if not ("Schlagwort" in str(currentTableModel)
                    and not "Schlagwortregister_erstsichtung" in str(
                currentTableModel
                )
                ):
                #try:

                self.assertTrue(
                    len(
                    currentTableModel.objects.filter(**stateDict)
                    ) == lengthOfQuerySet,
                    assertationMessage,
                )
                # except:
                #     pdb.set_trace()
            elif (
                ("Schlagwort" in str(currentTableModel) 
                and not "Schlagwortregister_erstsichtung" in str(currentTableModel)) 
                and lengthOfQuerySet == 0 
                and schlagwortregisterIDcurrent is not None
            ):
                tagToBeChecked = stateDict["schlagwort_id"]
                for numberPosition in range(1, 7):
                    dictCurrTagNum = {
                        f"schlagwort_{numberPosition}_id": tagToBeChecked
                    }
                    queryForCurrTag = Schlagwortregister_erstsichtung\
                        .objects.filter(**dictCurrTagNum)
                    for query in queryForCurrTag:
                        if (query.schlagwortregister_id 
                            == int(schlagwortregisterIDcurrent)):
                            self.assertTrue(False)              


    def _checkIfIDisNone(self, tableDict: dict) -> str:
        """This method finds the key-value pair in the current table 
        dictionary, in which the ID of the Data-Tuple is stored. It does this
        by iterating through the dictionary-keys and checks if '_id' is
        present in the string.

        tableDict:  dict
            Dictionary of the DatabaseDifference-Object containing the state 
            of one table either in current or csv-state.
        
        Returns:
        dictKey:    str
            string representation of the key, containing the id-of the tuple.

        """

        for dictKey in list(tableDict.keys()):
            if "_id" in dictKey:
                if tableDict[dictKey] == "None" or tableDict[dictKey] is None:
                    return True
        return False

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