"""iodule of Helper-Functions for the Preprocessing of XML-Files to CSV.

This module provides the `EvaluationUtils`-class, which wraps helper-
functions for the Conversion between different textformats like 
(.xml, .xlsx, or .csv). This class is used in the `pre_module.py` and
the `pre_enargus.py` file at `01_prePro`-directory. 
To use the methods inside the `EvaluationUtils`-class, it first has to be
instanciated. That can be done via
```
    import evaluation
    evaluationUtilsObj = evaluation.EvaluationUtils()
```  
The methods can then be used via
```
    evaluationUtilsObj.writeDataframe2CSV()
```
"""

import csv
from textwrap import wrap
import os
import xml.etree.ElementTree as et

import pandas as pd


class EvaluationUtils:
    """Wrapper for all helper-functions for Evaluation

    This class acts as a wrapper for helper-functions needed in the
    `pre_module.py` and `pre_enargus.py`.

    """

    @staticmethod
    def readCSV2Dataframe(
        filePath: str,
        seperator: str = ",",
    ) -> pd.DataFrame:
        """Reads CSV-File into Pandas-Dataframe.

        This Method reads a CSV-file into a Pandas-Dataframe by calling
        the pandas `read_csv`-method. As arguments, it 2 string-
        variables: The variable `filePath` specifies the path to the
        csv-file, while `seperator` specifies the delimiter inside the
        csv-file.

        Parameters
        ----------
        filePath:   str
            String, holds the path and filename to the csv-file.
        seperator:  str
            String, holdinf the delimiter character inside the csv-
            file.

        Returns
        -------
        pd.Dataframe
            Dataframe-Object, which is created by the `read_csv`-
            pandas-method.
        """
        return pd.read_csv(filePath, sep=seperator)

    @staticmethod
    def readXLSX(
        filePath: str,
        sheet: str = "Sheet1",
    ) -> pd.DataFrame:
        """Reads spreadsheet into pandas-Dataframe Object.

        This Method reads from a .xlsx-file, which the the path
        and filename specified in `filePath` the sheet with the
        name `sheet` into a pandas-Dataframe object and returns it.

        Parameters
        ----------
        filePath:   str
            Path to the .xlsx-file, including the filename.
        sheet:  str
            String, which specifies the Name of the sheet, to
            be exported.

        Returns
        -------
        pd.DataFrame
        """
        return pd.read_excel(filePath, sheet_name=sheet, engine="openpyxl")

    @staticmethod
    def writeDataframe2CSV(
        dataframe: pd.DataFrame,
        csvFilename: str,
        new: bool = False,
        anon: bool = True,
    ) -> None:
        """Writes pandas DataFrame into .csv-file

        This method writes a pandas DataFrame `dataframe` to a csv-file
        which name is specified in `csvFilename`. The parameter `new`
        controls if a new .csv-file is creted or the data is appended
        to the existing file `csvFilename`.
        The delimiter in the .csv is set as `;`

        Parameters
        ----------
        dataframe:  pd.DataFrame
            pandas Dataframe, which is written to `csvFilename`.
        csvFilename:    str
            String, which olds the name of the .csv-file to which
            `dataframe` is written.
        new:    bool
            Optional parameter, which specifies if a new file `csvFilename`
            is created or if `csvFilename` is appended to an existing
            file.

        Returns
        -------
        None
        """
        if anon:
            dataframe = EvaluationUtils._anonymizeDataframe(dataframe)

        if new:
            dataframe.to_csv(csvFilename, index=False, sep=";")
            print("new file was written: %s" % csvFilename)
        else:
            dataframe.to_csv(
                csvFilename,
                index=False,
                sep=";",
                header=False,
                mode="a",
            )
            print("data was attached to: %s" % csvFilename)

    @staticmethod
    def readDictXML2CSV(pathToFile: str) -> dict:
        """Reads in parameter-file, which holds mapping csv <-> enargus.xml

        This method reads in the parameter file `pathToFile`, which holds
        the mapping betwwen the .csv-columns names and the EnArgus.xml-
        file.

        Parameters
        ----------
        pathToFile: str
            path with filename of the parameter-file, which holds the
            mapping.

        Returns
        -------
            dict
        dict, which contains the mapping between the csv.-columns and
        the enargus.xml.
        """
        with open(pathToFile, newline="") as f:
            reader = csv.reader(f)
            dict = {}
            lineNumber = 0
            for row in reader:
                if lineNumber == 0:
                    pass
                else:
                    dict[row[0]] = row[1]
                lineNumber += 1
        return dict

    @staticmethod
    def _anonymizeDataframe(dataframe):
        """Anonymize read in Dataframe.

        This method anonyimzes the personal data in the read in xml-file
        to a default dataset.

        Parameters
        ----------
        dataframe: pd.Dataframe
            the data read in from the xml-file.

        Returns
        -------
        pd.Dataframe
            The Dataframe with the default dataset.
        """
        for index, row in dataframe.iterrows():
            row["Person_pl"] = "Robin Schmidt"
            row["Titel_pl"] = None
            row["Vorname_pl"] = "Robin"
            row["Name_pl"] = "Schmidt"
            row["Email_pl"] = "Robin.Schmidt@email.de"

        return dataframe

    @staticmethod
    def readGivenColumnsFromCSV(pathToFile: str) -> list:
        """Reads columns from `pathToFile` csv-file.

        This method reads in the columns-names from `pathToFile` csv-file
        and returns them as a list of strings.

        Parameters
        ----------
        pathToFile: str
            path, including the filename, to the csv-file whose column-
            names should be read into a list.

        Returns
        -------
            list
            list of column-names of `pathToFile` csv-file.
        """
        with open(pathToFile, newline="") as f:
            reader = csv.reader(f)
            liste = []
            for row in reader:
                liste.append(row[0])
        return liste

    @staticmethod
    def readXML(
        pathToFile: str,
        columnDict: dict,
        columns: list,
        namespaces: dict = None,
    ) -> pd.DataFrame:
        """Reads xml-file into pandas DataFrame

        This method reads the `pathToFile` xml-file into a pandas
        DataFrame-object and returns it. For that it needs `columnDict`,
        which is a mapping between the column-names and the xml-elements.
        `columns` is also needed, which is a list of the csv-column names.
        It has to fit the names of `columnDict`.

        Parameters
        ----------
        pathToFile: str
            path and filename of the .xml-file, which should be imported
            as pandas DataFrame.
        columnDict: dict
            Dictionary, which holds the mapping between the columns names
            and the xml-elements.
        columns:    list
            list of the column-names. has to match, with `columnDict`.
        namesspaces:    dict
            Dictionary, which holds the xml-Namespaces.

        Returns
        -------
            pd.DataFrame
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

    @staticmethod
    def readXMLEnargus(
        path2xml: str,
        pathDictXML2CSV: dict,
        pathListColumns: list,
    ) -> pd.DataFrame:
        """Reads xml-file into pandas DataFrame

        This method reads the data inside `path2xml`-file into a pandas
        Dataframe and returns it. Therefore it uses the `pathDictXML2CSV`
        dictionary, which holds the mapping from xml-elements to csv-
        column names and the `pathListColumns`, which holds the column-
        names of the csv-file.

        Parameters
        ----------
        path2xml:   str
            Path and filename of the xml-file, which should be read into
            a pandas DataFrame.
        pathDictXML2CSV:    dict
            Dictionary, holding Mapping between xml and csv.
        pathListColumns:    list
            List of column names.

        Returns
        --------
            pd.DataFrame
        """
        namenspacesEnargus = {
            "": "http://www.enargus.de/elements/0.1/begleitforschung/",
            "bscw": "http://bscw.de/bscw/elements/0.1/",
        }
        dictXML2CSV = EvaluationUtils.readDictXML2CSV(pathDictXML2CSV)
        listColumns = EvaluationUtils.readGivenColumnsFromCSV(pathListColumns)
        return EvaluationUtils.readXML(
            path2xml,
            dictXML2CSV,
            listColumns,
            namespaces=namenspacesEnargus,
        )
