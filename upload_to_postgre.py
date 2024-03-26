import pandas as pd
from sqlalchemy import URL, create_engine
import json
import os

# CREATE CONNECTION TO POSTGRE

DBHOST = os.environ.get("DBHOST")
DBPORT = os.environ.get("DBPORT")
DBUSER = os.environ.get("DBUSER")
DBNAME = os.environ.get("DBNAME")
DBPASS = os.environ.get("DBPASS")

engine_url = URL.create(
    drivername="postgresql+psycopg2",
    username=DBUSER,
    password=DBPASS,
    host=DBHOST,
    port=DBPORT,
    database=DBNAME,
)
engine = create_engine(url=engine_url)
conn = engine.connect()


# LOAD EXCEL FILE TO PANDAS DATAFRAMES

filepath = "raw_data/star-schema-2.xlsx"
config_file = "config.json"

df_dict = {}

with open(config_file, "r") as f:
    config = json.load(f)

for sheet in config:
    params = config[sheet]["READ_PARAMS"]
    df_dict[sheet] = pd.read_excel(filepath, **params)

# Country table contains duplicates
    
df = df_dict["Country"]
df.drop_duplicates(subset=["country_id"], inplace=True)

# Dealers have missing data

df = df_dict["Dealer"]
missing = pd.DataFrame.from_records(
    [
        {"dealer_id": "DLR0090"},
        {"dealer_id": "DLR0144"},
        {"dealer_id": "DLR0258"},
        {"dealer_id": "DLR0212"},
        {"dealer_id": "DLR0044"},
    ]
)
df_dict["Dealer"] = pd.concat([df, missing], ignore_index=True)

# INSERT VALUES INTO TABLE

df_dict["Date"].to_sql("dates", if_exists="append", con=conn, index=False)
df_dict["Branch"].to_sql("branches", if_exists="append", con=conn, index=False)
df_dict["Country"].to_sql("countries", if_exists="append", con=conn, index=False)
df_dict["Dealer"].to_sql("dealers", if_exists="append", con=conn, index=False)
df_dict["Product"].to_sql("products", if_exists="append", con=conn, index=False)
df_dict["Revenue"].to_sql("revenue", if_exists="append", con=conn, index=False)

conn.close()
