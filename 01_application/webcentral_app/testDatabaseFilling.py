"""This module tests the data-import into the database. 

Therefore it uses the Django-Testrunner. It loads different testdatasets
located in `02_work_doc/10_test/04_testData` with the `data_import`- 
Command into the Django ORM, and tests resolving conflicts with the 
`execute_db_changes`-command. The Test can be executed via the 
`manage.py`:
```
    python3 manage.py test testDatabaseFilling
```
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
import pandas as pd
import yaml

from project_listing.models import (
    Subproject,
    ModuleAssignment,
    Enargus,
)
from keywords.models import (
    KeywordRegisterFirstReview,
    Keyword,
)
from tools_over.models import (
    Tools,
)
from publications.models.publication import Publication
import pandas as pd
import glob
import os
from datetime import datetime
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

    def setUp(self):
        """
        
        """

        self.allModels = [
            importlib.import_module("project_listing.models"),
            importlib.import_module("keywords.models"),
        ]

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
            management.call_command(
                'data_import', 
                csvFileToBeLoaded,
                "testFiles/",
            )
        except MultipleFKZDatasets:
            time.sleep(1)
            return
        
        self.assertTrue(False)

        time.sleep(2)

    
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
        management.call_command(
            'data_import', 
            fileNameContainingTestData,
            "testFiles/",    
        )

        newestFilePath = self._getNewestYAML()
        head, newestFileName = os.path.split(newestFilePath)
        if (
            newestFileName == "" 
            or int(newestFileName[0:-5]) + 2 < datetime.datetime.now().timestamp()
            ):
            fileNameModifiedTestData = "../../02_work_doc/10_test/04_testData/enargus_testDatabaseFileModified.csv"
            management.call_command(
                'data_import', 
                fileNameModifiedTestData,
                "testFiles/",    
            )
            newestFilePath = self._getNewestYAML()
            head, newestFileName = os.path.split(newestFilePath)
        
        listOfDBDifferenceObjs = []

        with open(newestFilePath, "r") as file:
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
        
        time.sleep(2)

    def testExecuteDatabaseChangeskeepCurrent(self):
        """Tests`execute_db_changes`, whereby `keepCurrentState` set to True
 
        """

        loadInitialStateOfDB = "../../02_work_doc/10_test/04_testData/enargus_load10Datasets.csv"
        management.call_command(
            'data_import', 
            loadInitialStateOfDB,
            "testFiles/",    
        )

        newestYAMLFilePath = self._getNewestYAML()
        head, newestYAMLFileName = os.path.split(newestYAMLFilePath)
        updateDatasetInDB = "../../02_work_doc/10_test/04_testData/enargus_testExecuteDBchanges.csv"
        if (
            newestYAMLFileName == "" 
            or int(newestYAMLFileName[0:-5]) + 2 < datetime.datetime.now().timestamp()
            ):
            management.call_command(
                'data_import', 
                updateDatasetInDB,
                "testFiles/",
            )
            newestYAMLFilePath = self._getNewestYAML()
            head, newestYAMLFileName = os.path.split(newestYAMLFilePath)

        nameYAMLFileAfterUserInput = os.path.join(
            "testFiles/", 
            newestYAMLFileName[0:-5] + "Curr.yml",
        )

        with open(newestYAMLFilePath, "r") as file:
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
        
        time.sleep(2)

    def testExecuteDatabaseChangeskeepCSV(self):
        """Tests`execute_db_changes`, whereby `keepPendingState` set to True 
        
        """
        loadInitialStateOfDB = "../../02_work_doc/10_test/04_testData/enargus_load10Datasets.csv"
        management.call_command(
            'data_import', 
            loadInitialStateOfDB,
            "testFiles/",
        )

        newestYAMLFilePath = self._getNewestYAML()
        head, newestYAMLFileName = os.path.split(newestYAMLFilePath)
        updateDatasetInDB = "../../02_work_doc/10_test/04_testData/enargus_testExecuteDBchanges.csv"
        if (
            newestYAMLFileName == "" 
            or int(newestYAMLFileName[0:-5]) + 2 < datetime.datetime.now().timestamp()
            ):
            management.call_command(
                'data_import', 
                updateDatasetInDB,
                "testFiles/",
            )
            newestYAMLFilePath = self._getNewestYAML()
            head, newestYAMLFileName = os.path.split(newestYAMLFilePath)

        nameYAMLFileAfterUserInput = os.path.join(
            "testFiles/", 
            newestYAMLFileName[0:-5] + "CSV.yml",
        )
        with open(newestYAMLFilePath, "r") as file:
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
        
        time.sleep(2)

    def testModulZuordnungLoadSimpleDataset(self):
        """Load Modulzuordnung-Data, Test if .YAML file is created on conflict.
        
        """
        
        choiceKeepDBOrCSV = [(True, False), (False, True)]
        choiceToBeKept = random.choice(choiceKeepDBOrCSV)

        simpleModulzurodnungDatasets = \
            "../../02_work_doc/10_test/04_testData/modulzuordnung_simpleLoading.csv"
        management.call_command(
            "data_import", 
            simpleModulzurodnungDatasets,
            "testFiles/",
        )

        newestYAMLFilePath = self._getNewestYAML()
        head, newestYAMLFileName = os.path.split(newestYAMLFilePath)
        simpleModulzurodnungDatasetsModified = "../../02_work_doc/10_test/04_testData/modulzuordnung_simpleEdits.csv"
        if (newestYAMLFileName == "" 
            or int(newestYAMLFileName[0:-5]) + 2 < datetime.datetime.now().timestamp()
            ):
            management.call_command(
                "data_import", 
                simpleModulzurodnungDatasetsModified,
                "testFiles/",
            )
            newestYAMLFilePath = self._getNewestYAML()
            head, newestYAMLFileName = os.path.split(newestYAMLFilePath)

        nameYAMLFileAfterUserInput = os.path.join(
            "testFiles/", 
            newestYAMLFileName[0:-5] + "_edited.yml",
        )
        with open(newestYAMLFilePath, "r") as file:
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

    def testLoadSimpleToolData(self):
        """Load `AcceptMission`-Tool into Database.

        This method tests the loading of the `AcceptMission`-Tool into the
        database. It tests, if a .xslx-file can be used as input for the
        `data_import`-command. Furthermore it is tested, if all columns
        are present in the database after the loading process.

        """

        simpleToolsDataset = \
            "../../02_work_doc/10_test/04_testData/test_data_tool.xlsx"
        management.call_command(
            "data_import", 
            simpleToolsDataset,
            "testFiles/",
        )
        # breakpoint()
        # the xlsx file is also loaded here to test if the data_import works
        readToolTestfile = pd.read_excel("../../02_work_doc/10_test/04_testData/test_data_tool.xlsx")
        readToolTestfile = readToolTestfile.fillna("")
        toolAsDict = readToolTestfile.to_dict()
        # breakpoint()
        acceptMissionToolInDB = list(Tools.objects.filter(name=toolAsDict["name"][0]))[-1]
        for key in toolAsDict.keys():
            if key != "name":
                # check if attribute is a ManyToMany-relation:
                if getattr(acceptMissionToolInDB, key).__class__.__name__ == "ManyRelatedManager":
                    manyToManyValues = getattr(acceptMissionToolInDB, key).all()
                    manyToManyString = ""
                    for index, value in enumerate(manyToManyValues):
                        if index == 0:
                            manyToManyString += value.__getattribute__(key[0].lower() + key[1:])
                        else:
                            manyToManyString += ", " + value.__getattribute__(key[0].lower() + key[1:])
                    self.assertEqual(manyToManyString, toolAsDict[key][0])
                else:
                    if getattr(acceptMissionToolInDB, key) is None:
                        self.assertEqual("", toolAsDict[key][0])
                    else:
                        self.assertEqual(getattr(acceptMissionToolInDB, key), toolAsDict[key][0])

    def testUpdateToolData(self):
        """

        This test loads the test_tools_data.xlsx into the empty database. After that, an arbitrary cell
        of the loaded test_tools_data.xlsx is changed and the data_import command is called again. 

        """
        simpleToolsDataset = \
            "../../02_work_doc/10_test/04_testData/test_data_tool.xlsx"
        management.call_command(
            "data_import", 
            simpleToolsDataset,
            "testFiles/",
        )
        # the xlsx file is also loaded here to test if the data_import works
        readToolTestfile = pd.read_excel("../../02_work_doc/10_test/04_testData/test_data_tool.xlsx")
        readToolTestfile = readToolTestfile.fillna("")
        toolAsDict = readToolTestfile.to_dict()

        toolKeys = list(toolAsDict.keys())
        toolKeys.remove("name")
        randomToolKey = random.choice(toolKeys)
        randomToolValue = toolAsDict[randomToolKey][0]
        
        if isinstance(randomToolValue, str):
            if randomToolKey == "lastUpdate":
                possibleValues = [self._generateRandomDate(), "laufend", "unbekannt"]
                randomToolValue = random.choice(possibleValues)
            if randomToolValue.find(",") == -1:
                randomToolValue += "test-String"
            else:
                randomToolValue += ", test-String"
        elif isinstance(randomToolValue, int):
            randomToolValue += 1
        
        toolAsDict[randomToolKey][0] = randomToolValue
        
        # Convert the dictionary to a DataFrame
        modified_tool_df = pd.DataFrame.from_dict(toolAsDict)

        # Save the DataFrame as an xlsx file
        modified_tool_df.to_excel("../../02_work_doc/10_test/04_testData/modified_test_data_tool.xlsx", index=False)

        modifedToolsDataset = \
            "../../02_work_doc/10_test/04_testData/modified_test_data_tool.xlsx"
        management.call_command(
            "data_import", 
            modifedToolsDataset,
            "testFiles/",
        )

        # Get the current date and time
        now = datetime.now()
        dateString = now.strftime("%d%m%Y_%H%M%S")

        # Define the file pattern
        filePattern = f"testFiles/modified_test_data_tool_{dateString}.yaml"

        # Check if a file matching the pattern exists
        self.assertTrue(glob.glob(filePattern))

        listOfParsedConflicts = []

        with open(filePattern, "r") as stream:
            for databaseDifferenceObj in yaml.load_all(stream, Loader=yaml.Loader):
                databaseDifferenceObj.postprocessAfterReadIn()
                databaseDifferenceObj.keepCurrentState = False
                databaseDifferenceObj.keepPendingState = True
                listOfParsedConflicts.append(databaseDifferenceObj)        

        self.assertEqual(len(listOfParsedConflicts), 1)

        for tableKey in listOfParsedConflicts[0].differencesSortedByTable.keys():
            for attributeKey in listOfParsedConflicts[0].differencesSortedByTable[tableKey]["pendingState"]:
                if attributeKey != "id":
                    pendingObj = listOfParsedConflicts[0].differencesSortedByTable[tableKey]["pendingState"][attributeKey]
                    if pendingObj[-1] == ",":
                        pendingObj = pendingObj[:-1]
                    self.assertEqual(
                        pendingObj,
                        toolAsDict[attributeKey][0],
                    )
        listOfParsedConflictsForOutput = []
        with open(filePattern, "r") as stream:
            for databaseDifferenceObj in yaml.load_all(stream, Loader=yaml.Loader):
                databaseDifferenceObj.keepCurrentState = False
                databaseDifferenceObj.keepPendingState = True
                listOfParsedConflictsForOutput.append(databaseDifferenceObj)   
        outputFilePattern = filePattern[:-5] + "_edited.yml"
        
        with open(outputFilePattern, "w") as stream:
            yaml.dump_all(listOfParsedConflictsForOutput, stream)
        
        management.call_command(
            "execute_db_changes", 
            outputFilePattern,
        )

        # check if there is still only one tool with the name "AcceptMission" in the database
        self.assertEqual(len(Tools.objects.filter(name=toolAsDict["name"][0])), 1)

        # check if the tool in the database has the same values as the tool in the modified_test_data_tool.xlsx
        toolInDB = Tools.objects.filter(name=toolAsDict["name"][0])[0]
        for key in toolAsDict.keys():
            if key != "name":
                # check if attribute is a ManyToMany-relation:
                if getattr(toolInDB, key).__class__.__name__ == "ManyRelatedManager":
                    manyToManyValues = getattr(toolInDB, key).all()
                    manyToManyString = ""
                    for index, value in enumerate(manyToManyValues):
                        if index == 0:
                            manyToManyString += value.__getattribute__(key[0].lower() + key[1:])
                        else:
                            manyToManyString += ", " + value.__getattribute__(key[0].lower() + key[1:])
                    self.assertEqual(manyToManyString, toolAsDict[key][0])
                else:
                    if getattr(toolInDB, key) is None:
                        self.assertEqual("", toolAsDict[key][0])
                    else:
                        self.assertEqual(getattr(toolInDB, key), toolAsDict[key][0])


        # breakpoint()
        # for tableKey in listOfParsedConflicts[0].differencesSortedByTable.keys():
        #     for attributeKey in listOfParsedConflicts[0].differencesSortedByTable[tableKey]["pendingState"]:
        #         if attributeKey != "id":
        #             pendingObj = listOfParsedConflicts[0].differencesSortedByTable[tableKey]["pendingState"][attributeKey]
        #             if pendingObj[-1] == ",":
        #                 pendingObj = pendingObj[:-1]
        #             self.assertEqual(
        #                 pendingObj,
        #                 toolAsDict[attributeKey][0],
        #             )

    def testLoadSimplePublicationData(self):
        """Load `Publication`-Tool into Database.

        """
        simplePublicationsDataset = \
            "../../02_work_doc/10_test/04_testData/test_data_publications.xlsx"
        management.call_command(
            "data_import", 
            simplePublicationsDataset,
            "testFiles/",
        )       
        readPublicationTestfile = pd.read_excel("../../02_work_doc/10_test/04_testData/test_data_publications.xlsx")
        readPublicationTestfile = readPublicationTestfile.fillna("")
        publicationAsDict = readPublicationTestfile.to_dict()
        # breakpoint()
        for keyInFileDict in publicationAsDict["title"].keys():
            publicationInDB = list(Publication.objects.filter(title=publicationAsDict["title"][keyInFileDict]))[-1]
        
            for key in publicationAsDict.keys():
                # check if attribute is a ManyToMany-relation:
                if getattr(publicationInDB, key).__class__.__name__ == "ManyRelatedManager":
                    manyToManyValues = getattr(publicationInDB, key).all()
                    manyToManyString = ""
                    for index, value in enumerate(manyToManyValues):
                        if index == 0:
                            manyToManyString += value.__getattribute__(key[0].lower() + key[1:])
                        else:
                            manyToManyString += ", " + value.__getattribute__(key[0].lower() + key[1:])
                    self.assertEqual(manyToManyString, publicationAsDict[key][keyInFileDict])
                else:
                    if getattr(publicationInDB, key) is None:
                        self.assertEqual("", publicationAsDict[key][keyInFileDict])
                    else:
                        try:
                            self.assertEqual(getattr(publicationInDB, key), publicationAsDict[key][keyInFileDict])
                        except:
                            pass
    
    def _generateRandomDate(self) -> str:
        """This method generates a random date in the format of YYYY-MM-DD.

        Returns:
        """
        startDate = datetime(2000, 1, 1)
        endDate = datetime.now()

        randomDate = startDate + timedelta(
            seconds=random.randint(0, int((endDate - startDate).total_seconds())),
        )       

        formattedRandomDate = randomDate.strftime('%Y-%m-%d')
        return formattedRandomDate


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
        management.call_command(
            "data_import", 
            simpleTagsDatasets,
            "testFiles/",
        )
        
        newestYAMLFilePath = self._getNewestYAML()
        head, newestYAMLFile = os.path.split(newestYAMLFilePath)
        simpleTagsModifiedDataset = \
    "../../02_work_doc/10_test/04_testData/schlagwoerter_simpleTestDataModified.csv"
        if newestYAMLFile == "" or int(newestYAMLFile[0:-5]) + 2 < datetime.datetime.now().timestamp():
            management.call_command(
                "data_import", 
                simpleTagsModifiedDataset, 
                "testFiles/",
            )
            newestYAMLFilePath = self._getNewestYAML()
            head, newestYAMLFile = os.path.split(newestYAMLFilePath)


        with open(newestYAMLFilePath, "r") as file:
            for currentDifferenceObj in yaml.load_all(file, Loader=yaml.Loader):
                currentDifferenceObj.postprocessAfterReadIn()
                differencesStruct = currentDifferenceObj.differencesSortedByTable
                self._checkIfDifferencesFromYAMLAreInDB(
                    differencesStruct,
                    self._getTablesFromDiffDataStructure(differencesStruct),
                )                           

        time.sleep(2) 

        exportFileKeepCurrent = os.path.join(
            "testFiles/", 
            newestYAMLFile[:-5] + "keepCurr.yml",
        )
        # change each DifferenceObject to keep-Current-DB-State
        with open(newestYAMLFilePath, "r") as file:
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
        
        time.sleep(2)

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
            if "Subproject" in tableDictKey:
                tableName = dictMappingToTable[tableDictKey]

                dictOfDifferences = nestedDictContainingDiffs[tableDictKey]
                currentDBStateInTable = dictOfDifferences["currentState"]
                CSVState = dictOfDifferences["pendingState"]

                for models in self.allModels:
                    try:
                        currentTableModel = models.__getattribute__(tableName)
                        break
                    except:
                        pass

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
            if not ("Keyword" in str(currentTableModel)
                    and not "KeywordRegisterFirstReview" in str(
                currentTableModel
                )
                ):
                if str(currentTableModel) == "<class 'schlagwoerter.models.KeywordRegisterFirstReview'>":
                    schlagwortregisterQuery = currentTableModel.objects.filter(**stateDict)
                    if len(schlagwortregisterQuery) > 0:
                        schlagwortregisterObj = schlagwortregisterQuery[0]
                        if len(schlagwortregisterObj.teilprojekt_set.all()) == 0:
                            self.assertTrue(
                                len(
                                currentTableModel.objects.filter(**stateDict)
                                ) == lengthOfQuerySet,
                                assertationMessage,
                            )
                elif str(currentTableModel) == "<class 'project_listing.models.ModuleAssignment'>":
                    moduleQuery = currentTableModel.objects.filter(**stateDict)
                    if len(moduleQuery) > 0:
                        modulObj = moduleQuery[0]
                        if len(modulObj.subproject_set.all()) == 0:
                            self.assertTrue(
                                len(
                                currentTableModel.objects.filter(**stateDict)
                                ) == lengthOfQuerySet,
                                assertationMessage,
                            )                   
                else:
                    try:
                        self.assertTrue(
                            len(
                            currentTableModel.objects.filter(**stateDict)
                            ) == lengthOfQuerySet,
                            assertationMessage,
                        )
                    except:
                        pdb.set_trace()


            elif (
                ("Keyword" in str(currentTableModel) 
                and not "KeywordRegisterFirstReview" in str(currentTableModel)) 
                and lengthOfQuerySet == 0 
                and schlagwortregisterIDcurrent is not None
            ):
                tagToBeChecked = stateDict["schlagwort_id"]
                for numberPosition in range(1, 7):
                    dictCurrTagNum = {
                        f"schlagwort_{numberPosition}_id": tagToBeChecked
                    }
                    queryForCurrTag = KeywordRegisterFirstReview\
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
        if not os.path.exists("testFiles"):
            os.mkdir("testFiles")
        #os.chdir("testFiles")
        fileContents = os.listdir(path="testFiles/")
        newest = 0
        newestFileName = ""
        for currentFilename in fileContents:
            if ".yaml" in currentFilename:
                fileWithoutExtension = currentFilename[0:-5]

                if int(fileWithoutExtension) > newest:
                    newest = int(fileWithoutExtension)
                    newestFileName = currentFilename
        
        return os.path.join("testFiles/", newestFileName)

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
        modelsKeywords = importlib.import_module("keywords.models")
        allAttrOfModels = dir(allModels) + dir(modelsKeywords)
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
    
class TestDatabaseConcistency(TransactionTestCase):
    """
    
    """

    def testIfLastYAMLFileRepresentsDatabaseState(self):
        """Test checks, if DB-state specified by .YAML-file represents DB.

        This method checks if the user-edited-.YAML-file represents the
        state in the Database. Before execution, the filename variable
        needs to be set to the name of the .yaml-file. 
        
        """

        filename = "1683640522_edited.yaml"
        listOfDBDiffObjs = self._loadYAMLFile(filename, True)
        for currDBDiff in listOfDBDiffObjs:

            dictOfDiff = currDBDiff.differencesSortedByTable
            for tableNameInDiffStruct in list(dictOfDiff.keys()):
                if "Teilprojekt" in tableNameInDiffStruct:
                    foreignRelationFromTeilprojekt = tableNameInDiffStruct.split(".")[1]
                    fullKeyStr = tableNameInDiffStruct

            if currDBDiff.keepCurrentState and not currDBDiff.keepPendingState:
                currOrPendingStr = "currentState"
            elif currDBDiff.keepPendingState and not currDBDiff.keepCurrentState:
                currOrPendingStr = "pendingState"
            else:
                self.assertTrue(False, "User-defined kepdCurrent and keepPending Attributes are not consistent!")
                continue
            
            #pdb.set_trace()
            modelClassName = getattr(
                Subproject, 
                foreignRelationFromTeilprojekt,
            ).field.related_model

            foreignObjToPartProject = modelClassName.objects.filter(
                **dictOfDiff[fullKeyStr][currOrPendingStr]
            )[0]  

            filterDict = {
                **currDBDiff.identifer, 
                foreignRelationFromTeilprojekt: foreignObjToPartProject,
            }

            self.assertEqual(len(Subproject.objects.filter(**filterDict)), 1)

    def testIfNotUsedTupleWereDeleted(self):
        """Checks, if Tuple are present, which are not connected to Teilprojekt.

        This method checks if Enargus-, ModuleAssignment-, or 
        KeywordRegisterFirstReview-Tuples are present in the database,
        which are not conntected via ForeignKey-Relations to a 
        Teilprojekt-Tuple. That can happen, when after executing the user
        defined DB changes, the other dataset, which is set to be discarded,
        is not discarded by the system.
        """
        
        listOfSchlagwoerterTuplesTrash = []
        listOfModuleTuplesTrash = []
        listOfEnargusTupleTrash = []

        queryOfAllSchlagwoertregisterTuples = KeywordRegisterFirstReview.objects.all()
        for schlagwortregisterTuple in queryOfAllSchlagwoertregisterTuples:
            if len(schlagwortregisterTuple.teilprojekt_set.all()) == 0:
                listOfSchlagwoerterTuplesTrash.append(schlagwortregisterTuple)
        self.assertEqual(
            len(listOfSchlagwoerterTuplesTrash),
            0,
        )

        queryOfAllModulZuordnungTuples = ModuleAssignment.objects.all()
        for modulTuple in queryOfAllModulZuordnungTuples:
            if len(modulTuple.teilprojekt_set.all()) == 0:
                listOfModuleTuplesTrash.append(modulTuple)
        self.assertEqual(
            len(listOfModuleTuplesTrash),
            0,
        )

        allEnargusTuples = Enargus.objects.all()
        for enargusTuple in allEnargusTuples:
            try:
                enargusTuple.teilprojekt
            except:
                listOfEnargusTupleTrash.append(enargusTuple)
        self.assertEqual(len(listOfEnargusTupleTrash), 0)

    def _loadYAMLFile(self, filename, onlyLoadObjWithSetKeepAttr=False):
        """Helper-Function to load the .YAML-File.
        
        """
        listOfDBDiffs = []
        with open(filename, "r") as file:
            for element in yaml.load_all(file, Loader=yaml.Loader):
                element.postprocessAfterReadIn()
                if onlyLoadObjWithSetKeepAttr:
                    if (element.keepCurrentState is not None 
                        and element.keepPendingState is not None
                    ):
                        listOfDBDiffs.append(element)    
                else:
                    listOfDBDiffs.append(element)
        return listOfDBDiffs
            
