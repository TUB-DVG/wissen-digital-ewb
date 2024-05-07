import os
import pathlib

import pandas as pd
import plotly.graph_objects as go
from django_plotly_dash import DjangoDash
from dash.exceptions import PreventUpdate
from django.utils.translation import gettext as _
from django.contrib.sessions.models import Session
import dash
from dash import  dcc, html, Input, Output ,State

PATH = pathlib.Path(__file__).parent.resolve() 
DATA_PATH = os.path.join(PATH , 'DreiHaushalte.csv') 
DF_MAIN = pd.read_csv(DATA_PATH)

csv_files = {
    "file1": "01_application/webcentral_app/use_cases/dashApp/Household62_1h.csv",
    "file2": "01_application/webcentral_app/use_cases/dashApp/Household73_15min.csv",
}
app = DjangoDash('useCaseTS')

# Read all CSV files into dataframes
dataframes = {name: pd.read_csv(path) for name, path in csv_files.items()}

# Prepare graph traces from all dataframes
traces = []
for name, df in dataframes.items():
    traces.append({
        'x': df.iloc[:, 0],  # Assuming the first column is x-axis
        'y': df.iloc[:, 1],  # Assuming the second column is y-axis
        'type': 'scatter',
        'name': name  # Legend name for each trace
    })

# Layout of the Dash app
app.layout = html.Div([
    dcc.Graph(
        id='all-data-graph',
        figure={
            'data': traces,
            'layout': {
                'title': 'Combined Data Plot'
            }
        }
    )
])
options = [{"label": k, "value": k} for k in csv_files.keys()]

app.layout = html.Div([
    dcc.Dropdown(id='file-dropdown', options=options, value='file1'),
    dcc.Graph(id='graph')
])

@app.callback(
    Output('graph', 'figure'),
    [Input('file-dropdown', 'value')]
)
def update_graph(selected_file):
    df = pd.read_csv(csv_files[selected_file])
    figure = {
        'data': [{'x': df.columns[0], 'y': df.columns[1]}],  # Adjust columns as needed
        'layout': {'title': 'Simple Graph'}
    }
    return figure