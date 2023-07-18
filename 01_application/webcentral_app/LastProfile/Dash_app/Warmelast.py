import datetime
import locale
import pandas as pd
from typing import Tuple
import plotly.graph_objects as go
from django_plotly_dash import DjangoDash
from dash.exceptions import PreventUpdate
from .Warmelastapproximation_csv import heatLoad , heatLoadreferenceYear
from dash import  dcc, html, Input, Output ,State # pip install dash (version 2.0.0 or higher)
from wetterdienst.provider.dwd.observation import DwdObservationRequest

locale.setlocale(locale.LC_ALL, "de_DE.utf8") # German time

app = DjangoDash('Warmelast')   
#Setting up the resolution for data filtering
resolution = 'HOURLY'

#Selecting the dataset

dataset = 'AIR_TEMPERATURE'
# Parameter variable selection

parameter = 'TEMPERATURE_AIR_MEAN_200'
#Setting up the Period

period = 'RECENT'
# Acquiring all the stations that provide data according to selected filters
stations = DwdObservationRequest(
    parameter = parameter,
    resolution = resolution,
    period = period
    )

# App layout

app.layout = html.Div([
    # Title
    html.H1("Wärmelast Approximation", style = {'text-align': 'center'}),
    html.Div([
        html.P(["Als Testrefenzjahr haben wir die folgenden Werte gewählt:",html.Br(), 
                "Koordinatensystem : Lambert konform konisch",html.Br(), 
                "Rechtswert        : 4201500 Meter",html.Br(), 
                "Hochwert          : 2848500 Meter",html.Br(), 
                "Hoehenlage        : 36 Meter über NN",html.Br(), 
                "Erstellung des Datensatzes im Mai 2016",html.Br(), 
                "Art des TRY       : mittleres Jahr",html.Br(),
                "Bezugszeitraum    : 1995-2012",html.Br(), 
                "Datenbasis        : Beobachtungsdaten Zeitraum 1995-2012" ],id = "container",
            ),
    ],id = 'hideText', style = {'display': 'none'}),
    # Dropdown for the application options
    dcc.Dropdown( 
        options = [
            {'label': 'Testreferenzjahr', 'value': 'on'},
            {'label': 'Wetterstation', 'value': 'off'}     
        ],
        placeholder = "Berechnungstyp",
        id = 'referenceYear',
        value = 'on'
        ),
    html.Div([
    # Dropdown for State options for the Wetterdienst station choice
        dcc.Dropdown(
            stations.all( ).df['state'].unique(),
            placeholder = "Auswahl des Bundesland",
            id = 'state' 
        ),
        # Dropdown for the available wetterdienst stations in the chosen State
        dcc.Dropdown(
            placeholder = "Auswahl der Station",id = 'station'
        )
    ],id = 'hideElements', style = {'display': 'block'}),
    dcc.Dropdown(
        options = [
                {'label': 'Einfamilienhaus ', 'value': '2'},
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
        placeholder = "Auswahl des Gebäudetyps",
        id = 'application',
         # <-- This is the line that will be changed by the dropdown callback
    ),
        
    # Input field for the heat_demand in kWh/a      
    dcc.Input(
        id = "heatRequirement", type = "number",
        placeholder = "Jahreswärmebedarf in kWh/a", 
        debounce = True,style = {'width':'200px'}
    ),
    html.Br(),
    # Data range picker : choose the date range used for the approximation
    dcc.DatePickerRange(
        display_format = ' DD/MM/YYYY',
        start_date_placeholder_text = 'Start Datum',
        end_date_placeholder_text = 'End Datum',
        id = 'datePicker'
    ),
    # List of available display months for the chosen data range
    dcc.RadioItems(
        options = [
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
        value = 'All',
        id = 'displayMonth',
        inline = True
    ),
    html.Button('Approximation starten', id = 'approximation_start'),

    #Download data as csv
    html.Button("Download als csv", id = "btn-download-csv"),
    dcc.Download(id = "download-csv"),
    # Graph
    dcc.Graph(id = 'heat_graph', figure = {}),

    #Display the missing number of missing values from the station data
    html.P('Es gibt kein Eingabe ',id = 'container'),
    dcc.Store(id='heat_approximationStoring')
# style is used to control css output directly from dash 
],style={'font-family': "Roboto, sans-serif","color":"rgb(116, 117, 121)",
         "font-size":" 18.75px",
         "font-weight": "400",
         "line-height": "22.5px"})
# ------------------------------------------------------------------------------
# Connect the Plotly graphs with Dash Components
@app.callback(
   Output(component_id = 'hideText', component_property = 'style'),
   Input(component_id = 'referenceYear', component_property = 'value')
   )

# Hide explanation text for refrenceyear run
def showHideTxt(visibility_state):
    if visibility_state == 'off':
        return {'display': 'none'}
    if visibility_state == 'on':
        return {'display': 'block'}
@app.callback(
   Output(component_id = 'hideElements', component_property = 'style'),
   Input(component_id = 'referenceYear', component_property = 'value')
   )
# Hide unnecessary elements for refrenceyear run
def showHideElement(visibility_state):
    if visibility_state == 'off':
        return {'display': 'block'}
    if visibility_state == 'on':
        return {'display': 'none'}
#Selection of station
@app.callback(
    Output('station', 'options'),
    Input('state', 'value'),
    prevent_initial_call = True
    )
#The following funtion provides the list of available stations in the chosen Bundesland
def stationSelection(state:str) -> list:
    return [{"label":row['name'] , "value": row['station_id']} 
    for index,row in stations.all( ).df.iterrows() if row['state'] == state]


#Setting of the available date frame
@app.callback(
    Output(component_id = 'datePicker',component_property = 'min_date_allowed'),
    Output(component_id = 'datePicker',component_property = 'max_date_allowed'),
    Input(component_id = 'station', component_property = 'value'),
    Input(component_id = 'referenceYear', component_property = 'value'),
    prevent_initial_call = True
    )
# The following function returns the data range provided by the chosen station
def dateRangePicker (stationId:int,referenceYear:str)-> Tuple[str,str] :
    if referenceYear == "on":
        minDate = datetime.datetime.strptime("01/01/2021", "%m/%d/%Y")
        maxDate = datetime.datetime.strptime("12/31/2021", "%m/%d/%Y")
    else:
        data=stations.filter_by_station_id(station_id=stationId)
        stationData = data.values.all().df
        minDate = (min(stationData['date'])).date()
        maxDate = (max(stationData['date'])).date()

    return minDate, maxDate

#Setting Diplay Month
@app.callback(
    Output('displayMonth','options'),
    Input('datePicker', 'start_date'),
    Input('datePicker', 'end_date'),
    prevent_initial_call  = True
    )
# The following function  a list of available months in the data range selected
def displayMonths(startDate:str,endDate:str)-> list:
    Months = pd.date_range(startDate,
    endDate,freq = 'W').strftime("%B").unique().tolist()
    # Setting the months in the right format for plotly dash
    displayMonths = [{"label":index , 
        "value": datetime.datetime.strptime(index, "%B").month} 
        for index in Months ]
    displayMonths.append ({"label":'All' , "value": 'Alle'})

    return displayMonths

#Warme Approximation
@app.callback(
    Output(component_id = 'heat_graph', component_property = 'figure'),
    Output(component_id = 'container',component_property = 'children'),
    Output(component_id = 'heat_approximationStoring',component_property = 'data'),
    Input(component_id = 'application',component_property = 'value'),
    Input(component_id = 'station',component_property = 'value'),
    Input(component_id = 'heatRequirement',component_property = 'value'),
    Input(component_id = 'displayMonth',component_property = 'value'),
    Input(component_id = 'datePicker',component_property = 'start_date'),
    Input(component_id = 'datePicker',component_property = 'end_date'),
    Input(component_id = 'approximation_start',component_property = 'n_clicks'),
    Input(component_id = 'referenceYear', component_property = 'value'),
    prevent_initial_call = True
    )
# This function calculates the approximations and displays it
def updateHeatGraph(application:str,StationId:int,heatRequirement:int,
                    displayMonth:str,startDate:str,endDate:str,approximation_start:int,referenceYear:str):

    if approximation_start is None:
        raise PreventUpdate
    else:
        if referenceYear == "off":
            heat =  heatLoad(int(application),heatRequirement,StationId,startDate,endDate,referenceYear)
        if referenceYear == "on":
            heat = heatLoadreferenceYear(int(application),heatRequirement,startDate,endDate)
        #global heat_approximation
        heatApproximation = heat[1]
        missingValues = heat[0]

        if displayMonth == 'All':
            result = heatApproximation
        else:
            result=pd.DataFrame({'Last':(heatApproximation.groupby
            (heatApproximation.Time.dt.month).get_group(int(displayMonth)))['Last'],
            'WW_Last':(heatApproximation.groupby(heatApproximation.Time.dt.month).
            get_group(int(displayMonth)))['WW_Last'],
            'Time':(heatApproximation.groupby(heatApproximation.Time.dt.month).
            get_group(int(displayMonth)))
            ['Time'],'fehlend':heatApproximation['fehlend']})
        from plotly.subplots import make_subplots
        fig=make_subplots(specs = [[{"secondary_y": True}]])

        fig.add_trace(go.Scatter(name = 'Wärmelastgang in kW',x = result['Time'],
        y = result['Last'],mode = 'lines', line = dict(color = "#0000ff")),secondary_y = False)
        fig.add_trace(go.Scatter(name = 'Fehlende Eingaben',x = result['Time'],
        y = result['Last'].where(result['fehlend'] == 'True'),mode = 'lines',
        line = dict(color = "red")),secondary_y = False)
        fig.add_trace(go.Scatter(name='Trinkwarmwasser-Lastgang in kW',
        x = result['Time'],y = result['WW_Last'],mode = 'lines',
        line = dict(color="#f700ff")),secondary_y = True)

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
        title_text = "Trinkwarmwasser-Lastgang in kW", 
        secondary_y = True
        )
 
        return fig,'Für die ausgewählte Station gibt es ' + str(missingValues) + \
            ' fehlende Werte, die in der Grafik rot markiert sind. ' ,\
            pd.DataFrame.to_dict(heatApproximation)

# The download csv Funcionality
@app.callback(
    Output("download-csv", "data"),
    Input("btn-download-csv", "n_clicks"),
    Input('heat_approximationStoring','data'),
    Input('application','value'),
    Input('heatRequirement','value'),
    Input('datePicker', 'start_date'),
    Input('datePicker', 'end_date'),
    Input('state', 'value'),
    Input('station','value'),
    State('station',"options"),
    State("application","options"),
    prevent_initial_call = True,
)

def downloadAsCsv(nClicks,jsonifiedHeatApproximation:pd.DataFrame,
    application:str,heatRequirement:int,startDate:str,endDate:str,
    state:str,station:str,labelsStation,labelsApplication):
        if not nClicks:
            raise PreventUpdate
        else:
            heatApproximation = pd.DataFrame.from_dict(jsonifiedHeatApproximation)
            labelStation = [x['label'] for x in labelsStation if x['value'] == station]
            labelsApplication = [x['label'] for x in labelsApplication 
            if x['value'] == application]
            heatApproximation.columns = [['Jahreswärmebedarfs in kWh/a :'
            +str(heatRequirement),'','',''  ],['Anwendung:'+labelsApplication[0],'','',''],
            ['Zeitraum : Von '+startDate+' Bis '+endDate,'','',''],
            ['Bundesland:'+state + ' Station:' + labelStation[0] ,'','',''],
            ['','','',''],['Datum','WärmeLast in kW','TrinkwasserWärmeLast in kW',
            'FehlendeWerte(Angepasst)']]    

            return dcc.send_data_frame(heatApproximation.to_csv,'WarmeData.csv',
                                       index=False,encoding = 'utf-8')
# ------------------------------------------------------------------------------
# Connect the Plotly graphs with Dash Components







