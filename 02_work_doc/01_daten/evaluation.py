### Bibliothek von python-Funktionen für die Auswertung der Projektliste
### Autoren: F. Cudok, R. Streblow
### Zeit: Januar 2021

import os
import pandas as pd
import matplotlib as plt
from matplotlib import pyplot as plt
from textwrap import wrap
from nltk import tokenize
import xml.etree.ElementTree as et
import csv

class EvaluationUtils:
    """Wrapper for all helper-functions for Evaluation

    This class acts as a wrapper for helper-functions needed in the 
    evaluation of the projectlist.
    
    """

    def readCSV2Dataframe(
            self, 
            filePath: str, 
            seperator: str=',',
    ) -> pd.DataFrame:
            """Reads CSV-File into Pandas-Dataframe.

            This Method reads a CSV-file into a Pandas-Dataframe by calling
            the pandas `read_csv`-method. As arguments, it 2 string-
            variables: The variable `filePath` specifies the path to the 
            csv-file, while `seperator` specifies the delimiter inside the 
            csv-file.

            Function Arguments:
            filePath:   str
                String, holds the path and filename to the csv-file.
            seperator:  str
                String, holdinf the delimiter character inside the csv-
                file.
            
            returns:
            pd.Dataframe
                Dataframe-Object, which is created by the `read_csv`-
                pandas-method.
            """
            return pd.read_csv(filePath, sep=seperator)

    def readXLSX(
            self,
            filePath: str, 
            sheet: str="Sheet1",
    ) -> pd.DataFrame:
            """Reads spreadsheet into pandas-Dataframe Object.

            This Method reads from a .xlsx-file, which the the path 
            and filename specified in `filePath` the sheet with the 
            name `sheet` into a pandas-Dataframe object and returns it.

            Function Arguments:
            filePath:   str
                Path to the .xlsx-file, including the filename.
            sheet:  str
                String, which specifies the Name of the sheet, to
                be exported.
            """
            return pd.read_excel(filePath, sheet_name=sheet, engine='openpyxl')

    def writeDataframe2CSV(
            self,
            dataframe: pd.DataFrame, 
            dbName: str, 
            new: bool=False,
    ) -> None:
        """Schreiben eines pandasDataFrames (df) in eine csv-Datei mit dem Trennzeichen
        ";" und ohne Index-Spalte

        input
        df: pandasDataFrame
        db_name: name der csv-Datenbank inkl. Pfad
        new: Boolean-Parameter Neuanlegen(True) / Anhängen(False)

        output
        csv-Datei in das Arbeitsverzeichnis der Python-Instanz

        """
        if new:
            dataframe.to_csv(dbName, index=False, sep=';')
            print('new file was written: %s' %dbName )
        else:
            dataframe.to_csv(
                dbName, 
                index=False, 
                sep=';', 
                header=False, 
                mode='a',
            )
            print('data was attached to: %s' %dbName )

    def readDictXML2CSV(self, pathToFile: str) -> dict:
        """Einlesen des Übersetzungsdictionaries, welches die Zuordung zwischen den
        Spaltennamen in unserer Datenbank(csv) und der EnArgus-xml enthält
        input
        Datei: Dateiname inkl. Pfad

        output
        Dictionary mit den Zuordnungen
        """
        with open(pathToFile, newline='') as f:
            reader = csv.reader(f)
            dict = {}
            i = 0
            for row in reader:
                if i== 0:
                    pass
                else:
                    dict[row[0]]=row[1]
                i = i + 1
        return dict

    def readGivenColumnsFromCSV(self, pathToFile: str):
        """Einlesen der vorgegebenen/gewünschten Spalten aus einer csv-Dateien
        input
        Datei: Dateiname inkl. Pfad

        output
        Liste mit den vorgegebenen Spalten
        """
        with open(pathToFile, newline='') as f:
            reader = csv.reader(f)
            liste = []
            for row in reader:
                liste.append(row[0])
        return liste

    def readXML(
            self, 
            pathToFile: str, 
            columnDict: dict, 
            columns: list, 
            namespaces: dict = None,
        ) -> pd.DataFrame:
        """liest xml Datei in eine pandas dataFrame eine

        file: Dateiname inkl. Pfad als String
        col_dict: Dictionary enthält die Zuordnung zwischen Spaltennamen und xml-elementen
        columns: Namen der gewünschten Spalten als Liste von Strings (die
        gewünschten Spalten müssen in dem Zuordungs-Dictionary enthalten sein)
        namespaces: namespaces aus aus der xml-Datei (als Dictionary)
        """
        rows = []

        xtree = et.parse(pathToFile)
        xroot = xtree.getroot()
        for child in xroot:
            row = {}
            for item in columns:
                if namespaces == None:
                    node = child.find(columnDict[item])
                else:
                    node = child.find(columnDict[item], namespaces)
                if node is not None:
                    strItem = node.text
                else:
                    strItem = None
                row[item] = strItem
            rows.append(row)
        return pd.DataFrame(rows, columns=columns)

    def readXMLEnargus(
            self, 
            path2xml: str, 
            pathDictXML2CSV: dict, 
            pathListColumns: list,
        ) -> pd.DataFrame:
        """reading xml-file base on:
        - Dictionary xml2csv
        - List of read columns

        returns a DataFrame
        """
        namenspacesEnargus = {
                '' : "http://www.enargus.de/elements/0.1/begleitforschung/", 
                'bscw' : "http://bscw.de/bscw/elements/0.1/",
            }
        dictXML2CSV = self.readDictXML2CSV(pathDictXML2CSV)
        listColumns = self.readGivenColumnsFromCSV(pathListColumns)
        return self.readXML(
            path2xml, 
            dictXML2CSV, 
            listColumns, 
            namespaces=namenspacesEnargus,
        )


class WriteCSV2Dataframe(object):
    """Objekt zum Hinzufügen, Erstellen und aktuallisieren der csv-Datenbank"""

    def __init__(self) -> None:
        self.evaluationUtils = EvaluationUtils()
        self.path2xml = None
        self.path2xlsx = None # alte Liste, wurde 2020 für die Zuordung der
                              # Projekte zu den Modulen von Modul 4 genutzt
        self.path2CSVDatabaseOld = None # die auszulesende DB
        self.path2CSVDatabaseNew = None # wenm die DB verändert wird, wird die neue
                                    # DB in eine neue Datei geschrieben, evtl.
                                    # später anders lösen
        self.dataframeXML = pd.DataFrame()
        self.dataframeCSVDatabase = pd.DataFrame()
        self.path2ColumnsPre = None # Datei/Pfad zur Datei, welche die
                                    # gewünschten/vorgegeben Dateinamen enthält
        self.path2dictXML2CSV = None # Datei/Pfad zur Datei, welche die
                                      # Zuordung zwischen den xml-Elemente und
                                      # dem Spaltennamen enthält
        self.listColumnsPre = []
        self.dictXML2CSV = {}
        self.dataframeXLSX = pd.DataFrame()
        self.dataframeJSON = pd.DataFrame()
        self.dataframeWrite = pd.DataFrame() # Ziel-DataFrame: hier wird alles
                                       # zusammengefügt um anschließend
                                       # geschrieben werden zu können
        # Namenspaces wurden aus der xml-Datei rausgelesen (evtl. müssen die später mal angepasst werden)
        self.namenspacesEnargus = {
            '' : "http://www.enargus.de/elements/0.1/begleitforschung/", 
            'bscw' : "http://bscw.de/bscw/elements/0.1/",
        }

    def addColumnsFromXLSX(
            self, 
            listColumns: list, 
            indexColumnsXLSX: int, 
            indexColCSV: int,
    ) -> None:
        """Fügt Spalten aus einer xlsx-Datei dem csv-Dataframe hinzufügen

        input
        list_col: Liste mit den Spaltennamen inkl. Spalte 'Förderkennzeichen'
        col_fkz: Spaltenname der Spalte, welche die Förderkennzeichen enthält

        ouptut
        keiner - fügt das zusammengeführte Dataframe mit dem DataFrame
        df_write des Objekts zusammen

        """
        self.dataframeCSVDatabase = self.dataframeCSVDatabase.set_index(
            indexColCSV,
        )
        dataframeProcessing = self.df_xlsx[listColumns]
        dataframeProcessing = dataframeProcessing.set_index(indexColumnsXLSX)
        self.dataframeWrite = pd.concat(
            [
                self.dataframeWrite,
                self.dataframeCSVDatabase, 
                dataframeProcessing,
            ], 
            axis=1,
        )
        self.dataframeWrite = self.dataframeWrite.reset_index().rename(
            columns={'index':indexColCSV},
        )

    def readCSVDatabase(self) -> None:
            """Einlesen der csv-DB in das Objekt
            """
            self.dataframeCSVDatabase = self.evaluationUtils.readCSV2Dataframe(
                self.path2CSVDatabaseOld, 
                sep=';',
            )

    def readXML(self) -> None:
        """Einlesen der xml-Datei basierend auf:
           - Dictionary xml2csv
           - Liste "gewünschte" Spalten

        wird in das DataFrame 'df_xml' des Objekts geschrieben
        """

        self.dataframeXML = self.evaluationUtils.readXML(
            self.path2xml, 
            self.dictXML2CSV, 
            self.listColumnsPre, 
            namespaces=self.namenspacesEnargus,
        )

    def dataframeXMLEqualDataframeWrite(self) -> None:
        """Setzt das aus der xml-Datei ausgelesene DataFrame ohne weitere Veränderung
        mit dem DataFrame df_write gleich

        
        """
        self.dataframeWrite = self.dataframeXML

    def writeCSV(self, new: bool=False) -> None:
        """Schreiben des zusammenstellten DataFrames in die vorgebene csv-Datei

        input
        new: Boolean
             True - neue Datei wird erzeugt
             False - Zeilen werden angefübt

        return
        Datei wird geschrieben
        """
        if new:
                self.evaluationUtils.writeDataframe2CSV(
                    self.dataframeWrite, 
                    self.path2csvDatabaseNew, 
                    new=True
                )
        else:
                self.evaluationUtils.writeDataframe2CSV(
                    self.dataframeWrite, 
                    self.path2csvDatabaseOld, 
                    new=False,
                )


    def setColumnsPreCSVFile(self, pathFile: str):
        """Übergabe des Dateinames inkl. Pfad, der Datei, welche die vorgeben, gewünschten Spalten enthält
        input
        path_file: Dateiname inkl. Pfad

        ouptut
        keiner - Dateiname wird im Objekt gespeichert
        """
        self.path2ColumnsPre = os.path.join(pathFile)

    def readColumnsPre(self):
        """Einlesen der vorgeben/gewünschten Spalten in eine Liste des Objekts

        return
        Liste der Stalten
        """

        self.listColumnsPre = self.evaluationUtils.readGivenColumnsFromCSV(
            self.path2ColumnsPre
        )
        return self.listColumnsPre

    def setDictXML2CSVFile(self, path_file):
        """Übergabe des Dateinames inkl. Pfad, der Datei, welche die Zuordnung zwischen
        xml-Elementen und Spaltennamen enthält

        input path_file: Dateiname inkl.
        Pfad

        ouptut
        keiner - Dateiname wird im Objekt gespeichert

        """
        self.path2dictXML2CSV = os.path.join(path_file)

    def readDictXML2CSV(self):
        """Einlesen des Dictionaries mit der Zuordnung zwischen
        xml-Elementen und Spaltennamen

        return
        Dictionary mit den Zuordnungen
        """

        self.dictXML2CSV = self.evaluationUtils.readDictXML2CSV(
            self.path2dictXML2CSV
        )
        return self.dictXML2CSV

    def setCSVdatabaseNewFile(self, csvDatabaseFile: str):
        """Übergabe der Dateinames der neu zuschreiben csv-db inkl. Pfad - wenn die DB
        neu erzeugt wird und nicht ein teile angefügt

        input csv_file: Dateiname
        inkl. Pfad als String

        ouptut
        keiner - Dateiname wird im Objekt gespeichert

        """
        self.path2CSVDatabaseNew = os.path.join(csvDatabaseFile)

    def setCSVDatabaseOldFile(self, csvDatabaseFile: str):
        """Übergabe der Dateinames der vorhanden csv-db inkl. Pfad
        input
        csv_file: Dateiname inkl. Pfad als String

        ouptut
        keiner - Dateiname wird im Objekt gespeichert
        """
        self.path2csvDatabaseOld = os.path.join(csvDatabaseFile)

    def setXLSXFile(self, xlsxFile: str):
        """Übergabe der Dateinames des xlsx-Datei inkl. Pfad (alte Liste Modulzuordung Modul4)
        input
        xlsx_file: Dateiname inkl. Pfad als String

        ouptut
        keiner - Dateiname wird im Objekt gespeichert
        """
        self.path2xlsx = os.path.join(xlsxFile)

    def setXMLFile(self, xmlFile: str):
        """Übergabe der Dateinames des xml-Datei inkl. Pfad
        input
        xml_file: Dateiname inkl. Pfad als String

        ouptut
        keiner - Dateiname wird im Objekt gespeichert
        """
        self.path2xml = os.path.join(xmlFile)

    def readXLSXProjectlist(self, sheet: str) -> None:
        """liest ein Spreadsheet aus der ProjektListe (xlsx-Datei) in eine pandas-DataFrame ein

        input
        sheet: Name des Spreadsheets

        return
        keiner - wird in das Objekt geschrieben

        """
        self.dataframeXLSX = self.evaluationUtils.readXLSX(
            self.path2xlsx, 
            sheet=sheet,
        )


class EvaluationProjectlist(object):
    """Enthält Vorgaben und Ergebnisse der Auswertung der ProjektListe (pl)"""

    def __init__(self):
        """
        
        """
        self.evaluationUtils = EvaluationUtils()
        self.path2pl = None
        self.dataframeProjectlist = pd.DataFrame()
        self.keywords = []

    def setProjectlist(self, path: str) -> str:
        """Pfad zur Projektliste übergeben"""
        self.path2projectlist = path
        return path

    def readXLSXProjectlist(self):
        """liest ein Spreadsheet aus der ProjektListe (xlsx-Datei) in eine pandas-DataFrame ein
        """
        self.dataframeProjectlist = self.evalulationUtils.readXLSX(
            self.path2Projectlist, 
            sheet='EWB_gesamt',
        )

    def setKeywords(self, keywords: list) -> None:
        """einlesen der Keywords
        keywords: Keywords; Liste von Strings"""
        self.keywords = keywords

    def numberProjectsKeywords(self, column: str) -> tuple:
        """Anzahl der Projekte (nicht Teilprojekte), die mind. ein Keyword in einer Spalte (column) enthalten
        column: zu untersuchende Spalte; String XXX
        return:
           1. Keywords (nach den gesucht worden ist)
           2. Anzahl der Projekte entsprechend der Keywords
        """
        projectDict = {}
        projectCount =[]
        entireProjectlist = []
        for i in range(0, len(self.keywords)):
            projectAcronym = []
            # index wo das Keyword auftritt rausschreiben
            projektindex = self.dataframeProjectlist[
                self.dataframeProjectlist[column].str.contains(
                    self.keywords[i], 
                    na=False,
                ),
            ].index

            # Akronym rauslesen (auf Basis der Indices)
            for j in range(0, len(projektindex)):
                projectAcronym.append(self.dataframeProjectlist['Akronym'][j])

            # Dopplung rausnehmen
            projectAcronym = list(set(projectAcronym))

            projectDict[self.keywords[i]] = projectAcronym

        # Anzahl der Projekte je Keyword
        for i in range (0, len(projectDict)):
            projectCount.append(len(projectDict[self.keywords[i]]))
            entireProjectlist.extend(projectDict[self.keywords[i]])
        # Anzahl der aller Projekte, welche mind. ein Keyword enthalten
        gesamtprojektliste = list(set(gesamtprojektliste))
        self.keywords.append('Gesamtprojektanzahl')
        projectCount.append(len(entireProjectlist))
        return self.keywords, projectCount

    def getIndicesKeywords(
            self, 
            keywords: list, 
            columns: list,
    ) -> list:
        """Gibt die Indices der Zeilen zurück, welche ein Keyword in den
        vorgebeben Spalten enthalten
        input:
        keywords: as list
        columns: name strings as list
        output:
        indices: as list
        """
        listOfIndices = []
        for col in columns:
            for key in keywords:
                indicies = self.dataframeProjectlist[self.dataframeprojectlist[col].str.contains(key, na=False)].index
                #print(col)
                #print(indicies)
                listOfIndices.extend(indicies)
        return sorted(set(listOfIndices))

    def dataframeByIndexColumns(
            self, 
            indices: list, 
            columns: list,
        ) -> pd.DataFrame:
        """DataFrame, welches die Spalten entsprechend der vorgebeben Indices und die
        vorgebeben Spalten enthält

        input:
        indices: as list
        columns: as list
        output
        DataFrame
        """
        return self.dataframePorjectlist[columns][
            self.dataframeProjectlist.index.isin(indices),
        ]

if __name__ == "__main__":
    # ausführen
    ## plotten Rita
    # auswert = Auswert_pl()
    # auswert.set_projectlist("../../../Nextcloud/Shared/WenDE/Gesamt_BF_Daten/Leistungsplansystematik/ZE_fuer_BF_enargus_ergaenzt_Auswahl_rst_fc.xlsx")
    # # einlesen des Spreadsheets aus der xlsx-Datei
    # auswert.read_xlsx_pl()
    # # keywords nach denen gesucht wird
    # auswert.set_keywords(['Automation', 'Hemmniss', 'maschinelles Lernen', 'KI', 'digitaler Zwilling', 'Planungstool', 'Datenschutz', 'Digitalisierung'])
    # keyword = auswert.keywords
    # # durchsuchen der Kurzbeschreibungen
    # Keywords, numbers =auswert.number_projects_keywords('Kurzbeschreibung')
    # ## plotten
    # plt.barh(Keywords, numbers, align='center', alpha=0.5)
    # plt.show()





    # ## neue Tabelle Falk
    # listOfIndex = auswert.get_indices_keywords(keywords=["BIM"],
    #                                            columns=["Schlagwort1", "Schlagwort2", "Schlagwort3",
    #                                                     "Schlagwort4", 'Schlagwort5', 'Schlagwort6',
    #                                                     'Schlagwort', 'Leistungsplansystematik'])
    # col_in_new_tabel = ['Förderkennzeichen (0010)', 'Akronym', 'Ressortkennung', 'Laufzeitbeginn',
    #                     'Laufzeitende', 'Zuwendungsempfänger', 'Kurzbeschreibung']
    # df_filtert = auswert.df_by_index_columns(listOfIndex, col_in_new_tabel)
    # df_filtert.to_excel("BIM_Schlagwort_2021-01-19.xlsx")

    # # Tabelle roadmap Vernetzung PtJ-Anfrage
    # auswert = Auswert_pl()
    # auswert.set_projectlist("../../../Nextcloud/Shared/WenDE/Gesamt_BF_Daten/Leistungsplansystematik/ZE_fuer_BF_enargus_ergaenzt_Auswahl_rst_fc.xlsx")
    # # einlesen des Spreadsheets aus der xlsx-Datei
    # auswert.read_xlsx_pl()


    # col_in_new_tabel = ['Förderkennzeichen (0010)', 'Akronym', 'Ressortkennung', 'Laufzeitbeginn',
    #                     'Laufzeitende', 'Zuwendungsempfänger','Vorname - Projektleiter',
    #                     'Name - Projektleiter', 'e-Mail', 'Kurzbeschreibung',
    #                     'Schlagwort1', 'Schlagwort2', 'Schlagwort3', 'Schlagwort4',
    #                     'Schlagwort5', 'Schlagwort6', 'Schlagwort'
    #                     ]

    # ## Digitalisierung im ländlichen Raum
    # listOfIndex = auswert.get_indices_keywords(keywords=["03EN3006", '03ET1635'],
    #                                            columns=['Förderkennzeichen (0010)'])
    # df_filtert = auswert.df_by_index_columns(listOfIndex, col_in_new_tabel)
    # df_filtert.to_excel('RoadmapProjekte_2021-01-19.xlsx', sheet_name = 'laendl_Raum')

    # ## Digitalisierung in der Fernwärme
    # listOfIndex = auswert.get_indices_keywords(keywords=["03EN3010", '03EN3012', '03ET1638',
    #                                                      '03EN3021', '03EN3017', '03ET1668',
    #                                                      '03ET1673', '03ET1624'],
    #                                            columns=['Förderkennzeichen (0010)'])
    # df_filtert = auswert.df_by_index_columns(listOfIndex, col_in_new_tabel)
    # with pd.ExcelWriter("RoadmapProjekte_2021-01-19.xlsx",
    #                     mode='a') as writer:
    #     df_filtert.to_excel(writer, sheet_name='Fernwaerme')

    # ## Reallabor-Veranstaltung: Quartiersenergiemanagementsystem
    # listOfIndex = auswert.get_indices_keywords(keywords=['03EWR020',
    #                                            '03EWR010A', '03EWR010B', '03EWR010C',
    #                                            '03EWR010E', '03EWR010F', '03EWR010G',
    #                                                      '03EWR010I', '03EWR010J'],
    #                                            columns=['Förderkennzeichen (0010)'])
    # df_filtert = auswert.df_by_index_columns(listOfIndex, col_in_new_tabel)
    # with pd.ExcelWriter("RoadmapProjekte_2021-01-19.xlsx",
    #                     mode='a') as writer:
    #     df_filtert.to_excel(writer, sheet_name='RealLabore')

    # ## Thematischer Verbund Co2-Bilanzierung im Quartier
    # listOfIndex = auswert.get_indices_keywords(keywords=['03EGB0014'],
    #                                            columns=['Förderkennzeichen (0010)'])
    # df_filtert = auswert.df_by_index_columns(listOfIndex, col_in_new_tabel)
    # with pd.ExcelWriter("RoadmapProjekte_2021-01-19.xlsx",
    #                     mode='a') as writer:
    #     df_filtert.to_excel(writer, sheet_name='ThermC2Bilanz')


    # # Tabelle BIM alle Teilprojekte
    # ## FKZ aus vorher generierter Liste (siehe oben)
    # auswert = Auswert_pl()
    # auswert.set_projectlist("../../../Nextcloud/Shared/WenDE/Gesamt_BF_Daten/Leistungsplansystematik/ZE_fuer_BF_enargus_ergaenzt_Auswahl_rst_fc.xlsx")
    # # einlesen des Spreadsheets aus der xlsx-Datei
    # auswert.read_xlsx(sheet='EWB_gesamt')


    # col_in_new_tabel = ['Förderkennzeichen (0010)', 'Akronym', 'Ressortkennung', 'Laufzeitbeginn',
    #                     'Laufzeitende', 'Zuwendungsempfänger','Vorname - Projektleiter',
    #                     'Name - Projektleiter', 'e-Mail', 'Kurzbeschreibung',
    #                     'Schlagwort1', 'Schlagwort2', 'Schlagwort3', 'Schlagwort4',
    #                     'Schlagwort5', 'Schlagwort6', 'Schlagwort'
    #                     ]

    # ## Digitalisierung im ländlichen Raum
    # listOfIndex = auswert.get_indices_keywords(keywords=["03ET1466", '03ET1592', '03ET1562',
    #                                                      '03ET1413', '03ET1569', '03SBE0003',
    #                                                      '03ET1611', '03ET1603', '03SBE111',
    #                                                      '03EN1021'],
    #                                            columns=['Förderkennzeichen (0010)'])
    # df_filtert = auswert.df_by_index_columns(listOfIndex, col_in_new_tabel)
    # df_filtert.to_excel('BIM_alleTeilPro_2021-01-21.xlsx')


    # # Test Objekt write_csv_db aus xml/Enargus-Datei - direkt

    # obj_csv_db = write_csv_db()
    # # obj_csv_db.set_xml_file('./TestEnArgus.xml')
    # obj_csv_db.set_xml_file("../../../Nextcloud/Shared/Digitale_Vernetzung/Assis/Projekte/DVG0001_BMWi_Wende/01_WiMis/02_Cudok/03_projektliste/Daten_von_Roesch_2021-02-04/210204_enargusdata_last.xml")
    # # Datei, die schreiben werden soll
    # obj_csv_db.set_csv_db_new_file('./mal_sehen2.csv')
    # obj_csv_db.set_spalten_vor_csv_file('./02_Parameter_Dateien/Spalten_xml2csv.csv')
    # obj_csv_db.read_spalten_vor()
    # obj_csv_db.set_dict_xml2csv_file('./02_Parameter_Dateien/Spalten_dict_xml2csv.csv')
    # obj_csv_db.read_dict_xml2csv()
    # obj_csv_db.read_xml()
    # obj_csv_db.df_xml_equal_df_write()
    # print(obj_csv_db.df_write)
    # obj_csv_db.write_csv(new=True)

    # # Einlesen Spalten Schlagwort0-6 aus der ProjektListeLeistungssystematik
    # obj_csv_db = write_csv_db() # initalisieren Objekt
    # # obj_csv_db.set_xlsx_file('./Test_ZE_fuer_BF_enargus_ergaenzt_Auswahl_rst_fc.xlsx')
    # obj_csv_db.set_csv_db_old_file('./mal_sehen2.csv')
    # obj_csv_db.read_csv_db()
    # ## einlesen Projektliste Leistungsplansystematik - Spalten "Schlagwort0-6"
    # obj_csv_db.set_xlsx_file("../../../Nextcloud/Shared/WenDE/Gesamt_BF_Daten/Leistungsplansystematik/ZE_fuer_BF_enargus_ergaenzt_Auswahl_rst_fc.xlsx")
    # obj_csv_db.read_xlsx_pl(sheet= 'EWB_gesamt')
    # print(obj_csv_db.df_xlsx)
    # print(obj_csv_db.df_csv_db)
    # liste_spalten = ['Förderkennzeichen (0010)',
    #                  'Schlagwort1', 'Schlagwort2', 'Schlagwort3', 'Schlagwort4',
    #                  'Schlagwort5', 'Schlagwort6', 'Schlagwort'
    #                  ]
    # obj_csv_db.add_columns_from_xlsx(liste_spalten, 'Förderkennzeichen (0010)', 'FKZ')
    # # print(obj_csv_db.df_write)
    # obj_csv_db.set_csv_db_new_file('./mal_sehen3.csv')
    # obj_csv_db.write_csv(new=True)


    # obj_csv_db.set_xlsx_file("../../../Nextcloud/Shared/WenDE/Gesamt_BF_Daten/Leistungsplansystematik/20210128 ZE und Modulzuordnung für BF_FCDeleteEmptyRows.xlsx")
    # # copy von der ursprünglichen xlsx angelegt und Spalten ab 937 gelöscht, waren
    # # eigentlich leer; vor dem "Löschen" gab es eine Fehlermeldung
    # obj_csv_db.read_xlsx_pl(sheet= 'EWBProjekte gesamt')
    # liste_spalten = ['Förderkennzeichen (0010)',
    #                  'Modulvorschlag'
    #                  ]

    # obj_csv_db.add_columns_from_xlsx(liste_spalten, 'Förderkennzeichen (0010)', 'FKZ')
    # print(obj_csv_db.df_write)
    # obj_csv_db.set_csv_db_new_file('./mal_sehen4.csv')
    # obj_csv_db.write_csv(new=True)





    # Modulvorschlag


    #file = './TestEnArgus.xml'
    # xtree = et.parse(file)
    # xroot = xtree.getroot()
    # rows=[]
    # for child in xroot:
    #     # s_name = node.attrib.get("name")
    #     row = {}
    #     for item in li:
    #         print(item)
    #         if namespaces is not None:
    #             node = child.find(dic_zuo[item])
    #             if node is not None:
    #                 s_item = node.text
    #             else:
    #                 s_item = None
    #         else:
    #             s_item = node.find(dic_zuo[item], namespaces).text if node is not None else None
    #         row[item]= s_item
    #         print(row)
    #         rows.append(row)





    # Archiv - später löschen

    # test Lesen xml-Datei
    # read_xml()
    ## diesen Abschnitt als allgemeine Funktion um bauen und dann auf die xml-Projektliste anweden

    # Zuordnung der jeweiligen Spalten aus den jeweiligen QuellenDateien
    ## die Dicts würden aus einer json-Datei oder mehren csv-Dateien (mehrere, weil
    ## keine Hierarchien in einem Dokument sauber angelegt werden können)stammen
    # spalten_dict = {'Name':'name', 'email':'email', 'Note':'grade', 'PLZ':'address/PLZ', 'Alter':'age'}
    # spalten_dict = {'FKZ':'fkz', 'Datenbank':'db', 'Beginn':'fi_von/iso8601'}

    # Vorgegebene/Gewünschte Spalten
    ## kann in einer csv übergeben werden, oder auch in der einen json mit hinterlegt werden
    # spalten_vor = ['Name', 'email', 'Note', 'Alter', 'PLZ']
    # spalten_vor = ['Datenbank', 'FKZ', 'Beginn']



    # # if new:
    # #     self.df_write.to_csv(filename, index=False)
    # # else:
    # #     self.df_write.to_csv(filename, mode='a', header=False, index=False)

    # write_df2csv_db(df, './mal_sehen.csv', new=True)

    # 2021-05 EnArgus-Daten aktuallisieren

    ## einlesen csv
    obj_csv_db = write_csv_db()
    obj_csv_db.set_csv_db_old_file('../../projektliste_bf/BF_M4_DB.csv')
    obj_csv_db.read_csv_db()
    ## einlesen xml
    # # Namensraum (namespaces)
    # ## siehe https://www.w3schools.com/xml/xml_namespaces.asp
    # ## https://stackoverflow.com/questions/14853243/parsing-xml-with-namespace-in-python-via-elementtree
    # namespaces = {'':"http://www.enargus.de/elements/0.1/begleitforschung/", 'bscw':"http://bscw.de/bscw/elements/0.1/"}
    obj_csv_db.set_spalten_vor_csv_file('02_Parameter_Dateien/Spalten_xml2csv.csv')
    obj_csv_db.read_spalten_vor()
    obj_csv_db.set_dict_xml2csv_file('02_Parameter_Dateien/Spalten_dict_xml2csv.csv')
    obj_csv_db.read_dict_xml2csv()

    # df = read_xml('./TestEnArgus.xml', dic_zuo, li, namespaces= namespaces)
    obj_csv_db.set_xml_file("../../../Nextcloud/Shared/Digitale_Vernetzung/Assis/Projekte/DVG0001_BMWi_Wende/05_Daten_Quellen/Daten_von_Roesch_2021_04_27/210427_enargusdata_last.xml")
    obj_csv_db.read_xml()
    # print(df)

    ## df-csv auf die Spalten der df-xml reduzieren
    df_csv_reduziert = obj_csv_db.df_csv_db[obj_csv_db.list_spalten_vor]
    ## setze FKZ als Index
    df_csv_reduziert.set_index('FKZ', inplace = True)
    obj_csv_db.df_xml.set_index('FKZ', inplace = True)

    ## FKZ-Analyse
    idx_csv = df_csv_reduziert.index
    idx_xml = obj_csv_db.df_xml.index

    ### Gemeinsame Zeilen/FKZ herausfinden
    idx_beide = idx_xml.intersection(idx_csv)
    ### Zeilen/FKZ, die nur in  (alter) csv-df enthalten sind rausfinden
    idx_nur_csv = idx_csv.difference(idx_beide)
    ### Zeilen/FKZ, die nur in (neuer) xml-df enthalten sind rausfiden
    idx_nur_xml = idx_xml.difference(idx_beide)
    ### Ausgabe
    print('{} FKZ in beiden df'.format(idx_beide.size))
    print('{} FKZ nur in csv-df: {}'.format(idx_nur_csv.size, idx_nur_csv))
    print('{} FKZ nur in xml-df: {}'.format(idx_nur_xml.size, idx_nur_xml))
else:
    pass
