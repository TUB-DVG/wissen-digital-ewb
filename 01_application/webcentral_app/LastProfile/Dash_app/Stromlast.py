import os
import pathlib
import pandas as pd
import plotly.graph_objects as go
from project_listing.models import *
from django_plotly_dash import DjangoDash
from dash.exceptions import PreventUpdate
from dash import  dcc, html, Input, Output ,State # pip install dash (version 2.0.0 or higher)
from .Stromlastapproximation_Csv import currentApproximation

PATH = pathlib.Path(__file__).parent.resolve() 
DATA_PATH = os.path.join(PATH , 'Hauptblatt2.csv') 
DF_MAIN = pd.read_csv(DATA_PATH)
data = []
app = DjangoDash('Stromlast')   # replaces dash.Dash

# App layout
app.layout = html.Div([
    #Title
    html.H1("Stromlast Approximation", style = {'text-align': 'center'}),
    #Download data as csv
    html.Button("Download als csv", id = "btnDownloadCsv"),
    dcc.Download(id = "downloadCsv"),
    # Dropdown for the available applications
    dcc.Dropdown(
        options = [
            {'label': 'Gewerbe allgemein ', 'value': '2'},
            {'label': 'Gewerbe werktags 8-18 ', 'value': '3'},
            {'label': 'Gewerbe Verbrauch Abend', 'value': '4'},
            {'label': 'Gewerbe durchlaufend', 'value': '5'},
            {'label': 'Laden Friseur  ', 'value': '6'},
            {'label': 'Bäckerei mit Backstube ', 'value': '7'},
            {'label': 'Wochenendbetrieb ', 'value': '8'},
            {'label': 'Haushaltskunden ', 'value': '9'},
            {'label': 'Landwirtschaftsbetriebe ', 'value': '10'},
            {'label': 'Landwirts. mit Milchwirts Tierzucht ', 'value': '11'},
            {'label': 'Übrige Landwirtschaftsbe ', 'value': '12'},
        ],
        id = 'application'
    ),
    # Input Field for the 
    dcc.Input(
        id = "powerRequirement", type = "number", 
        placeholder = "Jahresstrombedarfs in kWh/a",
        style = {'width':'200px'}, debounce = True
    ),    
    dcc.RadioItems(
        options=[
            {'label': 'Januar', 'value': '1'},
            {'label': 'Februar', 'value': '2'},
            {'label': 'März', 'value': '3'},
            {'label': 'April', 'value': '4'},
            {'label': 'Mai', 'value': '5'},
            {'label': 'Juni', 'value': '6'},
            {'label': 'Juli', 'value': '7'},
            {'label': 'August', 'value': '8'},
            {'label': 'September', 'value': '9'},
            {'label': 'Oktober', 'value': '10'},
            {'label': 'November', 'value': '11'},
            {'label': 'Dezember', 'value': '12'},
            {'label': 'All', 'value': 'All'},
        ],
        value = 'All',
        id = 'displayMonth',
        inline = True
    ),
    dcc.Graph(id = 'powerGraph', figure = {}),
# style is used to control css output directly from dash 
],style = {'font-family': "Roboto, sans-serif","color":"rgb(116, 117, 121)",
           "font-size":" 18.75px","font-weight": "400","line-height": "22.5px"}
           )
# ------------------------------------------------------------------------------
# Connect the Plotly graph with Dash Components

#Stromapproximation
@app.callback(
    Output('powerGraph','figure'),
    Input('application','value'),
    Input('powerRequirement','value'),
    Input('displayMonth','value'),
    prevent_initial_call=True
    )
    
def updatePowerGraph(application:str,powerRequirement:int,displayMonth:str):

    if application != None:
        WW = currentApproximation(int(application),powerRequirement)
        days = DF_MAIN['Datum/ Uhrzeit']
        global data
        data = {'Time':days[0:8760],'Last':WW}
        data = pd.DataFrame(data)
        data['Time'] = pd.to_datetime(data['Time'], errors='coerce')
        if displayMonth == 'All':   
            result = data
        else:
            result = {
                'Last':(data.groupby(data.Time.dt.month).
                get_group(int(displayMonth)))['Last'],
                'Time':(data.groupby(data.Time.dt.month).
                get_group(int(displayMonth)))['Time']
            }
        from plotly.subplots import make_subplots
        fig = make_subplots()
        fig.add_trace(go.Scatter(name = 'Stromlastgang in kW',x = result['Time'],
        y = result['Last'],mode = 'lines', line=dict(color = "#0000ff")))

        fig.update_xaxes(
        tickangle = 90,
        title_text = "Datum",
        title_font = {"size": 20}
        )

        fig.update_yaxes(
        title_text = "Stromlastgang in kW",
        title_standoff = 25
        )
        return fig
    else:
        return {}
# The download csv Funcionality
@app.callback(
    Output("downloadCsv", "data"),
    Input("btnDownloadCsv", "n_clicks"),
    Input('application','value'),
    Input('powerRequirement','value'),
    State("application","options"),
    prevent_initial_call = True,
)

def downloadAsCsv(nClicks,application:str,powerRequirement:int,state):
    if not nClicks:
        raise PreventUpdate
    else:
        label = [x['label'] for x in state if x['value'] == application]
        data.columns = [['Jahresstrombedarf in KWh/a :'+str(powerRequirement),''],
        ['Anwendung: ' + label[0],''],['',''],['Datum','Last']]    
        return dcc.send_data_frame(data.to_csv,'Stromlastgang.csv',index = False)
# ------------------------------------------------------------------------------
# Connect the Plotly powerGraphs with Dash Components







