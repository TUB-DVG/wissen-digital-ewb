from this import d
from turtle import title
import pandas as pd


import os

os.chdir(r'C:\Users\Drass\plotly dash\webcentral\01_application\webcentral_app\project_listing\Dash_app')
# YOU MUST PUT sheet_name=None TO READ ALL CSV FILES IN YOUR XLSM FILE
df_haupt=pd.read_csv('Hauptblatt2.csv')
d=[]


from .Stromlastapproximation_Csv import Stromapproximation

from django_plotly_dash import DjangoDash
import os


import plotly.express as px  # (version 4.7.0 or higher)
import pandas as pd
from dash import  dcc, html, Input, Output  # pip install dash (version 2.0.0 or higher)

import datetime
from project_listing.models import *
app = DjangoDash('SimpleExample')   # replaces dash.Dash


# App layout
app.layout = html.Div([

    html.H1("Stromlast Approximation", style={'text-align': 'center'}),

    html.Button("Download Csv", id="btn-download-csv"),
    dcc.Download(id="download-csv"),
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
        id='input'
        ),
    dcc.Input(id="input2", type="number", placeholder="Strombedarf", debounce=True),
    
    dcc.RadioItems(
        options=[
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
        value='All',
        id='Display_Month',
        inline=True
    ),
    dcc.Graph(id='graph', figure={}),

   




])
# ------------------------------------------------------------------------------
# Connect the Plotly graphs with Dash Components

#Stromapproximation
@app.callback(
    Output(component_id='graph', component_property='figure'),
    Input('input','value'),
    Input('input2','value'),
    Input('Display_Month','value'),
    prevent_initial_call=True,)
    
def update_graph(value,value2,display):
    print(value)
    if value!=None:
        WW=Stromapproximation(int(value),value2)
        days=df_haupt['Datum/ Uhrzeit']
        global d
        d = {'Last':WW,'Time':days[0:8760]}
        d=pd.DataFrame(d)
        d['Time'] = pd.to_datetime(d['Time'], errors='coerce')
        #print(d)
        #print(d.Day.dt.month)
        #print(d.groupby(d.Day.dt.month).get_group(1))
        #print(d)
        if display=='All':   
            #result={'Last':(d.groupby(d.Day.dt.month)['Last'].sum()),'Month':list(calendar.month_name)[1:]}
            fig = px.line(d,x='Time', y='Last')
            return fig
        else:
            result={'Last':(d.groupby(d.Time.dt.month).get_group(int(display)))['Last'],'Time':(d.groupby(d.Time.dt.month).get_group(int(display)))['Time']}
            #print(Stromapproximation(1,7000000))
            fig = px.line(result,x='Time', y='Last')
            return fig
    else:
        return {}

@app.callback(
    Output("download-csv", "data"),
    Input("btn-download-csv", "n_clicks"),
    prevent_initial_call=True,
)

def download_as_excel(n_clicks):
    if not n_clicks:
        raise PreventUpdate
    else:
        d.to_csv('Stromdata.csv')
       

        return dcc.send_file('Stromdata.csv')
# ------------------------------------------------------------------------------
# Connect the Plotly graphs with Dash Components







