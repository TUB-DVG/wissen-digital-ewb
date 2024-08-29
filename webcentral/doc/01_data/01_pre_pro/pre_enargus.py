"""
    File name: pre_enargus.py
    Author: Falk Cudok
    Date created: 2022-02-16
    Date last modified:
    Python Version: 3.9
    Description: This file is a script for preprocessing the data
                 from enargus xml file to an csv file for later
                 load into the data base of webcentral.
   Virtual Env: data preprocessing, see requirement_pre.txt
   Use own lib: dvg_lib/ProjektListe
"""

import os
import sys

relativePathToScript, filenameofScript = os.path.split(sys.argv[0])
absolutePathToScript = os.getcwd() + "/" + relativePathToScript
parentDirectory = os.path.dirname(absolutePathToScript)
sys.path.insert(0, parentDirectory)

from evaluation import EvaluationUtils

listCol = absolutePathToScript + "/" + "02_parameter_files/col_xml2csv.csv"
xml2csv = absolutePathToScript + "/" + "02_parameter_files/col_dict_xml2csv.csv"

if len(sys.argv) != 3:
    print(
        "Preprocessing script for enargus data: Usage: python pre_enargus.py <source xml-file> <target csv-file>"
    )
    print("Hint: Use the run-script to execute this script.")
    exit

pathXML = "/" + sys.argv[1]
targetCsvFile = "/" + sys.argv[2]
dataframe = EvaluationUtils.readXMLEnargus(pathXML, xml2csv, listCol)

EvaluationUtils.writeDataframe2CSV(
    dataframe,
    targetCsvFile,
    True,
    True,
)
