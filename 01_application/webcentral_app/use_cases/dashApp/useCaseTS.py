import os
import pathlib
import regex as re
import pandas as pd
import plotly.graph_objects as go
from django_plotly_dash import DjangoDash
from dash.exceptions import PreventUpdate
from django.utils.translation import gettext as _
from django.contrib.sessions.models import Session
import dash
from dash import  dcc, html, Input, Output, State

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

def load_data(file):
    df = pd.read_csv(os.path.join(data_directory, file), parse_dates=['datetime'])
    df.set_index('datetime', inplace=True)
    return df

data_store = {
    "building62" : {
        "5s" : load_data("Household62_5sec.csv"),
        "15min" :  load_data("Household62_15min.csv"),
        "1h" :  load_data("Household62_1h.csv")
        
    },
    "building73" : {
        "5s" : load_data("Household73_5sec.csv"),
        "15min" :  load_data("Household73_15min.csv"),
        "1h" :  load_data("Household73_1h.csv")
        
    },
    "building106" : {
        "5s" : load_data("Household106_5sec.csv"),
        "15min" :  load_data("Household106_15min.csv"),
        "1h" :  load_data("Household106_1h.csv")
        
    },
    "threebuildings" : {
        "5s" : load_data("three_households_5sec.csv"),
        "15min" :  load_data("three_households_15min.csv"),
        "1h" :  load_data("three_households_1h.csv")
        
    },


}

app = DjangoDash('useCaseTS')

# Define the layout of the app
app.layout = html.Div([
    html.Div([
        dcc.Dropdown(
        id='building-dropdown',
        options=[
            {'label': 'Building 1', 'value': 'building62'},
            {'label': 'Building 2', 'value': 'building73'},
            {'label': 'Building 3', 'value': 'building106'},
            {'label': 'All Buildings', 'value': 'all'}
        ],
        value='all'
    ),
    dcc.Dropdown(
        id='interval-dropdown',
        options=[
            {'label': '5 Seconds', 'value': '5s'},
            {'label': '15 Minutes', 'value': '15min'},
            {'label': '1 Hour', 'value': '1h'},
            {'label': 'Alle Frequenzen', 'value': 'all'},

        ],
        value='all'
    ),
    dcc.Dropdown(
        id='scale-dropdown',
        options=[
            {'label': 'Equipment', 'value': 'equipment'},
            {'label': 'Full Building', 'value': 'full_building'},
            {'label': 'Aggregated Buildings', 'value': 'aggregated_buildings'},
            {'label': 'Alle Aggregationen', 'value': 'all'},
        ],
        value='all'
    ),
        dcc.Loading(
            id="loading",
            children=[html.Div([dcc.Graph(id="time-series-chart",figure = {})])],
            type="circle",
            fullscreen=False
            )
            ])],
            style={'font-family': "Roboto, sans-serif",
                   "color":"rgb(116, 117, 121)",
                   "font-size":" 18.75px",
                   "font-weight": "400",
                   "line-height": "22.5px",
                   "overflow-x": "auto",
                   "overflow-y": "auto",})


# Callback to update the graph based on file and column selection
@app.callback(
    Output('time-series-chart', 'figure'),
    Input('building-dropdown', 'value'),
    Input('interval-dropdown', 'value'),
    Input('scale-dropdown', 'value'),
)
def update_graph(building, interval, scale):
    
    temp_data = {}
    # Initialize a plotly graph object figure
    fig = go.Figure()

    # Loop through selected files and add each as a separate trace in the graph
    #for file in selected_files:
    #    df = pd.read_csv(os.path.join(data_directory, file), parse_dates=['datetime'])
    #    df.set_index('datetime', inplace=True)#


         # Automatically add traces for all numerical columns
    #    for col in df.columns:
    #        fig.add_trace(go.Scatter(x=df.index, y=df[col], mode='lines', name=f'{file} - {col}'))
    if building == "all":
        buildings = ["building62", "building73", "building106", "threebuildings"]
    else:
        buildings = [building]

    for b in buildings:
        if interval == "all":
            intervals = ["5s", "15min", "1h"]
        else:
            intervals = [interval]
            # columns: 
            # Elektrisch-Kombiniert_einHaushalt_15min,Wasserkocher_einHaushalt_15min,
            # Waschmaschine_einHaushalt_15min,Kühl-_und_Gefrierschrank_einHaushalt_15min,Hauptanschluss_einHaushalt_15min,Durchlauferhitzer_einHaushalt_15min

        for i in intervals:
            data = data_store[b][i]
            if scale == "all" or scale == "equipment":
                if any(re.match(r'Wasserkocher.*', col) for col in data.columns):
                    for col in [col for col in data.columns if re.match(r'Wasserkocher.*', col)]:
                        fig.add_trace(go.Scatter(x=data.index, y=data[col], mode='lines', name=f'{b} {i} Wasserkocher'))
                if any(re.match(r'Waschmaschine.*', col) for col in data.columns):
                    for col in [col for col in data.columns if re.match(r'Waschmaschine.*', col)]:
                        fig.add_trace(go.Scatter(x=data.index, y=data[col], mode='lines', name=f'{b} {i} Waschmaschine'))
                if any(re.match(r'Kühl-_und_Gefrierschrank.*', col) for col in data.columns):
                    for col in [col for col in data.columns if re.match(r'Kühl-_und_Gefrierschrank.*', col)]:
                        fig.add_trace(go.Scatter(x=data.index, y=data[col], mode='lines', name=f'{b} {i} Kühl- und Gefrierschrank'))
                if any(re.match(r'Durchlauferhitzer.*', col) for col in data.columns):
                    for col in [col for col in data.columns if re.match(r'Durchlauferhitzer.*', col)]:
                        fig.add_trace(go.Scatter(x=data.index, y=data[col], mode='lines', name=f'{b} {i} Durchlauferhitzer'))
            
            if scale == "all" or scale == "full_building":
                if any(re.match(r'Elektrisch-Kombiniert.*', col) for col in data.columns):
                    for col in [col for col in data.columns if re.match(r'Hauptanschluss.*', col)]:
                        fig.add_trace(go.Scatter(x=data.index, y=data[col], mode='lines', name=f'{b} {i} Gesamter Stromverbrauch'))
            
            if scale == "all" or scale == "aggregated_buildings":
                if building == 'all':
                    aggregated_data = data.groupby(data.index).sum()
                    if any(re.match(r'Elektrisch-Kombiniert.*', col) for col in aggregated_data.columns):
                        for col in [col for col in aggregated_data.columns if re.match(r'Hauptanschluss.*', col)]:
                            fig.add_trace(go.Scatter(x=aggregated_data.index, y=aggregated_data[col], mode='lines', name=f'{b} {i} Aggregierter {col}'))
                else:
                    if any(re.match(r'Elektrisch-Kombiniert.*', col) for col in data.columns):
                        for col in [col for col in data.columns if re.match(r'Hauptanschluss.*', col)]:
                            fig.add_trace(go.Scatter(x=data.index, y=data[col], mode='lines', name=f'{b} {i} Gesamtstromverbrauch '))

            elif scale == "aggregated_buildings":
                
                fig.add_trace(go.Scatter(x=aggregated_data.index, y=aggregated_data['total'], mode='lines', name=f'{b} {i} Aggregierter Gesamterverbrauch'))

        

    # Update layout
    fig.update_layout(
        xaxis_title='Datum Zeit',
        yaxis_title="Werte (kWh)",
        legend_title='Dargestellte Zeitreihen'
    )

    return fig
