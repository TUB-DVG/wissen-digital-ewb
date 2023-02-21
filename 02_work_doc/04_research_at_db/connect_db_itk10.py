import psycopg2
import pandas as pd
from sqlalchemy import create_engine

# Create an engine instance
#conn_string = 'postgresql://dbadmint:abc123@127.0.0.1:5432/m4_data3'
conn_string = 'postgresql://adm_webcentral:M4_rocks_EWB@134.94.130.147:5432/db_webcentral3'
alchemeyEngine = create_engine(conn_string)


# connect to PostgreSQL server
conn = alchemeyEngine.connect()

# Read data from PostgreSQL database table and load into a DataFrame instance
## test the sql code and find the specific name of the tables, use pgadmin
df = pd.read_sql_query(
   """
   SELECT project_listing_teilprojekt.fkz, project_listing_enargus.thema, project_listing_forschung.forschungsprogramm
   FROM project_listing_teilprojekt
   INNER JOIN project_listing_enargus
   ON project_listing_enargus.enargus_id = project_listing_teilprojekt.enargus_daten_id
   INNER JOIN project_listing_forschung ON  project_listing_forschung.forschung_id = project_listing_enargus.forschung_id
   WHERE kurzbeschreibung_de like '%%BIM%%'
   """
   , conn)
# df = pd.read_sql_query(
#    """
#    SELECT project_listing_teilprojekt.fkz, project_listing_enargus.thema
#    FROM project_listing_teilprojekt
#    INNER JOIN project_listing_enargus ON project_listing_enargus.enargus_id = project_listing_teilprojekt.enargus_daten_id
#    WHERE fkz like '03ETS002B'
#    """
#    , conn)
print(df)
