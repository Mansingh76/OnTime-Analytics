import pandas as pd
from sqlalchemy import create_engine
import os

DB_URL = os.getenv('DATABASE_URL', 'sqlite:///ontime.db')
engine = create_engine(DB_URL)

# Load CSVs
stops = pd.read_csv('sample_data/stops.csv')
routes = pd.read_csv('sample_data/routes.csv')
arrivals = pd.read_csv('sample_data/arrivals.csv')

# Write to DB
stops.to_sql('stops', engine, if_exists='replace', index=False)
routes.to_sql('routes', engine, if_exists='replace', index=False)
arrivals.to_sql('arrivals', engine, if_exists='replace', index=False)

print("ETL complete: data loaded into database")
