import datetime
import locale
from typing import Tuple

import pandas as pd
from django.utils.translation import gettext as _
import plotly.graph_objects as go
import dash 
from django_plotly_dash import DjangoDash
from plotly.subplots import make_subplots
from dash.exceptions import PreventUpdate
from dash import  dcc, html, Input, Output ,State # pip install dash (version 2.0.0 or higher)
from wetterdienst.provider.dwd.observation import DwdObservationRequest

from .Warmelastapproximation_csv import heatLoad

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
    html.H1(_("Wärmelast Approximation"), style = {'text-align': 'center'}, id="headingOfSite"),
    html.Div([
        dcc.Store(id='on-load', data='loaded'),
        html.P([_("Als Testrefenzjahr haben wir die folgenden Werte gewählt") + ":",html.Br(), 
                _("Koordinatensystem") + " : " + _("Lambert konform konisch"),html.Br(), 
                _("Rechtswert") + "        : " + "4201500 " + _("Meter"),html.Br(), 
                _("Hochwert") + "          : 2848500" + _("Meter"),html.Br(), 
                _("Höhenlage") + "        : 36 " + _("Meter über NN"),html.Br(), 
                _("Erstellung des Datensatzes im Mai 2016"),html.Br(), 
                _("Art des TRY") + "       : " + _("mittleres Jahr"),html.Br(),
                _("Bezugszeitraum") + "    : 1995-2012",html.Br(), 
                _("Datenbasis") + "        : " + _("Beobachtungsdaten Zeitraum") + " 1995-2012" ],id = "containerAbove",
            ),
    ],id = 'hideText', style = {'display': 'none'}),
    # Dropdown for the application options
    dcc.Dropdown( 
        options = [
            {'label': _('Testreferenzjahr'), 'value': 'on'},
            {'label': _('Wetterstation'), 'value': 'off'}     
        ],
        placeholder = _("Berechnungstyp"),
        id = 'referenceYear',
        value = 'on'
        ),
    html.Div([
    # Dropdown for State options for the Wetterdienst station choice
        dcc.Dropdown(
            stations.all( ).df['state'].unique(),
            placeholder = _("Auswahl des Bundesland"),
            id = 'state',
        ),
        # Dropdown for the available wetterdienst stations in the chosen State
        dcc.Dropdown(
            placeholder = _("Auswahl der Station"),id = 'station'
        )
    ],id = 'hideElements', style = {'display': 'block'}),
    dcc.Dropdown(
        options = [
                {'label': _('Einfamilienhaus '), 'value': '2'},
                {'label': _('Mehrfamilienhaus '), 'value': '3'},
                {'label': _('Gebietskörperschaft'), 'value': '4'},
                {'label': _('Einzelhandel, Großhandel'), 'value': '5'},
                {'label': _('Metall, Kfz'), 'value': '6'},
                {'label': _('sonst. betr. Dienstleistungen  '), 'value': '7'},
                {'label': _('Gaststätten '), 'value': '8'},
                {'label': _('Beherbergung '), 'value': '9'},
                {'label': _('Bäckereien '), 'value': '10'},
                {'label': _('Wäschereien '), 'value': '11'},
                {'label': _('Gartenbau '), 'value': '12'},
                {'label': _('Papier und Druck '), 'value': '13'},
                {'label': _('haushaltsähnliche Gewerbebetriebe '), 'value': '14'},
                {'label': _('Summenlastprofil Gewerbe, Handel, Dienstleistung '), 'value': '15'},

            ],
        placeholder = _("Auswahl des Gebäudetyps"),
        id = 'application',
         # <-- This is the line that will be changed by the dropdown callback
    ),
        
    # Input field for the heat_demand in kWh/a      
    dcc.Input(
        id = "heatRequirement", type = "number",
        placeholder = _("Jahreswärmebedarf in kWh/a"), 
        debounce = True,style = {'width':'200px','height':'25px'}
    ),
    html.Br(),
    # Data range picker : choose the date range used for the approximation
    dcc.DatePickerRange(
        display_format = ' DD/MM/YYYY',
        start_date_placeholder_text = _('Start Datum'),
        end_date_placeholder_text = _('End Datum'),
        id = 'datePicker'
    ),
    # List of available display months for the chosen data range
    dcc.RadioItems(
        options =[
                {'label': _('Januar'), 'value': '1'},
                {'label': _('Februar'), 'value': '2'},
                {'label': _('März'), 'value': '3'},
                {'label': _('April'), 'value': '4'},
                {'label': _('Mai'), 'value': '5'},
                {'label': _('Juni'), 'value': '6'},
                {'label': _('Juli'), 'value': '7'},
                {'label': _('August'), 'value': '8'},
                {'label': _('Sepember'), 'value': '9'},
                {'label': _('Oktober'), 'value': '10'},
                {'label': _('November'), 'value': '11'},
                {'label': _('Dezember'), 'value': '12'},
                {'label': _('Alle'), 'value': 'All'},
                ],
        value = 'All',
        id = 'displayMonth',
        inline = True
    ),
    html.Button(_('Approximation starten'), id = 'approximationStart'),
    #Download data as csv
    html.Button(_("Download als csv"), id = "btn-download-csv"),
    dcc.Download(id = "download-csv"),
    # Graph
    dcc.Loading(id="ls-loading",
           children=[html.Div([dcc.Graph(id="heatGraph",figure = {})])],
           type="circle",fullscreen=False),
    #Display the missing number of missing values from the station data
    html.P(_('Es gibt keine Eingabe '),id = 'container'),
    dcc.Store(id='heat_approximationStoring')
# style is used to control css output directly from dash 
],style={'font-family': "Roboto, sans-serif","color":"rgb(116, 117, 121)",
         "font-size":" 18.75px",
         "font-weight": "400",
         "line-height": "22.5px",
         "overflow-x": "hidden"})
# ------------------------------------------------------------------------------
# Connect the Plotly graphs with Dash Components

@app.callback(
    Output('application', 'options'),
    Output("application", "placeholder"),
    Output("hideText", "children"),
    Output("headingOfSite", "children"),
    Output("state", "placeholder"),
    Output("station", "placeholder"),
    Output("referenceYear", "placeholder"),
    Output("referenceYear", "options"),
    Output("heatRequirement", "placeholder"),
    Output("displayMonth", "options"),
    Output("approximationStart", "children"),
    Output("btn-download-csv", "children"),
    Output("datePicker", "start_date_placeholder_text"),
    Output("datePicker", "end_date_placeholder_text"),
    Output("container", "children"),
    # Output("headingApp", "children"),
    # Output("powerRequirement", "placeholder"),
    Input('on-load', 'data'),
    allow_duplicate=True,
    # Input('url', 'pathname'),  # Assuming you have a `dcc.Location` component with id='url'
    # prevent_initial_call=True
    )
def update_layout(unsuedArgument):
    optionsMonths =[
                    {'label': _('Januar'), 'value': '1'},
                    {'label': _('Februar'), 'value': '2'},
                    {'label': _('März'), 'value': '3'},
                    {'label': _('April'), 'value': '4'},
                    {'label': _('Mai'), 'value': '5'},
                    {'label': _('Juni'), 'value': '6'},
                    {'label': _('Juli'), 'value': '7'},
                    {'label': _('August'), 'value': '8'},
                    {'label': _('Sepember'), 'value': '9'},
                    {'label': _('Oktober'), 'value': '10'},
                    {'label': _('November'), 'value': '11'},
                    {'label': _('Dezember'), 'value': '12'},
                    {'label': _('Alle'), 'value': 'All'},
                ]
    optionsDropdown = [
            {'label': _('Einfamilienhaus '), 'value': '2'},
            {'label': _('Mehrfamilienhaus '), 'value': '3'},
            {'label': _('Gebietskörperschaft'), 'value': '4'},
            {'label': _('Einzelhandel, Großhandel'), 'value': '5'},
            {'label': _('Metall, Kfz'), 'value': '6'},
            {'label': _('sonst. betr. Dienstleistungen  '), 'value': '7'},
            {'label': _('Gaststätten '), 'value': '8'},
            {'label': _('Beherbergung '), 'value': '9'},
            {'label': _('Bäckereien '), 'value': '10'},
            {'label': _('Wäschereien '), 'value': '11'},
            {'label': _('Gartenbau '), 'value': '12'},
            {'label': _('Papier und Druck '), 'value': '13'},
            {'label': _('haushaltsähnliche Gewerbebetriebe '), 'value': '14'},
            {'label': _('Summenlastprofil Gewerbe, Handel, Dienstleistung '), 'value': '15'},

    ]
    optionsPlaceholder = _("Auswahl des Gebäudetyps") 
    headingOfSite = _("Wärmelast Approximation")
    optionsDisplayMonth =[
            {'label': _('Januar'), 'value': '1'},
            {'label': _('Februar'), 'value': '2'},
            {'label': _('März'), 'value': '3'},
            {'label': _('April'), 'value': '4'},
            {'label': _('Mai'), 'value': '5'},
            {'label': _('Juni'), 'value': '6'},
            {'label': _('Juli'), 'value': '7'},
            {'label': _('August'), 'value': '8'},
            {'label': _('Sepember'), 'value': '9'},
            {'label': _('Oktober'), 'value': '10'},
            {'label': _('November'), 'value': '11'},
            {'label': _('Dezember'), 'value': '12'},
            {'label': _('Alle'), 'value': 'All'},
            ]
    optionsTRY = [
        {'label': _('Testreferenzjahr'), 'value': 'on'},
        {'label': _('Wetterstation'), 'value': 'off'}     
    ]
    placeholderTRY = _("Berechnungstyp")
                # _("Koordinatensystem") + " : " + _("Lambert konform konisch"),html.Br(), 
                # _("Rechtswert") + "        : " + "4201500 " + _("Meter"),html.Br(), 
                # _("Hochwert") + "          : 2848500" + _("Meter"),html.Br(), 
                # _("Höhenlage") + "        : 36 " + _("Meter über NN"),html.Br(), 
                # _("Erstellung des Datensatzes im Mai 2016"),html.Br(), 
                # _("Art des TRY") + "       : " + _("mittleres Jahr"),html.Br(),
                # _("Bezugszeitraum") + "    : 1995-2012",html.Br(), 
                # _("Datenbasis") + "        : " + _("Beobachtungsdaten Zeitraum") + " 1995-2012" ]
    # buttonTextApprStart = 
    paragraphElement = html.P([_("Als Testrefenzjahr haben wir die folgenden Werte gewählt") + ":",html.Br(), 
                _("Koordinatensystem") + " : " + _("Lambert konform konisch"),html.Br(), 
                _("Rechtswert") + "        : " + "4201500 " + _("Meter"),html.Br(), 
                _("Hochwert") + "          : 2848500" + _("Meter"),html.Br(), 
                _("Höhenlage") + "        : 36 " + _("Meter über NN"),html.Br(), 
                _("Erstellung des Datensatzes im Mai 2016"),html.Br(), 
                _("Art des TRY") + "       : " + _("mittleres Jahr"),html.Br(),
                _("Bezugszeitraum") + "    : 1995-2012",html.Br(), 
                _("Datenbasis") + "        : " + _("Beobachtungsdaten Zeitraum") + " 1995-2012" ],id = "containerAbove",
            )
    placeholderOfState = _("Auswahl des Bundesland")
    stationPlaceholder = _("Auswahl der Station")
    placeholderYearDemand = _("Jahreswärmebedarf in kWh/a")
    buttonApprStart = _('Approximation starten')
    downloadCSV = _("Download als csv")
    startDatePlaceholder = _('Start Datum')
    endDatePlaceholder = _('End Datum')
    paragraphPlaceholderTextBelowDiagram = _('Es gibt keine Eingabe ')
    return optionsDropdown, optionsPlaceholder, paragraphElement, headingOfSite, placeholderOfState, stationPlaceholder, placeholderTRY, optionsTRY, placeholderYearDemand, optionsMonths, buttonApprStart, downloadCSV, startDatePlaceholder, endDatePlaceholder, paragraphPlaceholderTextBelowDiagram
    # , 
    # optionsDisplayMonth, optionsTRY, placeholderTRY

    
# Hide explanation text for refrenceyear run
@app.callback(
    Output(component_id = 'datePicker',component_property = 'start_date'),
    Output(component_id = 'datePicker',component_property = 'end_date'),
    Output(component_id = 'heatRequirement',component_property = 'value'),
    Output(component_id = 'application',component_property = 'value'),
    Output(component_id = 'displayMonth', component_property = 'value'),
    Input(component_id = 'referenceYear', component_property = 'value'),
    prevent_initial_call = True,
    allow_duplicate=True,
   )
def resetData(visibility_state):
        return None,None,None,None,'All'
    
# Hide explanation text for refrenceyear run
@app.callback(
    Output(component_id = 'hideText', component_property = 'style'),
    Input(component_id = 'referenceYear', component_property = 'value'),
    allow_duplicate=True,
   )
def showHideTxt(visibility_state):
    if visibility_state == 'off':
        return {'display': 'none'}
    if visibility_state == 'on':
        return {'display': 'block'}

# Hide unnecessary elements for refrenceyear run    
@app.callback(
   Output(component_id = 'hideElements', component_property = 'style'),
   Input(component_id = 'referenceYear', component_property = 'value'),
   allow_duplicate=True,
   )
def showHideElement(visibility_state):
    if visibility_state == 'off':
        return {'display': 'block'}
    if visibility_state == 'on':
        return {'display': 'none'}

#Selection of station
@app.callback(
    Output('station', 'options'),
    Input('state', 'value'),
    prevent_initial_call = True,
    allow_duplicate=True,
    )
#The following funtion provides the list of available stations in the chosen Bundesland
def stationSelection(state:str) -> list:
    return [{"label":row['name'] , "value": row['station_id']} 
    for index,row in stations.all( ).df.iterrows() if row['state'] == state]

#Setting of the available date frame
@app.callback(
    Output(component_id = 'datePicker',component_property = 'min_date_allowed'),
    Output(component_id = 'datePicker',component_property = 'max_date_allowed'),
    Input(component_id = 'referenceYear', component_property = 'value'),
    Input(component_id = 'station', component_property = 'value'),
    allow_duplicate=True,
    )
# The following function returns the data range provided by the chosen station
def dateRangePicker (referenceYear:str,stationId:int)-> Tuple[str,str] :
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
    Output('displayMonth','options', allow_duplicate=True),
    Input('datePicker', 'end_date'),
    State('datePicker', 'start_date'),
    allow_duplicate=True,
    prevent_initial_call  = True
    )
# The following function displays a list of available months in the data range selected
def displayMonths(endDate:str,startDate:str)-> list:
    Months = pd.date_range(startDate,
    endDate,freq = 'W').strftime("%B").unique().tolist()
    # Setting the months in the right format for plotly dash
    displayMonths = [{"label":index , 
        "value": datetime.datetime.strptime(index, "%B").month} 
        for index in Months ]
    displayMonths.append ({"label":'Alle' , "value": 'All'})

    return displayMonths

#Warme Approximation
@app.callback(
    Output(component_id = 'heatGraph', component_property = 'figure'),
    Output(component_id = 'containerAbove',component_property = 'children', allow_duplicate=True),
    Output(component_id = 'heat_approximationStoring',component_property = 'data'),
    Input(component_id = 'approximationStart',component_property = 'n_clicks'),
    Input(component_id = 'displayMonth',component_property = 'value'),
    State(component_id = 'application',component_property = 'value'),
    State(component_id = 'station',component_property = 'value'),
    State(component_id = 'heatRequirement',component_property = 'value'),
    State(component_id = 'datePicker',component_property = 'start_date'),
    State(component_id = 'datePicker',component_property = 'end_date'),
    State(component_id = 'referenceYear', component_property = 'value'),
    prevent_initial_call = True,
    allow_dublicate=True,
    )
# This function calculates the approximations and displays it
def updateHeatGraph(n_clicks:int,displayMonth:str,application:str,StationId:int,heatRequirement:int,
                    startDate:str,endDate:str,referenceYear:str):

    changed_id = [p['prop_id'] for p in dash.callback_context.triggered][0] 
    # Restructure Option 1: Seperate Graph update and calculation
    # Restrucute Option 2: validate, 
   
    heat =  heatLoad(int(application),heatRequirement,StationId,startDate,endDate,referenceYear)
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
    
    fig=make_subplots(specs = [[{"secondary_y": True}]])
    fig.add_trace(go.Scatter(name = _('Wärmelastgang in kW'),x = result['Time'],
    y = result['Last'],mode = 'lines', line = dict(color = "#0000ff")),secondary_y = False)
    fig.add_trace(go.Scatter(name = _('Fehlende Angaben'),x = result['Time'],
    y = result['Last'].where(result['fehlend'] == 'True'),mode = 'lines',
    line = dict(color = "red")),secondary_y = False)
    fig.add_trace(go.Scatter(name=_('Trinkwarmwasser-Lastgang in kW'),
    x = result['Time'],y = result['WW_Last'],mode = 'lines',
    line = dict(color="#f700ff")),secondary_y = True)

    fig.update_xaxes(
    tickangle = 90,
    title_text = _("Datum"),
    title_font = {"size": 20}
    )

    fig.update_yaxes(
    title_text = _("Wärmelastgang in kW"),
    title_standoff = 25
    )

    fig.update_yaxes(
    title_text = _("Trinkwarmwasser-Lastgang in kW"),
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
    Input('referenceYear', 'value'),
    State('station',"options"),
    State("application","options"), 
    prevent_initial_call = True,
)
def downloadAsCsv(nClicks,jsonifiedHeatApproximation:pd.DataFrame,
    application:str,heatRequirement:int,startDate:str,endDate:str,
    state:str,station:str,referenceYear:str, labelsStation,labelsApplication, ):
    #To Do Add download for Wärmelast 
    changed_id = [p['prop_id'] for p in dash.callback_context.triggered][0]      
    if 'btn-download-csv' in changed_id:
            if referenceYear == "off":
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
            if referenceYear == "on":
                heatApproximation = pd.DataFrame.from_dict(jsonifiedHeatApproximation)  
            return dcc.send_data_frame(heatApproximation.to_csv,'WarmeData.csv',
                                       index=False,encoding = 'utf-8')
# ------------------------------------------------------------------------------
# Connect the Plotly graphs with Dash Components







