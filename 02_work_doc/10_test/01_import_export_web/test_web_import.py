#!/usr/bin/env python3

import pandas as pd
from sqlalchemy import create_engine

# read data from the xlsx file
path_to_xlsx = 'enargus_csv_20220902_test1.xlsx'
df_xlxs = pd.read_excel(path_to_xlsx)
print(df_xlxs)


# read data from the data base
# Create an engine instance
# remote access after config the server see [[remote_postgresql.org]
conn_string = 'postgresql://dbadmint:abc123@localhost:5432/m4_data2'
alchemeyEngine = create_engine(conn_string)

# connect to PostgreSQL server
conn = alchemeyEngine.connect()

# Read data from PostgreSQL database table and load into a DataFrame instance
# test the sql code and find the specific name of the tables, use pgadmin
df = pd.read_sql_query(
   """
   SELECT project_listing_teilprojekt.fkz, project_listing_enargus.thema, project_listing_forschung.forschungsprogramm
   FROM project_listing_teilprojekt
   INNER JOIN project_listing_enargus
   ON project_listing_enargus.enargus_id = project_listing_teilprojekt.enargus_daten_id
   INNER JOIN project_listing_forschung ON  project_listing_forschung.forschung_id = project_listing_enargus.forschung_id
   WHERE kurzbeschreibung_de like '%%BIM%%'
   """, conn)
print(df)
