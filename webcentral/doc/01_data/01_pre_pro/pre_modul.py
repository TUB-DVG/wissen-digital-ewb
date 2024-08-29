"""
    File name: pre_modul.py
    Author: Falk Cudok
    Date created: 2022-02-16
    Date last modified:
    Python Version: 3.9
    Description: This file is a script for reading the "Modul Zuordnung"
                 from YYYYMMDD_Verteiler_EWB_Projekte.xlsx to an csv file for later
                 load into the data base of webcentral.
   Virtual Env: data preprocessing, see requirement_pre.txt
   Use own lib: dvg_lib/ProjektListe
"""

#!/usr/bin/env python
import os
import sys

relativePathToScript, filenameofScript = os.path.split(sys.argv[0])
absolutePathToScript = os.getcwd() + "/" + relativePathToScript
parentDirectory = os.path.dirname(absolutePathToScript)
sys.path.insert(0, parentDirectory)


import pandas as pd

sys.path.insert(0, "..")
from evaluation import EvaluationUtils

if len(sys.argv) != 3:
    print(
        "Preprocessing script for modul data: Usage: python pre_modul.py <source xlsx-file> <target csv-file>"
    )
    print("Hint: Use the run-script to execute this script.")
    exit

pathExcel = "/" + sys.argv[1]
targetCsvFile = "/" + sys.argv[2]

dataframeXLSX = pd.read_excel(
    pathExcel,
    sheet_name="Projektverteiler",
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

dataframeModul["modulzuordnung_ptj_1"] = dataframeModul[
    "modulzuordnung_ptj_1"
].str.lstrip()
dataframeModul["modulzuordnung_ptj_2"] = dataframeModul[
    "modulzuordnung_ptj_2"
].str.lstrip()
dataframeModul["modulzuordnung_ptj_3"] = dataframeModul[
    "modulzuordnung_ptj_3"
].str.lstrip()
dataframeModul["modulzuordnung_ptj_4"] = dataframeModul[
    "modulzuordnung_ptj_4"
].str.lstrip()


dataframeModul["modulzuordnung_ptj_2"] = dataframeModul[
    "modulzuordnung_ptj_2"
].str.replace("M2 BF", "M2")
dataframeModul["modulzuordnung_ptj_1"] = dataframeModul[
    "modulzuordnung_ptj_1"
].str.replace("ausgelaufen", "ag")

EvaluationUtils.writeDataframe2CSV(
    dataframeModul,
    targetCsvFile,
    new=True,
)
