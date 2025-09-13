import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# Create sample stops
stops = pd.DataFrame({
    'stop_id': range(1, 11),
    'name': [f'Stop {i}' for i in range(1, 11)],
    'lat': np.random.uniform(40.7, 40.8, 10),
    'lon': np.random.uniform(-74, -73.9, 10)
})
stops.to_csv('sample_data/stops.csv', index=False)

# Sample routes
routes = pd.DataFrame({
    'route_id': [1, 2, 3],
    'name': ['Route A','Route B','Route C']
})
routes.to_csv('sample_data/routes.csv', index=False)

# Sample arrivals
arrivals_list = []
for route_id in routes['route_id']:
    for stop_id in stops['stop_id']:
        for hour in range(6, 23):
            scheduled_time = datetime.now().replace(hour=hour, minute=0, second=0, microsecond=0)
            actual_time = scheduled_time + timedelta(minutes=np.random.randint(-5, 15))
            delay = (actual_time - scheduled_time).total_seconds()/60
            arrivals_list.append([route_id, stop_id, scheduled_time, actual_time, delay])
arrivals = pd.DataFrame(arrivals_list, columns=['route_id','stop_id','scheduled_time','actual_time','delay_minutes'])
arrivals.to_csv('sample_data/arrivals.csv', index=False)

print("Sample data generated in sample_data/ folder")
