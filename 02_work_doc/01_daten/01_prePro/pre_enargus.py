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
#!/usr/bin/env python
import os
import sys
# adapt actual working directory (for fix the relative depenencies)
os.chdir('/home/tobias/Aufgaben/07_dockerWithDB/webcentral/02_work_doc/01_daten/01_prePro')

# load own lib
path_modules = os.path.join(
    '../../../../dvg_lib/ProjektListe/')  # link to the folder including
                                         # the lib file auswertung.py
sys.path.append(path_modules)
import auswertung as asw

# load parameter files
list_col = '02_parameter_files/col_xml2csv.csv'
xml2csv = '02_parameter_files/col_dict_xml2csv.csv'

path_xml = "../../../../../../Nextcloud/Shared/01_Enargus/Daten_von_Bosch_2023_02_24/2023-02-24_enargus.xml"
df = asw.read_xml_enargus(path_xml, xml2csv, list_col)

asw.write_df2csv(df, 'enargus_csv_20230403.csv', new=True)
