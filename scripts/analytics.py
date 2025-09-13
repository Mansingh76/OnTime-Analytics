import pandas as pd
from sqlalchemy import create_engine
import os

DB_URL = os.getenv('DATABASE_URL', 'sqlite:///ontime.db')
engine = create_engine(DB_URL)

arrivals = pd.read_sql('SELECT * FROM arrivals', engine)

arrivals['scheduled_time'] = pd.to_datetime(arrivals['scheduled_time'])
arrivals['actual_time'] = pd.to_datetime(arrivals['actual_time'])
arrivals['delay_minutes'] = arrivals['delay_minutes'].astype(float)

# Analytics
avg_delay = arrivals['delay_minutes'].mean()
route_ranking = arrivals.groupby('route_id')['delay_minutes'].mean().sort_values()
busiest_stop = arrivals.groupby('stop_id').size().sort_values(ascending=False).index[0]

print(f"Average delay: {avg_delay:.1f} minutes")
print("Route reliability ranking (best to worst):")
print(route_ranking)
print(f"Busiest stop: {busiest_stop}")
