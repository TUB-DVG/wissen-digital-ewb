from cmath import nan
from turtle import title
import pandas as pd
import datetime
from collections import OrderedDict


import os

os.chdir(r'C:\Users\Drass\plotly dash\webcentral\01_application\webcentral_app\project_listing\Dash_app')



from .Warmelastapproximation_csv import Warmelast
from wetterdienst.provider.dwd.observation import DwdObservationRequest
from django_plotly_dash import DjangoDash
import plotly.express as px  # (version 4.7.0 or higher)
import pandas as pd
from dash import  dcc, html, Input, Output,State  # pip install dash (version 2.0.0 or higher)

import plotly.graph_objects as go
app = DjangoDash('Warmelast')   
#Setting up the resolution for data filtering
Resolution='HOURLY'

#Selecting the dataset

Dataset='AIR_TEMPERATURE'
# Parameter variable selection

Parameter='TEMPERATURE_AIR_MEAN_200'
#Setting up the Period

Period='RECENT'
# Acquiring all the stations that provide data according to selected filters
stations = DwdObservationRequest(
    parameter=Parameter,
    resolution=Resolution,
    period=Period
    )

# App layout
app.layout = html.Div([

    html.H1("WarmeLast Approximation", style={'text-align': 'center'}),
    dcc.Dropdown(
        options=[
                {'label': 'EFH ', 'value': '2'},
                {'label': 'MFH ', 'value': '3'},
                {'label': 'Gebietskörpersch', 'value': '4'},
                {'label': 'Einzelhandel, Großhandel', 'value': '5'},
                {'label': 'Metall, Kfz', 'value': '6'},
                {'label': 'sonst. betr. Dienstleistungen  ', 'value': '7'},
                {'label': 'Gaststätten ', 'value': '8'},
                {'label': 'Beherbergung ', 'value': '9'},
                {'label': 'Bäckereien ', 'value': '10'},
                {'label': 'Wäschereien ', 'value': '11'},
                {'label': 'Gartenbau ', 'value': '12'},
                {'label': 'Papier und Druck ', 'value': '13'},
                {'label': 'haushaltsähnliche Gewerbebetriebe ', 'value': '14'},
                {'label': 'Summenlastprofil Gewerbe, Handel, Dienstleistung ', 'value': '15'},

            ],

        placeholder="Auswahl der Anwendung",
        id='Anwendung'
        ),
    
    dcc.Dropdown(stations.all( ).df['state'].unique(),placeholder="Auswahl der Bundesland",
        id='State'
        ),

    dcc.Dropdown(placeholder="Auswahl der Station",id='Station'
        ),
    dcc.Input(id="Warmebedarf", type="number",placeholder="Jahreswärmebedarfs in kWh/a", debounce=True,style={'width':'200px'}),
    html.Br(),
    dcc.DatePickerRange(
    
    display_format='DD/MM/YYYY',
    #start_date_placeholder_text='DD/MM/YYYY',
    #end_date=datetime.date(2022, 6, 1),    # Add last date coressponding tochosen station
    id='date_picker'),
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
        id='Display_month',
        inline=True
    ),
    dcc.Graph(id='graph2', figure={}),

        
    html.P('Es gibt kein Eingabe ',id='container'),
            



])
# ------------------------------------------------------------------------------
# Connect the Plotly graphs with Dash Components
#Selection of station
@app.callback(Output('Station', 'options'), Input('State', 'value'),prevent_initial_call=True)
def station_selection(value):
    #print(value)
    list=stations.all( ).df['name'].where(stations.all( ).df['state']==value).unique().tolist()
    #print('list')
    return [{"label":row['name'] , "value": row['station_id']} for index,row in stations.all( ).df.iterrows() if row['state']==value]

#Setting of the available date frame
@app.callback(Output('date_picker', 'min_date_allowed'),Output('date_picker', 'max_date_allowed'), Input('Station', 'value'),prevent_initial_call=True)
def date_picker (value):
    data= stations.filter_by_station_id(station_id=value)
    station_data = data.values.all().df.tail(8760)
    min_date=(min(station_data['date'])).date()
    max_date=(max(station_data['date'])).date()
    return min_date, max_date

#Setting Diplay Month
@app.callback(Output('Display_month','options'),Input('date_picker', 'start_date'),Input('date_picker', 'end_date'),prevent_initial_call=True)
def display_month(start_date,end_date):
    Months=pd.date_range(start_date,end_date,freq='W').strftime("%b").unique().tolist()
    display_months=[{"label":index , "value": datetime.datetime.strptime(index, "%b").month} for index in Months ]
    display_months.append ({"label":'All' , "value": 'All'})

    return display_months



#Warme Approximation
@app.callback(
    Output(component_id='graph2', component_property='figure'),
    Output(component_id='container', component_property='children'),
    Input('Anwendung','value'),
    Input('Station','value'),
    Input('Warmebedarf','value'),
    Input('Display_month','value'),
    Input('date_picker','start_date'),
    Input('date_picker','end_date'),prevent_initial_call=True)
    
def update_graph2(Anwendung,Station,Warmebedarf,display,start_date,end_date):
    
        Warme=Warmelast(int(Anwendung),Warmebedarf,Station,start_date,end_date)
        d=Warme[1]
        fehlende_werte=Warme[0]
        if display=='All':
            result=d
        else:
            result={'Last':(d.groupby(d.Time.dt.month).get_group(int(display)))['Last'],'Time':(d.groupby(d.Time.dt.month).get_group(int(display)))['Time'],'fehlend':d['fehlend']}
        result=pd.DataFrame(result)

        fig = go.Figure()

        fig.add_trace(go.Scatter(name='Richtige Eingaben',x=result['Time'], y=result['Last'],mode='lines', line=dict(color="#0000ff")))
        fig.add_trace(go.Scatter(name='Fehlende Eingaben',x=result['Time'], y=result['Last'].where(result['fehlend']=='True'),mode='lines', line=dict(color="red")))

        fig.update_xaxes(
        tickangle = 90,
        title_text = "Datum",
        title_font = {"size": 20},
       )
        fig.update_yaxes(
        title_text = "Last in kW",
        title_standoff = 25)
        return fig, 'Für die ausgewählte Station gibt es '+ str(fehlende_werte)+' fehlende Werte, die in der Grafik rot markiert sind. ' 
    


# ------------------------------------------------------------------------------
# Connect the Plotly graphs with Dash Components







