
import pandas as pd
from .Stromlastapproximation_Csv import Stromapproximation
from django_plotly_dash import DjangoDash
import plotly.express as px  # (version 4.7.0 or higher)
from dash import  dcc, html, Input, Output  # pip install dash (version 2.0.0 or higher)
from project_listing.models import *
import os
import plotly.graph_objects as go

os.chdir(r'C:\Users\Drass\plotly dash\webcentral\01_application\webcentral_app\LastProfile\Dash_app')

df_haupt=pd.read_csv('Hauptblatt2.csv')
data=[]



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
    dcc.Input(id="power_requirement", type="number", placeholder="Jahresstrombedarfs in kWh/a", debounce=True),
    
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
        fig.add_trace(go.Scatter(name='Strom-lastgang in kW',x=result['Time'], y=result['Last'],mode='lines', line=dict(color="#0000ff")))
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
    prevent_initial_call=True,
)

def download_as_csv(n_clicks):
    if not n_clicks:
        raise PreventUpdate
    else:
        #print (d)
        return dcc.send_data_frame(d.to_csv,'Stromdata.csv')
# ------------------------------------------------------------------------------
# Connect the Plotly power_graphs with Dash Components







