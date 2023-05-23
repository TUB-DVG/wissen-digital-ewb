
import pandas as pd
from .Stromlastapproximation_Csv import Stromapproximation
from django_plotly_dash import DjangoDash
import plotly.express as px  # (version 4.7.0 or higher)
from dash import  dcc, html, Input, Output ,State # pip install dash (version 2.0.0 or higher)
from project_listing.models import *
import os
from dash.exceptions import PreventUpdate
import plotly.graph_objects as go

PATH = os.chdir(r'./LastProfile/Dash_app')

df_haupt = pd.read_csv('Hauptblatt2.csv')


data = []

app = DjangoDash('Stromlast')   # replaces dash.Dash


# App layout
app.layout = html.Div([
    #Title
    html.H1("Stromlast Approximation", style={'text-align': 'center'}),
    #Download data as csv
    html.Button("Download Csv", id="btn-download-csv"),
    dcc.Download(id="download-csv"),
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
    dcc.Input(id = "powerRequirement", type = "number", 
    placeholder = "Jahresstrombedarfs in kWh/a",
    style = {'width':'200px'}, debounce=True),
    
    dcc.RadioItems(
        options = [
                {'label': 'January', 'value': '1'},
                {'label': 'February', 'value': '2'},
                {'label': 'March', 'value': '3'},
                {'label': 'April', 'value': '4'},
                {'label': 'May', 'value': '5'},
                {'label': 'June', 'value': '6'},
                {'label': 'July', 'value': '7'},
                {'label': 'August', 'value': '8'},
                {'label': 'September', 'value': '9'},
                {'label': 'October', 'value': '10'},
                {'label': 'November', 'value': '11'},
                {'label': 'December', 'value': '12'},
                {'label': 'All', 'value': 'All'},
            ],
        value = 'All',
        id = 'display_Month',
        inline = True
    ),
    dcc.Graph(id = 'power_graph', figure={}),

# style is used to control css output directly from dash 
],style={'font-family': "Roboto, sans-serif","color":"rgb(116, 117, 121)","font-size":" 18.75px",
"font-weight": "400",
"line-height": "22.5px"})
# ------------------------------------------------------------------------------
# Connect the Plotly graph with Dash Components

#Stromapproximation
@app.callback(
    Output(component_id='power_graph', component_property='figure'),
    Input('application','value'),
 
    Input('powerRequirement','value'),
    Input('display_Month','value'),
    prevent_initial_call=True,)
    
def updatePowerGraph(application:str,powerRequirement:int,display_Month:str):

    if application != None:

        WW = Stromapproximation(int(application),powerRequirement)
        days = df_haupt['Datum/ Uhrzeit']
        global data
        
        data = {'Time':days[0:8760],'Last':WW}
        data = pd.DataFrame(data)
        data['Time'] = pd.to_datetime(data['Time'], errors='coerce')
        if display_Month == 'All':   
         
            result = data
        else:
            result = {'Last':
            (data.groupby(data.Time.dt.month).
            get_group(int(display_Month)))['Last'],
            'Time':(data.groupby(data.Time.dt.month).
            get_group(int(display_Month)))['Time']}
        from plotly.subplots import make_subplots
        fig = make_subplots()
        fig.add_trace(go.Scatter(name='Strom-lastgang in kW',x=result['Time'],
         y = result['Last'],mode='lines', line=dict(color="#0000ff")))
        fig.update_xaxes(
        tickangle = 90,
        title_text = "Datum",
        title_font = {"size": 20}
        )

        fig.update_yaxes(
        title_text = "Strom-lastgang in kW",
        title_standoff = 25
        )
        return fig
    else:
        return {}
# The download csv Funcionality
@app.callback(
    Output("download-csv", "data"),
    Input("btn-download-csv", "n_clicks"),
    
    Input('application','value'),

    Input('powerRequirement','value'),
        State("application","options"),
    prevent_initial_call=True,
)

def DownloadAsCsv(n_clicks,application:str,powerRequirement:int,state):
    if not n_clicks:
        raise PreventUpdate
    else:
        #print(state)
        label = [x['label'] for x in state if x['value'] == application]
        data.columns = [['Jahresstrombedarf in KWh/a :'+str(powerRequirement),''],
        ['Anwendung:' + label[0],''],['',''],['Datum','Last']]    
        #print (d)
        return dcc.send_data_frame(data.to_csv,'Stromdata.csv',index=False)
# ------------------------------------------------------------------------------
# Connect the Plotly power_graphs with Dash Components







