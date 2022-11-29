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
    dcc.Dropdown(stations.all( ).df['state'].unique(),placeholder="Auswahl der Bundesland",
        id='State'
        ),
      # Dropdown for the available wetterdienst stations in the chosen State
    dcc.Dropdown(placeholder="Auswahl der Station",id='Station'
        ),
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
        id='application'
        ),
    # Input field for the heat_demand in kWh/a      
    dcc.Input(id="Heat_reqruirement", type="number",placeholder="Jahreswärmebedarfs in kWh/a", debounce=True,style={'width':'200px'}),
    html.Br(),
    # Data range picker : choose the date range used for the approximation
    dcc.DatePickerRange(

    display_format='DD/MM/YYYY',
    start_date_placeholder_text='Start Datum',
    end_date_placeholder_text='End Datum',
    #end_date=datetime.date(2022, 6, 1),    # Add last date coressponding tochosen station
    id='date_picker'),
    # List of available display months for the chosen data range
    dcc.RadioItems(
        options=[
                {'label': 'Jan', 'value': '1'},
                {'label': 'Feb', 'value': '2'},
                {'label': 'Mar', 'value': '3'},
                {'label': 'Apr', 'value': '4'},
                {'label': 'Mai', 'value': '5'},
                {'label': 'Jun', 'value': '6'},
                {'label': 'Jul', 'value': '7'},
                {'label': 'Aug', 'value': '8'},
                {'label': 'Sep', 'value': '9'},
                {'label': 'Oct', 'value': '10'},
                {'label': 'Nov', 'value': '11'},
                {'label': 'Dec', 'value': '12'},
                {'label': 'All', 'value': 'All'},
            ],
        value='All',
        id='Display_month',
        inline=True
    ),
    html.Button('Approximation starten', id='Approximation_Start'),
        # Graph
    dcc.Graph(id='Heat_graph', figure={}),

        
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
def date_range_picker (station_id:int) -> tuple[str,str]:
    data= stations.filter_by_station_id(station_id=station_id)
    station_data = data.values.all().df
    min_date=(min(station_data['date'])).date()
    max_date=(max(station_data['date'])).date()

    return min_date, max_date

#Setting Diplay Month
@app.callback(Output('Display_month','options'),Input('date_picker', 'start_date'),Input('date_picker', 'end_date'),prevent_initial_call=True)
# The following function  a list of available months in the data range selected
def display_months(start_date:str,end_date:str)-> list:
    Months=pd.date_range(start_date,end_date,freq='W').strftime("%b").unique().tolist()
   
    # Setting the months in the right format for plotly dash
    display_months=[{"label":index , "value": datetime.datetime.strptime(index, "%b").month} for index in Months ]
    display_months.append ({"label":'All' , "value": 'All'})


    return display_months



#Warme Approximation
@app.callback(
    Output(component_id='Heat_graph', component_property='figure'),
    Output(component_id='container', component_property='children'),
    Input('application','value'),
    Input('Station','value'),
    Input('Heat_reqruirement','value'),
    Input('Display_month','value'),
    Input('date_picker','start_date'),
    Input('date_picker','end_date'),Input('Approximation_Start', 'n_clicks'),prevent_initial_call=True)
# This function calculates the approximations and displays it
def update_Heat_graph(application:str,Station_id:int,Heat_reqruirement:int,Display_month:str,start_date:str,end_date:str,Approximation_Start:int):
    print(type(Approximation_Start))
    if Approximation_Start is None:
        raise PreventUpdate
    else:
        Heat=Warmelast(int(application),Heat_reqruirement,Station_id,start_date,end_date)
        Heat_approximation=Heat[1]
        fehlende_werte=Heat[0]
        WW_Heat_approximation=Heat[2]
        if Display_month=='All':
            result=Heat_approximation
            result2=WW_Heat_approximation
        else:
            result=pd.DataFrame({'Last':(Heat_approximation.groupby(Heat_approximation.Time.dt.month).get_group(int(Display_month)))['Last'],'Time':(Heat_approximation.groupby(Heat_approximation.Time.dt.month).get_group(int(Display_month)))['Time'],'fehlend':Heat_approximation['fehlend']})
            result2=pd.DataFrame({'Last':(WW_Heat_approximation.groupby(WW_Heat_approximation.Time.dt.month).get_group(int(Display_month)))['Last'],'Time':(WW_Heat_approximation.groupby(WW_Heat_approximation.Time.dt.month).get_group(int(Display_month)))['Time'],'fehlend':WW_Heat_approximation['fehlend']})
        from plotly.subplots import make_subplots
        fig = make_subplots(specs=[[{"secondary_y": True}]])

        fig.add_trace(go.Scatter(name='Wärme-lastgang in kW',x=result['Time'], y=result['Last'],mode='lines', line=dict(color="#0000ff")),secondary_y=False)
        fig.add_trace(go.Scatter(name='Fehlende Eingaben',x=result['Time'], y=result['Last'].where(result['fehlend']=='True'),mode='lines', line=dict(color="red")),secondary_y=False)

        fig.add_trace(go.Scatter(name='Trink-WW-Lastgang in kW',x=result2['Time'], y=result2['Last'],mode='lines', line=dict(color="#f700ff")),secondary_y=True)

        fig.update_xaxes(
        tickangle = 90,
        title_text = "Datum",
        title_font = {"size": 20},
       )

        fig.update_yaxes(
        title_text = "Wärme-lastgang in kW",
        title_standoff = 25)
        fig.update_yaxes(
        title_text="Trink-WW-Lastgang in kW", 
        secondary_y=True)
        return fig, 'Für die ausgewählte Station gibt es '+ str(fehlende_werte)+' fehlende Werte, die in der Grafik rot markiert sind. ' 
    


# ------------------------------------------------------------------------------
# Connect the Plotly graphs with Dash Components







