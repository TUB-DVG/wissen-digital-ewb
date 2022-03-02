'''
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
'''
#!/usr/bin/env python
import os
import sys
# adapt actual working directory (for fix the relative depenencies)
os.chdir('/home/cudok/Documents/GitHub/webcentral/02_work_doc/01_daten/01_prePro/')

# load own lib
path_modules = os.path.join(
    '../../../../dvg_lib/ProjektListe')  # link to the folder including
                                         # the lib file auswertung.py
sys.path.append(path_modules)
import auswertung as asw

import pandas as pd

path_excel = '../../../../../../Nextcloud/Shared/WenDE/12_Daten/03_Gesamt_BF_Daten/20220207_Verteiler_EWB_Projekte.xlsx'
df_xlsx = pd.read_excel(path_excel, sheet_name='Projektverteiler', dtype="str")

df_modul = df_xlsx[["Förderkenz. (0010)", "Modulzuordnung PtJ - 1 aktuell"
                    , "Modulzuordnung PtJ - 2 aktuell", "Modulzuordnung PtJ - 3 aktuell"
                    , "Modulzuordnung PtJ - 4 aktuell"]]
# rename columns
df_modul = df_modul.rename(columns={"Förderkenz. (0010)": "FKZ",
                                     "Modulzuordnung PtJ - 1 aktuell" : 'modulzuordnung_ptj_1',
                                     "Modulzuordnung PtJ - 2 aktuell" : 'modulzuordnung_ptj_2',
                                     "Modulzuordnung PtJ - 3 aktuell" : 'modulzuordnung_ptj_3',
                                     "Modulzuordnung PtJ - 4 aktuell" : 'modulzuordnung_ptj_4'
                    })
# clean up , dirty, could be done nicer
# see https://stackoverflow.com/questions/41476150/removing-space-from-columns-in-pandas
df_modul['modulzuordnung_ptj_1'] = df_modul['modulzuordnung_ptj_1'].str.lstrip()
df_modul['modulzuordnung_ptj_2'] = df_modul['modulzuordnung_ptj_2'].str.lstrip()
df_modul['modulzuordnung_ptj_3'] = df_modul['modulzuordnung_ptj_3'].str.lstrip()
df_modul['modulzuordnung_ptj_4'] = df_modul['modulzuordnung_ptj_4'].str.lstrip()


df_modul['modulzuordnung_ptj_2'] = df_modul['modulzuordnung_ptj_2'].str.replace('M2 BF', 'M2')
df_modul['modulzuordnung_ptj_1'] = df_modul['modulzuordnung_ptj_1'].str.replace('ausgelaufen', 'ag')

asw.write_df2csv(df_modul, 'modulzuordnung_csv_20220225.csv', new=True)
