import pathlib

import pandas as pd
from .Stromlastapproximation_Csv import Stromapproximation
from django_plotly_dash import DjangoDash

from dash import  dcc, html, Input, Output  # pip install dash (version 2.0.0 or higher)
from project_listing.models import *
import os
import plotly.graph_objects as go

PATH = pathlib.Path(__file__).parent.resolve() 
DATA_PATH = os.path.join(PATH , 'Hauptblatt2.csv') 
df_haupt=pd.read_csv(DATA_PATH)
data=[]
app = DjangoDash('Stromlast')   # replaces dash.Dash


# App layout
app.layout = html.Div([
    #Title
    html.H1("Stromlast Approximation", style={'text-align': 'center'}),
 
    # Dropdown for the available applications
    dcc.Dropdown(
        options=[
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
        id='application'
        ),
        # Input Field for the 
    dcc.Input(id="power_requirement", type="number", placeholder="Jahresstrombedarf in kWh/a",  debounce=True,style={'width':'200px'}),
    
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
        value='All',
        id='display_Month',
        inline=True
    ),
    dcc.Graph(id='power_graph', figure={}),

   




])
# ------------------------------------------------------------------------------
# Connect the Plotly graph with Dash Components

#Stromapproximation
@app.callback(
    Output(component_id='power_graph', component_property='figure'),
    Input('application','value'),
    Input('power_requirement','value'),
    Input('display_Month','value'),
    prevent_initial_call=True,)
    
def update_power_graph(application:str,power_requirement:int,display_Month:str):

    if application!=None:
        WW=Stromapproximation(int(application),power_requirement)
        days=df_haupt['Datum/ Uhrzeit']
        global d
        data = {'Last':WW,'Time':days[0:8760]}
        data=pd.DataFrame(data)
        data['Time'] = pd.to_datetime(data['Time'], errors='coerce')
        if display_Month=='All':   
         
            result=data
        else:
            result={'Last':(data.groupby(data.Time.dt.month).get_group(int(display_Month)))['Last'],'Time':(data.groupby(data.Time.dt.month).get_group(int(display_Month)))['Time']}
        from plotly.subplots import make_subplots
        fig = make_subplots()
        fig.add_trace(go.Scatter(name='Stromlastgang in kW',x=result['Time'], y=result['Last'],mode='lines', line=dict(color="#0000ff")))
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

# ------------------------------------------------------------------------------
# Connect the Plotly power_graphs with Dash Components






