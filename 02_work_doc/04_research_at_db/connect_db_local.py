import psycopg2
import pandas as pd
from sqlalchemy import create_engine

# Create an engine instance
conn_string = 'postgresql://dbadmint:abc123@localhost:5432/m4_data3'
alchemeyEngine = create_engine(conn_string)

# connect to PostgreSQL server
conn = alchemeyEngine.connect()

# Read data from PostgreSQL database table and load into a DataFrame instance
df = pd.read_sql_table("weatherdata_over_weatherdata", conn)
df.info()

print('Hello world')
