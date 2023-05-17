'''
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
'''
import os
import sys

sys.path.insert(0, '..')
from evaluation import EvaluationUtils

# adapt actual working directory (for fix the relative depenencies)
os.chdir(
    '/home/tobias/Aufgaben/07_dockerWithDB/webcentral/02_work_doc/01_daten/01_prePro'
)

# load parameter files
listCol = '02_parameter_files/col_xml2csv.csv'
xml2csv = '02_parameter_files/col_dict_xml2csv.csv'

pathXML = "../../../../../../Nextcloud/Shared/01_Enargus/Daten_von_Bosch_2023_02_24/2023-02-24_enargus.xml"

dataframe = EvaluationUtils.readXMLEnargus(pathXML, xml2csv, listCol)

EvaluationUtils.writeDataframe2CSV(
    dataframe, 
    'enargus_csv_20230403_test.csv', 
    new=True,
)
