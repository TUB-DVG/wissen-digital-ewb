from cmath import nan
from turtle import title
import pandas as pd
import datetime
from typing import Tuple


from .Warmelastapproximation_csv import warmelast
from wetterdienst.provider.dwd.observation import DwdObservationRequest
from django_plotly_dash import DjangoDash


import pandas as pd
from dash import  dcc, html, Input, Output  # pip install dash (version 2.0.0 or higher)
from dash.exceptions import PreventUpdate
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
    # Title
    html.H1("Wärmelast Approximation", style={'text-align': 'center'}),
    # Dropdown for the application options
   
    # Dropdown for State options for the Wetterdienst station choice
    dcc.Dropdown(stations.all( ).df['state'].unique(),placeholder="Auswahl des Bundeslands",
        id='State'
        ),
      # Dropdown for the available wetterdienst stations in the chosen State
    dcc.Dropdown(placeholder="Auswahl der Station",id='Station'
        ),
     dcc.Dropdown(
        options=[
                {'label': 'Einfamlienhaus ', 'value': '2'},
                {'label': 'Mehrfamilienhaus ', 'value': '3'},
                {'label': 'Gebietskörperschaft', 'value': '4'},
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

        placeholder="Auswahl des Typs",
        id='application'
        ),
    # Input field for the heat_demand in kWh/a      
    dcc.Input(id="heat_requirement", type="number",placeholder="Jahreswärmebedarf in kWh/a", debounce=True,style={'width':'200px'}),
    html.Br(),
    # Data range picker : choose the date range used for the approximation
    dcc.DatePickerRange(

    display_format='DD/MM/YYYY',
    start_date_placeholder_text='Start Datum',
    end_date_placeholder_text='End Datum',
    id='date_picker'),
    # List of available display months for the chosen data range
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
                {'label': 'Sepember', 'value': '9'},
                {'label': 'Oktober', 'value': '10'},
                {'label': 'November', 'value': '11'},
                {'label': 'Dezember', 'value': '12'},
                {'label': 'Alle', 'value': 'All'},
            ],
        value='All',
        id='display_month',
        inline=True
    ),
    html.Button('Approximation starten', id='approximation_start'),
    # Graph
    dcc.Graph(id='heat_graph', figure={}),

    #Display the missing number of missing values from the station data
    html.P('Es gibt kein Eingabe ',id='container'),
            



])
# ------------------------------------------------------------------------------
# Connect the Plotly graphs with Dash Components
#Selection of station
@app.callback(Output('Station', 'options'), Input('State', 'value'),prevent_initial_call=True)
#The following funtion provides the list of available stations in the chosen Bundesland
def station_selection(State:str) -> list:

    return [{"label":row['name'] , "value": row['station_id']} for index,row in stations.all( ).df.iterrows() if row['state']==State]

#Setting of the available date frame
@app.callback(Output('date_picker', 'min_date_allowed'),Output('date_picker', 'max_date_allowed'), Input('Station', 'value'),prevent_initial_call=True)
# The following function returns the data range provided by the chosen station
def date_range_picker(station_id:int) -> Tuple[str,str]:
    data= stations.filter_by_station_id(station_id=station_id)
    station_data = data.values.all().df
    min_date=(min(station_data['date'])).date()
    max_date=(max(station_data['date'])).date()

    return min_date, max_date

#Setting Diplay Month
@app.callback(Output('display_month','options'),Input('date_picker', 'start_date'),Input('date_picker', 'end_date'),prevent_initial_call=True)
# The following function  a list of available months in the data range selected
def display_months(start_date:str,end_date:str)-> list:
    Months=pd.date_range(start_date,end_date,freq='W').strftime("%b").unique().tolist()
   
    # Setting the months in the right format for plotly dash
    display_months=[{"label":index , "value": datetime.datetime.strptime(index, "%b").month} for index in Months ]
    display_months.append ({"label":'All' , "value": 'All'})


    return display_months

#Warme Approximation
@app.callback(
    Output(component_id='heat_graph', component_property='figure'),
    Output(component_id='container', component_property='children'),
    Input('application','value'),
    Input('Station','value'),
    Input('heat_requirement','value'),
    Input('display_month','value'),
    Input('date_picker','start_date'),
    Input('date_picker','end_date'),Input('approximation_start', 'n_clicks'),prevent_initial_call=True)
# This function calculates the approximations and displays it
def update_heat_graph(application:str,Station_id:int,heat_requirement:int,display_month:str,start_date:str,end_date:str,approximation_start:int):
    #print(type(Approximation_Start))
    if approximation_start is None:
        raise PreventUpdate
    else:
        heat=warmelast(int(application),heat_requirement,Station_id,start_date,end_date)
        heat_approximation=heat[1]
        fehlende_werte=heat[0]
        ww_heat_approximation=heat[2]
        if display_month=='All':
            result=heat_approximation
            result2=ww_heat_approximation
        else:
            result=pd.DataFrame({'Last':(heat_approximation.groupby(heat_approximation.Time.dt.month).get_group(int(display_month)))['Last'],'Time':(heat_approximation.groupby(heat_approximation.Time.dt.month).get_group(int(display_month)))['Time'],'fehlend':heat_approximation['fehlend']})
            result2=pd.DataFrame({'Last':(ww_heat_approximation.groupby(ww_heat_approximation.Time.dt.month).get_group(int(display_month)))['Last'],'Time':(ww_heat_approximation.groupby(ww_heat_approximation.Time.dt.month).get_group(int(display_month)))['Time'],'fehlend':ww_heat_approximation['fehlend']})
        from plotly.subplots import make_subplots
        fig = make_subplots(specs=[[{"secondary_y": True}]])

        fig.add_trace(go.Scatter(name='Wärmelastgang in kW',x=result['Time'], y=result['Last'],mode='lines', line=dict(color="#0000ff")),secondary_y=False)
        fig.add_trace(go.Scatter(name='Fehlende Eingaben',x=result['Time'], y=result['Last'].where(result['fehlend']=='True'),mode='lines', line=dict(color="red")),secondary_y=False)
        fig.add_trace(go.Scatter(name='Trinkwarmwasser-Lastgang in kW',x=result2['Time'], y=result2['Last'],mode='lines', line=dict(color="#f700ff")),secondary_y=True)

        fig.update_xaxes(
        tickangle = 90,
        title_text = "Datum",
        title_font = {"size": 20}
       )

        fig.update_yaxes(
        title_text = "Wärmelastgang in kW",
        title_standoff = 25
        )
        fig.update_yaxes(
        title_text="Trinkwarmwasser-Lastgang in kW", 
        secondary_y=True
        )
        return fig, 'Für die ausgewählte Station gibt es '+ str(fehlende_werte)+' fehlende Werte, die in der Grafik rot markiert sind. ' 
    
# ------------------------------------------------------------------------------
# Connect the Plotly graphs with Dash Components







