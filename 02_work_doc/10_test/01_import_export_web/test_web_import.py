#!/usr/bin/env python3

import pandas as pd
from sqlalchemy import create_engine

# read data from the xlsx file
path_to_xlsx = 'enargus_csv_20220902_test1.xlsx'
df_xlsx = pd.read_excel(path_to_xlsx
                        ,converters={'PLZ_ZWE': lambda x: f'{x:04}'})
# print(df_xlxs)

fkz_test = ['03EWR010K', '03EWR002P', '03EWR008L', '03EWR008I']
# data from the test xlsx-file

# read data from the data base
# Create an engine instance
# remote access after config the server see [[remote_postgresql.org]
conn_string = 'postgresql://dbadmint:abc123@localhost:5432/m4_db_serv_220707'
alchemeyEngine = create_engine(conn_string)

# connect to PostgreSQL server
conn = alchemeyEngine.connect()
for fkz in fkz_test:
    # Read data from PostgreSQL database table and load into a DataFrame instance
    # test the sql code and find the specific name of the tables, use pgadmin
    query = """
   SELECT project_listing_teilprojekt.fkz,
          project_listing_enargus.thema,
          project_listing_enargus.verbundbezeichnung,
          project_listing_enargus.laufzeitbeginn,
          project_listing_enargus.laufzeitende,
          project_listing_enargus.kurzbeschreibung_de,
          project_listing_enargus.foerdersumme,
          project_listing_forschung.forschungsprogramm,
          sw_1st.schlagwort_1_id,
          sw_1.schlagwort AS schlagwort_1,
          sw_2.schlagwort AS schlagwort_2,
          sw_3.schlagwort AS schlagwort_3,
          sw_4.schlagwort AS schlagwort_4,
          sw_5.schlagwort AS schlagwort_5,
          sw_6.schlagwort AS schlagwort_6,
          sw_7.schlagwort AS schlagwort_7,
          zu_ptj.priority_1,
          zu_ptj.priority_2,
          zu_ptj.priority_3,
          zu_ptj.priority_4,
          bearbeiter.name,
          bearbeiter.vorname,
          bearbeiter.titel,
          bearbeiter.email,
          aus_stelle.name AS AusfuehrendeStelle,
    	  zwe.name as Zuwendungsempfaenger,
	      zwe_anschrift.plz AS Zwe_plz
   FROM project_listing_teilprojekt
     INNER JOIN project_listing_enargus
       ON project_listing_enargus.enargus_id = project_listing_teilprojekt.enargus_daten_id
     INNER JOIN project_listing_forschung
       ON  project_listing_forschung.forschung_id = project_listing_enargus.forschung_id
     FULL JOIN project_listing_modulen_zuordnung_ptj AS zu_ptj
       ON  zu_ptj.mod_id = project_listing_teilprojekt.zuordnung_id
     FULL JOIN schlagwoerter_schlagwortregister_erstsichtung AS sw_1st
       ON  sw_1st.schlagwortregister_id = project_listing_teilprojekt.schlagwortregister_erstsichtung_id
     FULL JOIN schlagwoerter_schlagwort AS sw_1
       ON sw_1.schlagwort_id = sw_1st.schlagwort_1_id
     FULL JOIN schlagwoerter_schlagwort AS sw_2
       ON sw_2.schlagwort_id = sw_1st.schlagwort_2_id
     FULL JOIN schlagwoerter_schlagwort AS sw_3
       ON sw_3.schlagwort_id = sw_1st.schlagwort_3_id
     FULL JOIN schlagwoerter_schlagwort AS sw_4
       ON sw_4.schlagwort_id = sw_1st.schlagwort_4_id
     FULL JOIN schlagwoerter_schlagwort AS sw_5
       ON sw_5.schlagwort_id = sw_1st.schlagwort_5_id
     FULL JOIN schlagwoerter_schlagwort AS sw_6
       ON sw_6.schlagwort_id = sw_1st.schlagwort_6_id
     FULL JOIN schlagwoerter_schlagwort AS sw_7
       ON sw_7.schlagwort_id = sw_1st.schlagwort_7_id
     INNER JOIN project_listing_person AS bearbeiter
       ON  project_listing_enargus.projektleiter_id = bearbeiter.person_id
     INNER JOIN project_listing_ausfuehrende_stelle AS aus_stelle
       ON  project_listing_enargus.ausfuehrende_stelle_id = aus_stelle.ausfuehrende_stelle_id
     INNER JOIN project_listing_zuwendungsempfaenger AS zwe
       ON zwe.zuwendungsempfaenger_id = project_listing_enargus.zuwendsempfanger_id
    INNER JOIN project_listing_anschrift AS zwe_anschrift
       ON zwe_anschrift.anschrift_id = zwe.anschrift_id
   WHERE fkz = '%s'
        """ % fkz
    df_db = pd.read_sql_query(query, conn)
    # data from the data base
    print(' ')
    print('Vergleich für Projekt {}'.format(fkz))
    # comparison "Laufzeitbeginn" (date formate)
    db_laufzeitbeginn = df_db[df_db['fkz'] == fkz]['laufzeitbeginn']
    db_laufzeitbeginn = pd.to_datetime(db_laufzeitbeginn.values[0]).strftime('%Y-%m-%d')
    xlsx_laufzeitbeginn = df_xlsx[df_xlsx['fkz'] == str(fkz)]['Laufzeitbeginn']
    xlsx_laufzeitbeginn = pd.to_datetime(xlsx_laufzeitbeginn.values[0]).strftime('%Y-%m-%d')

    print('## Vergleich Laufzeitbeginn bzw. date-feature')
    if str(db_laufzeitbeginn) == str(xlsx_laufzeitbeginn):
        print('Die Angaben zum Laufzeitbeginn sind gleich.')
        print(' -- Datenbank: {}   \n --      xlxs: {}'.format(
                   db_laufzeitbeginn, xlsx_laufzeitbeginn))
    else:
        print(' ')
        print('Die Angaben zum Laufzeitbeginn sind NICHT gleich.')
        print(' -- Datenbank: {}   \n --      xlxs: {}'.format(
                   db_laufzeitbeginn, xlsx_laufzeitbeginn))

    print('## Vergleich Kurzbeschreibung bzw. character formate')
    # comparison "Kurzbeschreibung" (character formate)
    db_kurzbeschreibung = df_db[df_db['fkz'] == fkz]['kurzbeschreibung_de']
    db_kurzbeschreibung = db_kurzbeschreibung.values[0]
    xlsx_kurzbeschreibung = df_xlsx[df_xlsx['fkz'] == str(fkz)]['Kurzbeschreibung_de']
    xlsx_kurzbeschreibung = xlsx_kurzbeschreibung.values[0]
    if db_kurzbeschreibung == xlsx_kurzbeschreibung:
        print('Die Angaben zum Kurzbeschreibung_de sind gleich.')
        print(' -- Datenbank: {}   \n --      xlxs: {}'.format(
                   db_kurzbeschreibung[0:20], xlsx_kurzbeschreibung[0:20]))
    else:
        print('Die Angaben zum Kurzbeschreibung_de sind NICHT gleich.')
        print(' -- Datenbank: {}   \n --      xlxs: {}'.format(
                   db_kurzbeschreibung[0:20], xlsx_kurzbeschreibung[0:20]))

    print('## Vergleich PLZ_zwe bzw. character formate, oft fehlt die erste Null')
    # comparison "PLZ_zwe" (character formate, often first zero removed)
    db_PLZ_ZWE = df_db[df_db['fkz'] == fkz]['zwe_plz']
    db_PLZ_ZWE = str(db_PLZ_ZWE.values[0])
    xlsx_PLZ_ZWE = df_xlsx[df_xlsx['fkz'] == str(fkz)]['PLZ_ZWE']
    xlsx_PLZ_ZWE_deb = xlsx_PLZ_ZWE
    xlsx_PLZ_ZWE = str(xlsx_PLZ_ZWE.values[0])
    if db_PLZ_ZWE == xlsx_PLZ_ZWE:
        print('Die Angaben zum PLZ_zwe sind gleich.')
        print(' -- Datenbank: {}   \n --      xlxs: {}'.format(
                   db_PLZ_ZWE, xlsx_PLZ_ZWE))
    else:
        print('Die Angaben zum PLZ_zwe_de sind NICHT gleich.')
        print(' -- Datenbank: {}   \n --      xlxs: {}'.format(
                   db_PLZ_ZWE, xlsx_PLZ_ZWE))

    print('## Vergleich Foerdersumme bzw. decimal formate')
    # comparison "Foerdersumme" (decimal formate)
    db_Foerdersumme = df_db[df_db['fkz'] == fkz]['foerdersumme']
    db_Foerdersumme = str(db_Foerdersumme.values[0])
    xlsx_Foerdersumme = df_xlsx[df_xlsx['fkz'] == str(fkz)]['Foerdersumme_EUR']
    xlsx_Foerdersumme = str(xlsx_Foerdersumme.values[0])
    if db_Foerdersumme == xlsx_Foerdersumme:
        print('Die Angaben zum Foerdersumme sind gleich.')
        print(' -- Datenbank: {}   \n --      xlxs: {}'.format(
                   db_Foerdersumme, xlsx_Foerdersumme))
    else:
        print('Die Angaben zum Foerdersumme sind NICHT gleich.')
        print(' -- Datenbank: {}   \n --      xlxs: {}'.format(
                   db_Foerdersumme, xlsx_Foerdersumme))
