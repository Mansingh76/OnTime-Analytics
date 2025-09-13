import dash
from dash import dcc, html
import pandas as pd
import plotly.express as px
from sqlalchemy import create_engine
import os

DB_URL = os.getenv('DATABASE_URL', 'sqlite:///../ontime.db')
engine = create_engine(DB_URL)

app = dash.Dash(__name__)
server = app.server

stops = pd.read_sql('SELECT * FROM stops', engine)
routes = pd.read_sql('SELECT * FROM routes', engine)
arrivals = pd.read_sql('SELECT * FROM arrivals', engine)

arrivals['scheduled_time'] = pd.to_datetime(arrivals['scheduled_time'])
arrivals['actual_time'] = pd.to_datetime(arrivals['actual_time'])
arrivals['delay_minutes'] = arrivals['delay_minutes'].astype(float)
arrivals['hour'] = arrivals['scheduled_time'].dt.hour
arrivals['weekday'] = arrivals['scheduled_time'].dt.day_name()
arrivals['is_weekend'] = arrivals['weekday'].isin(['Saturday','Sunday'])

avg_delay = arrivals['delay_minutes'].mean()
most_reliable_route = arrivals.groupby('route_id')['delay_minutes'].mean().sort_values().index[0]
busiest_stop = arrivals.groupby('stop_id').size().sort_values(ascending=False).index[0]

fig_map = px.scatter_mapbox(
    stops,
    lat='lat',
    lon='lon',
    hover_name='name',
    zoom=12,
    height=500
)
fig_map.update_layout(mapbox_style='open-street-map', margin={'r':0,'t':0,'l':0,'b':0})

heat = arrivals.groupby(['hour','route_id'])['delay_minutes'].mean().reset_index()
fig_heat = px.density_heatmap(
    heat,
    x='hour',
    y='route_id',
    z='delay_minutes',
    color_continuous_scale='Viridis',
    height=500,
    labels={'hour':'Hour of Day', 'route_id':'Route', 'delay_minutes':'Avg Delay (min)'}
)

weekday_avg = arrivals.groupby('is_weekend')['delay_minutes'].mean().reset_index()
weekday_avg['day_type'] = weekday_avg['is_weekend'].map({True:'Weekend', False:'Weekday'})
fig_weekday = px.bar(
    weekday_avg,
    x='day_type',
    y='delay_minutes',
    text='delay_minutes',
    title='Average Delay: Weekday vs Weekend'
)

app.layout = html.Div([
    html.H1('OnTime — Public Transport Analytics Dashboard', style={'textAlign':'center'}),
    
    html.Div([
        html.Div([
            html.H3('Most Reliable Route'),
            html.H2(most_reliable_route, style={'color':'green'})
        ], style={'width':'30%','display':'inline-block'}),
        
        html.Div([
            html.H3('Average Delay (mins)'),
            html.H2(f"{avg_delay:.1f}")
        ], style={'width':'30%','display':'inline-block'}),
        
        html.Div([
            html.H3('Busiest Stop'),
            html.H2(busiest_stop, style={'color':'red'})
        ], style={'width':'30%','display':'inline-block'}),
    ], style={'textAlign':'center', 'marginBottom':'20px'}),
    
    html.Div([
        html.Div(dcc.Graph(figure=fig_map), style={'width':'50%','display':'inline-block'}),
        html.Div(dcc.Graph(figure=fig_heat), style={'width':'50%','display':'inline-block'})
    ]),
    
    html.Div([
        html.Div(dcc.Graph(figure=fig_weekday), style={'width':'50%','display':'inline-block'}),
    ], style={'marginTop':'20px'}),
    
    html.Div([
        html.H3('Insights:'),
        html.Ul([
            html.Li('Average delays are highest during rush hours.'),
            html.Li('Route reliability ranking shows which routes are consistently on time.'),
            html.Li('Busiest stops can indicate potential congestion points.'),
            html.Li('Weekend patterns differ significantly from weekdays.')
        ])
    ], style={'marginTop':'20px','padding':'10px','border':'1px solid #ccc','borderRadius':'5px'})
])

if __name__ == '__main__':
    app.run_server(host='0.0.0.0', port=8050, debug=False)
