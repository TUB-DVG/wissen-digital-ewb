
import datetime
from typing import Tuple

from .Warmelastapproximation_csv import warmelast
from wetterdienst.provider.dwd.observation import DwdObservationRequest
from django_plotly_dash import DjangoDash

import pandas as pd
from dash import  dcc, html, Input, Output ,State # pip install dash (version 2.0.0 or higher)
from dash.exceptions import PreventUpdate
import plotly.graph_objects as go
import locale
locale.setlocale(locale.LC_ALL, "de_DE.utf8") # German time

app = DjangoDash('Warmelast')   
#Setting up the resolution for data filtering
Resolution = 'HOURLY'

#Selecting the dataset

Dataset = 'AIR_TEMPERATURE'
# Parameter variable selection

Parameter = 'TEMPERATURE_AIR_MEAN_200'
#Setting up the Period

Period = 'RECENT'
# Acquiring all the stations that provide data according to selected filters
stations = DwdObservationRequest(
    parameter = Parameter,
    resolution = Resolution,
    period = Period
    )

# App layout

app.layout = html.Div([
    # Title
    html.H1("Wärmelast Approximation", style={'text-align': 'center'}),
    html.Div([
        html.P(["Als Testrefenzjahr haben wir die folgenden Werte gewählt:",html.Br(), 
"Koordinatensystem : Lambert konform konisch",html.Br(), 
"Rechtswert        : 4201500 Meter",html.Br(), 
"Hochwert          : 2848500 Meter",html.Br(), 
"Hoehenlage        : 36 Meter ueber NN",html.Br(), 
"Erstellung des Datensatzes im Mai 2016",html.Br(), 
"Art des TRY       : mittleres Jahr",html.Br(),
"Bezugszeitraum    : 1995-2012",html.Br(), 
"Datenbasis        : Beobachtungsdaten Zeitraum 1995-2012" ],id="container",
),
        ],id='hide_text', style= {'display': 'none'}),
    # Dropdown for the application options
    dcc.Dropdown( options=[
                {'label': 'Standard', 'value': 'on'}, 
                {'label': 'Testrefenzjahr', 'value': 'off'},     
            ],

        placeholder = "Berechnungstyp",
        id = 'referenceyear',
        value = 'on'
        ),
    html.Div([
    # Dropdown for State options for the Wetterdienst station choice
    dcc.Dropdown(stations.all( ).df['state'].unique(),
                 placeholder="Auswahl der Bundesland",
                 id = 'state'
                ),
      # Dropdown for the available wetterdienst stations in the chosen State
    dcc.Dropdown(placeholder="Auswahl der Station",id='station'
        )
         ],id='hide_elements', style= {'display': 'block'}),
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
                {'label': 'Summenlastprofil Gewerbe, Handel, Dienstleistung ',
                  'value': '15'},

            ],

        placeholder = "Auswahl des Typs",
        id = 'application',
         # <-- This is the line that will be changed by the dropdown callback
    ),
        
    # Input field for the heat_demand in kWh/a      
    dcc.Input(id="heat_requirement", type="number",
    placeholder="Jahreswärmebedarfs in kWh/a", 
    debounce=True,style={'width':'200px'}),
    html.Br(),
    # Data range picker : choose the date range used for the approximation
    dcc.DatePickerRange(
    display_format=' DD/MM/YYYY',
    start_date_placeholder_text='Start Datum',
    end_date_placeholder_text='End Datum',
    id = 'date_picker'),
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

    #Download data as csv
    html.Button("Download Csv", id="btn-download-csv"),
    dcc.Download(id="download-csv"),
    # Graph
    dcc.Graph(id='heat_graph', figure={}),

    #Display the missing number of missing values from the station data
    html.P('Es gibt kein Eingabe ',id='container'),
    dcc.Store(id='heat_approximationStoring')
# style is used to control css output directly from dash 
],style={'font-family': "Roboto, sans-serif","color":"rgb(116, 117, 121)","font-size":" 18.75px",
"font-weight": "400",
"line-height": "22.5px"})
# ------------------------------------------------------------------------------
# Connect the Plotly graphs with Dash Components
@app.callback(
   Output(component_id='hide_text', component_property='style'),
   [Input(component_id='referenceyear', component_property='value')])
# Hide explanation text for refrenceyear run
def show_hide_txt(visibility_state):
    if visibility_state == 'on':
        return {'display': 'none'}
    if visibility_state == 'off':
        return {'display': 'block'}
@app.callback(
   Output(component_id='hide_elements', component_property='style'),
   [Input(component_id='referenceyear', component_property='value')])
# Hide unnecessary elements for refrenceyear run
def show_hide_element(visibility_state):
    if visibility_state == 'on':
        return {'display': 'block'}
    if visibility_state == 'off':
        return {'display': 'none'}
#Selection of station
@app.callback(Output('station', 'options'), Input('state', 'value')
              ,prevent_initial_call=True)
#The following funtion provides the list of available stations in the chosen Bundesland
def stationSelection(state:str) -> list:

    return [{"label":row['name'] , "value": row['station_id']} 
    for index,row in stations.all( ).df.iterrows() if row['state']==state]


#Setting of the available date frame
@app.callback(Output(component_id='date_picker',component_property='min_date_allowed'),
              Output(component_id='date_picker',component_property='max_date_allowed'),
              Input(component_id='station', component_property='value'),
              Input(component_id='referenceyear', component_property='value'),
              prevent_initial_call=True
              )
# The following function returns the data range provided by the chosen station
def dateRangePicker (station_id:int,referenceyear:str)-> Tuple[str,str] :
    if referenceyear =="off":
        min_date=datetime.datetime.strptime("01/01/2021", "%m/%d/%Y")
        max_date=datetime.datetime.strptime("12/31/2021", "%m/%d/%Y")
    else:
        data=stations.filter_by_station_id(station_id=station_id)
        station_data=data.values.all().df
        min_date=(min(station_data['date'])).date()
        max_date=(max(station_data['date'])).date()

    return min_date, max_date

#Setting Diplay Month
@app.callback(Output('display_month','options'),Input('date_picker', 'start_date'),
              Input('date_picker', 'end_date'),prevent_initial_call=True)
# The following function  a list of available months in the data range selected
def displayMonths(start_date:str,end_date:str)-> list:
    Months=pd.date_range(start_date,
    end_date,freq='W').strftime("%B").unique().tolist()
    # Setting the months in the right format for plotly dash
    displayMonths=[{"label":index , 
    "value": datetime.datetime.strptime(index, "%B").month} 
    for index in Months ]

    displayMonths.append ({"label":'All' , "value": 'All'})
    return displayMonths

#Warme Approximation
@app.callback(
    Output(component_id='heat_graph', component_property='figure'),
    Output(component_id='container',component_property='children'),
    Output(component_id='heat_approximationStoring',component_property='data'),
    Input(component_id='application',component_property='value'),
    Input(component_id='station',component_property='value'),
    Input(component_id='heat_requirement',component_property='value'),
    Input(component_id='display_month',component_property='value'),
    Input(component_id='date_picker',component_property='start_date'),
    Input(component_id='date_picker',component_property='end_date'),
    Input(component_id='approximation_start',component_property='n_clicks'),
    Input(component_id='referenceyear', component_property='value'),
    prevent_initial_call=True)
# This function calculates the approximations and displays it
def updateHeatGraph(application:str,Station_id:int,heat_requirement:int,
display_month:str,start_date:str,end_date:str,approximation_start:int,referenceyear:str):


    if approximation_start is None:
        raise PreventUpdate
    else:
        #if referenceyear="on":

        heat=warmelast(int(application),heat_requirement,Station_id,start_date,end_date,referenceyear)
        #global heat_approximation
        heat_approximation=heat[1]
        fehlende_werte=heat[0]

        if display_month=='All':
            result=heat_approximation

        else:
            result=pd.DataFrame({'Last':(heat_approximation.groupby
            (heat_approximation.Time.dt.month).get_group(int(display_month)))['Last'],
            'WW_Last':(heat_approximation.groupby(heat_approximation.Time.dt.month).
            get_group(int(display_month)))['WW_Last'],
            'Time':(heat_approximation.groupby(heat_approximation.Time.dt.month).
            get_group(int(display_month)))
            ['Time'],'fehlend':heat_approximation['fehlend']})
        from plotly.subplots import make_subplots
        fig=make_subplots(specs=[[{"secondary_y": True}]])

        fig.add_trace(go.Scatter(name='Wärmelastgang in kW',x=result['Time'],
        y=result['Last'],mode='lines', line=dict(color = "#0000ff")),secondary_y=False)
        fig.add_trace(go.Scatter(name='Fehlende Eingaben',x=result['Time'],
        y=result['Last'].where(result['fehlend']=='True'),mode='lines',
        line=dict(color="red")),secondary_y=False)
        fig.add_trace(go.Scatter(name='Trinkwarmwasser-Lastgang in kW',
        x=result['Time'],y=result['WW_Last'],mode='lines',
        line=dict(color="#f700ff")),secondary_y=True)

        fig.update_xaxes(
        tickangle=90,
        title_text="Datum",
        title_font={"size": 20}
       )

        fig.update_yaxes(
        title_text="Wärmelastgang in kW",
        title_standoff=25
        )
        fig.update_yaxes(
        title_text="Trinkwarmwasser-Lastgang in kW", 
        secondary_y=True
        )
 
        return fig,'Für die ausgewählte Station gibt es ' + str(fehlende_werte) + \
            ' fehlende Werte, die in der Grafik rot markiert sind. ' ,\
            pd.DataFrame.to_dict(heat_approximation)

# The download csv Funcionality
@app.callback(
    Output("download-csv", "data"),
    Input("btn-download-csv", "n_clicks"),
    Input('heat_approximationStoring','data'),
    Input('application','value'),
    Input('heat_requirement','value'),
    Input('date_picker', 'start_date'),
    Input('date_picker', 'end_date'),
    Input('state', 'value'),
    Input('station','value'),
    State('station',"options"),
    State("application","options"),

    prevent_initial_call=True,
)

def downloadAsCsv(n_clicks,jsonified_heat_approximation:pd.DataFrame,
application:str,heat_requirement:int,start_date:str,end_date:str,
state:str,station:str,labels_station,labels_application):
    if not n_clicks:
        raise PreventUpdate
    else:

        heat_approximation =pd.DataFrame.from_dict(jsonified_heat_approximation)
        label_station = [x['label'] for x in labels_station if x['value'] == station]
        label_application = [x['label'] for x in labels_application 
        if x['value'] == application]
        heat_approximation.columns = [['Jahreswärmebedarfs in kWh/a :'
        +str(heat_requirement),'','',''  ],['Anwendung:'+label_application[0],'','',''],
        ['Zeitraum : Von '+start_date+' Bis '+end_date,'','',''],
        ['Bundesland:'+state + ' Station:' + label_station[0] ,'','',''],
        ['','','',''],['Datum','WärmeLast in kW','TrinkwasserWärmeLast in kW',
        'FehlendeWerte(Angepasst)']]    

        return dcc.send_data_frame(heat_approximation.to_csv,'WarmeData.csv',
                                   index=False,encoding='utf-8')
# ------------------------------------------------------------------------------
# Connect the Plotly graphs with Dash Components







