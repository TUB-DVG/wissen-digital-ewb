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
DATA_PATH = os.path.join(PATH , 'auxillary/Household62_1h.csv') 
DF_MAIN = pd.read_csv(DATA_PATH)

csv_files = {
    "file1": "01_application/webcentral_app/use_cases/dashApp/auxillary/Household62_1h.csv",
    "file2": "01_application/webcentral_app/use_cases/dashApp/auxillary/Household73_15min.csv",
}
data_directory = '01_application/webcentral_app/use_cases/dashApp/auxillary'
file_list = os.listdir(data_directory)
file_list = [file for file in file_list if file.endswith('.csv')] 

app = DjangoDash('useCaseTS')

# Define the layout of the app
app.layout = html.Div([html.Div(
    dcc.Dropdown(
        id='file-selector',
        options=[{'label': file, 'value': file} for file in file_list],
        value=file_list[:min(len(file_list), 12)],  # Default to the first 12 files
        multi=True
    )),
    dcc.Loading(id="loading",
           children=[html.Div([dcc.Graph(id="time-series-chart",figure = {})])],
           type="circle",fullscreen=False),
    ],style={'font-family': "Roboto, sans-serif",
             
         "color":"rgb(116, 117, 121)",
         "font-size":" 18.75px",
         "font-weight": "400",
         "line-height": "22.5px",
         "overflow-x": "auto",
         "overflow-y": "auto",})


# Callback to update the graph based on file and column selection
@app.callback(
    Output('time-series-chart', 'figure'),
    Input('file-selector', 'value')
)
def update_graph(selected_files):
    if not selected_files:
        return go.Figure()

    # Initialize a plotly graph object figure
    fig = go.Figure()

    # Loop through selected files and add each as a separate trace in the graph
    for file in selected_files:
        df = pd.read_csv(os.path.join(data_directory, file), parse_dates=['datetime'])
        df.set_index('datetime', inplace=True)


         # Automatically add traces for all numerical columns
        for col in df.columns:
            fig.add_trace(go.Scatter(x=df.index, y=df[col], mode='lines', name=f'{file} - {col}'))



    # Update layout
    fig.update_layout(
        xaxis_title='Datum Zeit',
        yaxis_title="Werte (kWh)",
        legend_title='Dargestellte Zeitreihen'
    )

    return fig
