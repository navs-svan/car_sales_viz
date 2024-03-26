import pandas as pd
from sqlalchemy import URL, create_engine
from sqlalchemy.orm import sessionmaker
import json
import os
from table_schema import Base, Dates, Branch, Countries, Dealer, Products, Revenue

# HELPER FUNCTIONS
def load_dates(row):
    ...


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

Base.metadata.create_all(bind=engine)
Session = sessionmaker(bind=engine)

session = Session()


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

df = df = df_dict["Country"]
df.drop_duplicates(subset=["country_id"], inplace=True)
