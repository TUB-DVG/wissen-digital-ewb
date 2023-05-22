"""Unittest for the evaluation.py

This class tests the evaluation.py with the unittest-framework. The 
Testcase is called via the commandline, by specifying the relative-path
to the "01_daten"-folder. An execution could look as follows:
```
    python3 testPrePro.py ../../01_daten/
```
The testcase basically tests, if the output of the .csv-files is the
same, when called with the `evaluation.py` and the `auswertung.py`.
That means, that the old `auswertung.py` needs still be present on 
the local machine to run the testcases 
`testCheckIfCSVAreTheSameAsWithAuswertung` and 
`testCheckIfCSVAreTheSameAsWithAuswertung`. The path to the the
`auswertung.py` needs to be set in the `__init__`-method.
"""
import csv
from filecmp import (
    cmp,
)
import os.path
import sys
import unittest


from pandas import (
    DataFrame,
    read_excel,
)

class TestPreModule(unittest.TestCase):
    """Class to test the preprocessing

    This class inherits from unittest.TestCase. It tests the preprocessing
    -chain, in which a .xml/.xlsx-file is written as .csv-file, which can then
    be read into the database.
    """
    def setUp(self) -> None:
        """setUp of TestPreModule.

        This method setts the attributes of `TestProModule`. It is called 
        before every-testmethods execution.
        
        Parameters
        ----------

        Returns
        -------
        None
        """
        self.pathToAuswertungPy = "../../../dvg_lib/ProjektListe/"
        self.pathExcelModul = "../../../../../../Nextcloud/Shared/05_Degner/20230403_Verteiler_EWB_Projekte.xlsx"
        self.pathXMLEnargus = "../../../../../../Nextcloud/Shared/01_Enargus/Daten_von_Bosch_2023_02_24/2023-02-24_enargus.xml"

    def testdWriteOut(self) -> None:
        """

        This method first creates an empty dataset and hands it to the
        `writeDataframe2CSV`. It is then tested, if a .csv-file is 
        created from an empty Dataframe.
        After that, a Dataframe is created from a dictionary. The keys
        of the dictionary, containing the header-names of the later
        .csv-file.
        The created Dataframe is then written with the 
        `writeDataframe2CSV` to a .csv-file. It is tested, if the 
        .csv-file exists and if it contains one data-row, and 5 
        header-columns.
        Lastly, the `writeDataframe2CSV` is called in append mode.
        It is then tested, if the .csv-file now contains 2 rows.

        Parameters
        ----------

        Returns
        -------
        None
        """
        dataframe = DataFrame()

        EvaluationUtils.writeDataframe2CSV(
            dataframe, 
            "testWriteCSV.csv", 
            new=True,
        )

        checkIfCSVWasCreated = os.path.isfile("testWriteCSV.csv")

        self.assertTrue(
            checkIfCSVWasCreated, 
            "CSV-file was not created from empty pandas DataFrame!",
        )

        dictToBeFilledIntoCSVFile = {
            "Förderkenz. (0010)": ["03EN1032D"],
            "Modulzuordnung PtJ - 1 aktuell": ["M2"],
            "Modulzuordnung PtJ - 2 aktuell": ["M1"],
            "Modulzuordnung PtJ - 3 aktuell": [""],
            "Modulzuordnung PtJ - 4 aktuell": [""],              
        }

        dataframeFromDict = DataFrame(data=dictToBeFilledIntoCSVFile)

        
        EvaluationUtils.writeDataframe2CSV(
            dataframeFromDict, 
            "testWriteCSV.csv", 
            new=True,
        )   
        
        self.assertTrue(
            os.path.isfile("testWriteCSV.csv"), 
            "testCSV-file does not exist, when filled with Dictionary!",
        )

        with open("testWriteCSV.csv", "r") as testFile:
            readerObj = csv.reader(testFile, delimiter=";")
            lineNumber = 0
            headers = []
            data = []
            for row in readerObj:
                if lineNumber == 0:
                    headers = row
                else:
                    data.append(row)
                lineNumber += 1
            
            self.assertEqual(
                len(data), 
                1, 
                "csv-file contains more than one data-row! But only one data-row was specified in the the dictionary!",
            )
            self.assertEqual(
                len(headers), 
                5, 
                "Number of Header-fields does not match Dictionary keynumber!",
            )

        EvaluationUtils.writeDataframe2CSV(
            dataframeFromDict, 
            "testWriteCSV.csv", 
            new=False,
        )  

        with open("testWriteCSV.csv", "r") as testFile:
            readerObj = csv.reader(testFile, delimiter=";")
            lineNumber = 0
            headers = []
            data = []
            for row in readerObj:
                if lineNumber == 0:
                    headers = row
                else:
                    data.append(row)
                lineNumber += 1
        self.assertEqual(
            len(data), 
            2, 
            "After execution of writeDataframe2CSV in append mode, number of data-rows should be two!",
        )
    
    def testReadDictXML2CSV(self) -> None:
        """Tests `readDictXML2CSV` from `EvaluationUtils`

        This method tests the static-method from the `EvaluationUtils`-
        class inside the `evaluation.py`. The method reads in a 
        parameter-file in which the mapping between the .csv-columns 
        and thte xml-elements is placed.

        Parameters
        ----------

        Returns
        -------
        None
        """

        returnDict = EvaluationUtils.readDictXML2CSV(
            "02_parameter_files/col_dict_xml2csv.csv",
        )

        hardCodedResultDict = {
            'FKZ': 'fkz', 
            'Datenbank': 'db', 
            'Laufzeitbeginn': 'fi_von/iso8601', 
            'Laufzeitende': 'fi_ende/iso8601', 
            'Thema': 'v_thema', 
            'Foerdersumme_EUR': 'fi_sumbew/value', 
            'Verbundbezeichung': 'ver_bez', 
            'Leistungsplan_Sys_Nr': 'lp_nr', 
            'Leistungsplan_Sys_Text': 'lp_text', 
            'Name_AS': 'name_st', 
            'PLZ_AS': 'plz_strasse_st', 
            'Ort_AS': 'ort_st', 
            'Adress_AS': 'ad_str_st', 
            'Land_AS': 'land_st', 
            'Gemeindekennziffer_AS': 'gem_gemkz_st', 
            'Name_ZWE': 'name_ze', 
            'PLZ_ZWE': 'plz_strasse_ze', 
            'Ort_ZWE': 'ort_ze', 
            'Adress_ZWE': 'ad_str_ze', 
            'Land_ZWE': 'land_ze', 
            'Gemeindekennziffer_ZWE': 'gem_gemkz_ze', 
            'Bundesministerium': 'v_ressort', 
            'Projekttraeger': 'v_pt_detail', 
            'Forschungsprogramm': 'v_forschsp_text', 
            'Foerderprogramm': 'v_prog_text', 
            'Kurzbeschreibung_de': 'auf_bez_pub', 
            'Kurzbeschr_de_quelle': 'auf_bez_pub_quelle', 
            'Kurzbeschreibung_en': 'auf_bez_pub_en', 
            'Kurzbeschr_en_quelle': 'auf_bez_pub_quelle_en', 
            'Person_pl': 'pers_pl', 
            'Titel_pl': 'pers_titel_pl', 
            'Vorname_pl': 'pers_vname_pl', 
            'Name_pl': 'pers_name_pl', 
            'Email_pl': 'pers_email_pl'
        }

        self.assertTrue(
            returnDict == hardCodedResultDict,
            "returned Dictionary from readDictXML2CSV is not equal to hard coded dictionary! Are there changes in the parameter file?",
        )

    def testReadGivenColumnsFromCSV(self) -> None:
        """Tests the `readGivenColumnsFromCSV` method

        This method tests the `readGivenColumnsFromCSV` staticmethod
        inside of `EvaluationUtils`-class. Because 
        `readGivenColumnsFromCSV` just reads a static list, the
        returned list is compared to a hard-coded list inside of
        `testReadGivenColumnsFromCSV`. The use of this testmethod 
        should be discussed. It can just detect unwanted changes in 
        the parameter-files, which can lead to errors. 

        Parameters
        ----------

        Returns
        -------
        None
        """

        returnedList = EvaluationUtils.readGivenColumnsFromCSV(
            "02_parameter_files/col_xml2csv.csv",
        )

        hardCodedList = [
            'FKZ', 
            'Laufzeitbeginn', 
            'Laufzeitende', 
            'Datenbank', 
            'Thema', 
            'Foerdersumme_EUR', 
            'Verbundbezeichung', 
            'Leistungsplan_Sys_Nr', 
            'Leistungsplan_Sys_Text', 
            'Name_ZWE', 
            'PLZ_ZWE', 
            'Ort_ZWE', 
            'Adress_ZWE', 
            'Land_ZWE', 
            'Bundesministerium', 
            'Projekttraeger', 
            'Forschungsprogramm', 
            'Foerderprogramm', 
            'Kurzbeschreibung_de', 
            'Kurzbeschreibung_en', 
            'Person_pl', 
            'Titel_pl', 
            'Vorname_pl', 
            'Name_pl', 
            'Email_pl', 
            'Name_AS', 
            'PLZ_AS', 
            'Ort_AS', 
            'Adress_AS', 
            'Land_AS',
        ]

        self.assertTrue(
            returnedList == hardCodedList,
            "Returned List of readGivenColumnsFromCSV doesnt match hardcoded list. Did you change the parameterfile 01_prePro/02_parameter_files/col_xml2csv.csv?"
        )


    def testCheckIfCSVAreTheSameAsWithAuswertung(self) -> None:
        """Tests, if `evaluation` and `auswertung` produce same output.

        This method checks, if `evalution.py`, which is a refactored 
        version of `auswertung.py` produces the same contents in the 
        .csv-files. Therefore the content of the `pre_modul.py` is 
        placed here to load the `20230403_Verteiler_EWB_Projekte.xlsx`.
        The path to the .xlsx file is saved inside the 
        `self.pathExcelModul` and needs to be modified before execution.
        The .csv-file is then produced with the old `auswertung.py`
        and the new `evaluation.py` and the contents of the two files
        compared.
        The same procedure is repeated with the EnargusXML-file.

        Parameters
        ----------

        Returns
        -------
        None
        """

        

        if not os.path.isfile(self.pathToAuswertungPy + "auswertung.py"):
            self.assertTrue(
                False, 
                "Please set the path to auswertung.py in testCheckIfCSVAreTheSameAsWithAuswertung!",
            )
            return

        sys.path.insert(0, self.pathToAuswertungPy)
        import auswertung as asw

        os.chdir(
            '/home/tobias/Aufgaben/07_dockerWithDB/webcentral/02_work_doc/01_daten/01_prePro'
        )

        dataframeXLSX = read_excel(
            self.pathExcelModul, 
            sheet_name='Projektverteiler', 
            dtype="str",
        )

        dataframeModul = dataframeXLSX[
            [
                "Förderkenz. (0010)", 
                "Modulzuordnung PtJ - 1 aktuell",
                "Modulzuordnung PtJ - 2 aktuell", 
                "Modulzuordnung PtJ - 3 aktuell",
                "Modulzuordnung PtJ - 4 aktuell",
            ]
        ]
        dataframeModul = dataframeModul.rename(
            columns={
                "Förderkenz. (0010)": "FKZ",
                "Modulzuordnung PtJ - 1 aktuell": "modulzuordnung_ptj_1",
                "Modulzuordnung PtJ - 2 aktuell": "modulzuordnung_ptj_2",
                "Modulzuordnung PtJ - 3 aktuell": "modulzuordnung_ptj_3",
                "Modulzuordnung PtJ - 4 aktuell": "modulzuordnung_ptj_4",
            }
        )

        dataframeModul['modulzuordnung_ptj_1'] = dataframeModul[
            'modulzuordnung_ptj_1'
        ].str.lstrip()
        dataframeModul['modulzuordnung_ptj_2'] = dataframeModul[
            'modulzuordnung_ptj_2'
        ].str.lstrip()
        dataframeModul['modulzuordnung_ptj_3'] = dataframeModul[
            'modulzuordnung_ptj_3'
        ].str.lstrip()
        dataframeModul['modulzuordnung_ptj_4'] = dataframeModul[
            'modulzuordnung_ptj_4'
        ].str.lstrip()


        dataframeModul['modulzuordnung_ptj_2'] = dataframeModul[
            'modulzuordnung_ptj_2'
        ].str.replace('M2 BF', 'M2')
        dataframeModul['modulzuordnung_ptj_1'] = dataframeModul[
            'modulzuordnung_ptj_1'
        ].str.replace('ausgelaufen', 'ag')

        asw.write_df2csv(
            dataframeModul, 
            "modulzuordnungOldAuswertung.csv", 
            new=True,
        )

        EvaluationUtils.writeDataframe2CSV(
            dataframeModul,
            "modulzuordnungNewEvaluation.csv",
            new=True,
        )

        self.assertTrue(
            cmp(
                "modulzuordnungOldAuswertung.csv",
                "modulzuordnungNewEvaluation.csv",
                False,
            ),
            "File-contents from the .csv-files produced by evaluation and auswertung differ!",
        )

        listCol = '02_parameter_files/col_xml2csv.csv'
        xml2csv = '02_parameter_files/col_dict_xml2csv.csv'
        
        dataframeFromAuswertung = asw.read_xml_enargus(
            self.pathXMLEnargus, 
            xml2csv, 
            listCol
        )

        asw.write_df2csv(
            dataframeFromAuswertung, 
            "enargusOldAuswertung.csv", 
            new=True,
        )

        dataframeFromEvaluationModule = EvaluationUtils.readXMLEnargus(
            self.pathXMLEnargus, 
            xml2csv, 
            listCol,
        )
        EvaluationUtils.writeDataframe2CSV(
            dataframeFromEvaluationModule,
            "enargusNewEvaluation.csv",
            new=True,
        )

        self.assertTrue(
            cmp(
                "enargusOldAuswertung.csv",
                "enargusNewEvaluation.csv",
                False,
            ),
            "File-contents from the .csv-files produced by evaluation and auswertung differ (For Enargus)!",
        )

    
    @classmethod
    def tearDownClass(cls) -> None:
        """Method, which is called after all tests are executed.

        This method is called after all Tests of `TestPreModul` were
        executed. It then deletes all created test-.csv-files. Since 
        this method is a static-class method and not a instance-method,
        it does not get the `self`-attribute. Its not mandatory, but a
        coding style. See [1] for more information.

        Parameters
        ----------

        Returns
        -------
        None

        References
        ----------
        [1] https://peps.python.org/pep-0008/#function-and-method-arguments
        """
        os.remove("enargusNewEvaluation.csv")
        os.remove("enargusOldAuswertung.csv")
        os.remove("modulzuordnungNewEvaluation.csv")
        os.remove("modulzuordnungOldAuswertung.csv")
        os.remove("testWriteCSV.csv")

if __name__ == "__main__":
    os.chdir(sys.argv[1])
    sys.path.insert(0, os.getcwd())
    from evaluation import EvaluationUtils
    unittest.main(argv=['first-arg-is-ignored'], exit=False)