import datetime
import locale

from django.contrib import messages
from django.utils.translation import gettext as _
import pandas as pd
import plotly.graph_objects as go
import dash
from dash import (
    dcc,
    html,
    Input,
    Output,
    State,
)
from django_plotly_dash import DjangoDash
from typing import Tuple
from plotly.subplots import make_subplots
from dash.exceptions import PreventUpdate

from .Warmelastapproximation_csv import heatLoad


locale.setlocale(locale.LC_ALL, "de_DE.utf8")  # German time

app = DjangoDash("Warmelast")

zonelist = [
    "Berlin",
    "Bremerhaven",
    "Dresden",
    "Freiburg",
    "Garmisch Partenkirchen",
    "Göttingen",
    "Hannover",
    "Kiel",
    "München",
    "Nürnberg",
    "Oldenburg",
    "Rostock",
    "Worms",
]
template_option_zone = [{"label": i, "value": i} for i in zonelist]
template_option_year = [
    {"label": "2015", "value": "2015"},
    {"label": "2045", "value": "2045"},
]
template_option_temperature = [
    {"label": _("kalt"), "value": "kalt"},
    {"label": _("normal"), "value": "normal"},
    {"label": _("warm"), "value": "warm"},
]
template_option_application = [
    {"label": _("Einfamilienhaus"), "value": "2"},
    {"label": _("Mehrfamilienhaus"), "value": "3"},
    {"label": _("Gebietskörperschaft"), "value": "4"},
    {"label": _("Einzelhandel, Großhandel"), "value": "5"},
    {"label": _("Metall, Kfz"), "value": "6"},
    {"label": _("sonst. betr. Dienstleistungen"), "value": "7"},
    {"label": _("Gaststätten"), "value": "8"},
    {"label": _("Beherbergung"), "value": "9"},
    {"label": _("Bäckereien"), "value": "10"},
    {"label": _("Wäschereien"), "value": "11"},
    {"label": _("Gartenbau"), "value": "12"},
    {"label": _("Papier und Druck"), "value": "13"},
    {"label": _("haushaltsähnliche Gewerbebetriebe"), "value": "14"},
    {
        "label": _("Summenlastprofil Gewerbe, Handel, Dienstleistung"),
        "value": "15",
    },
]
template_option_displaymonth = [
    {"label": _("Januar"), "value": "1"},
    {"label": _("Februar"), "value": "2"},
    {"label": _("März"), "value": "3"},
    {"label": _("April"), "value": "4"},
    {"label": _("Mai"), "value": "5"},
    {"label": _("Juni"), "value": "6"},
    {"label": _("Juli"), "value": "7"},
    {"label": _("August"), "value": "8"},
    {"label": _("September"), "value": "9"},
    {"label": _("Oktober"), "value": "10"},
    {"label": _("November"), "value": "11"},
    {"label": _("Dezember"), "value": "12"},
    {"label": _("Alle"), "value": "All"},
]
# App layout
app.layout = html.Div(
    [  # Title
        dcc.Store(id="on-load", data="loaded"),
        html.H1(
            _("Wärmelast Approximation"),
            style={"text-align": "center"},
            id="headingApp",
        ),
        # Dropdown for the application options
        dcc.Dropdown(
            options=template_option_year,
            placeholder=_("Berechnungstyp"),
            id="referenceYear",
            value="2015",
        ),
        dcc.Dropdown(
            options=template_option_zone,
            placeholder=_("Auswahl der Zone"),
            id="Zone",
        ),
        dcc.Dropdown(
            options=template_option_temperature,
            placeholder=_("Auswahl der Temperatur"),
            id="Temp",
        ),
        dcc.Dropdown(
            options=template_option_application,
            placeholder=_("Auswahl des Gebäudetyps"),
            id="application",
            # <-- This is the line that will be changed by the dropdown callback
        ),
        # Input field for the heat_demand in kWh/a
        dcc.Input(
            id="heatRequirement",
            type="number",
            placeholder=_("Jahreswärmebedarf in kWh/a"),
            debounce=True,
            style={"width": "200px", "height": "25px"},
        ),
        html.Br(),
        # Data range picker : choose the date range used for the approximation
        dcc.DatePickerRange(
            display_format=" DD/MM/YYYY",
            min_date_allowed="2015-01-01",
            max_date_allowed="2045-12-31",
            start_date_placeholder_text=_("Start Datum"),
            end_date_placeholder_text=_("End Datum"),
            id="datePicker",
        ),
        # List of available display months for the chosen data range
        dcc.RadioItems(
            options=template_option_displaymonth,
            value="All",
            id="displayMonth",
            inline=True,
        ),
        html.Button(_("Approximation starten"), id="approximationStart"),
        # Download data as csv
        html.Button(_("Download als csv"), id="btn-download-csv"),
        dcc.Download(id="download-csv"),
        # Graph
        dcc.Loading(
            id="ls-loading",
            children=[html.Div([dcc.Graph(id="heatGraph", figure={})])],
            type="circle",
            fullscreen=False,
        ),
        # Display the missing number of missing values from the station data
        html.P(_("Es gibt keine Eingabe"), id="containerParagraphAtBottom"),
        dcc.Store(id="heat_approximationStoring"),
        # style is used to control css output directly from dash
    ],
    style={
        "font-family": "Roboto, sans-serif",
        "color": "rgb(116, 117, 121)",
        "font-size": " 18.75px",
        "font-weight": "400",
        "line-height": "22.5px",
        "overflow-x": "hidden",
    },
)
# ------------------------------------------------------------------------------
# Connect the Plotly graphs with Dash Component


# Setting of the available date frame
@app.callback(
    Output(component_id="datePicker", component_property="min_date_allowed"),
    Output(component_id="datePicker", component_property="max_date_allowed"),
    Output(component_id="datePicker", component_property="start_date"),
    Output(component_id="datePicker", component_property="end_date"),
    Input(component_id="referenceYear", component_property="value"),
    prevent_initial_call=True,
)
# The following function returns the data range provided by the chosen station
def dateRangePicker(referenceYear: str) -> Tuple[str, str]:
    referenceYear = int(referenceYear)
    minDate = datetime.datetime.strptime(f"01/01/{referenceYear}", "%m/%d/%Y")
    maxDate = datetime.datetime.strptime(f"12/31/{referenceYear}", "%m/%d/%Y")

    return minDate, maxDate, None, None


# Setting Diplay Month
@app.callback(
    Output("displayMonth", "options"),
    Input("datePicker", "end_date"),
    Input("on-load", "data"),
    State("datePicker", "start_date"),
    # prevent_initial_call  = True,
)
# The following function displays a list of available months in the data range selected
def displayMonths(endDate: str, dataOnLoad, startDate: str) -> list:
    if endDate is None or startDate is None:
        return template_option_displaymonth
    Months = (
        pd.date_range(startDate, endDate, freq="W")
        .strftime("%B")
        .unique()
        .tolist()
    )
    # Setting the months in the right format for plotly dash
    displayMonths = [
        {
            "label": _(index),
            "value": datetime.datetime.strptime(index, "%B").month,
        }
        for index in Months
    ]
    displayMonths.append({"label": _("Alle"), "value": "All"})

    return displayMonths


# Warme Approximation
@app.callback(
    Output(component_id="heatGraph", component_property="figure"),
    Output(
        component_id="containerParagraphAtBottom", component_property="children"
    ),
    Output(component_id="heat_approximationStoring", component_property="data"),
    Input("on-load", "data"),
    Input(component_id="approximationStart", component_property="n_clicks"),
    Input(component_id="displayMonth", component_property="value"),
    State(component_id="application", component_property="value"),
    State(component_id="heatRequirement", component_property="value"),
    State(component_id="datePicker", component_property="start_date"),
    State(component_id="datePicker", component_property="end_date"),
    State(component_id="referenceYear", component_property="value"),
    State(component_id="Zone", component_property="value"),
    State(component_id="Temp", component_property="value"),
    # prevent_initial_call = True
)
# This function calculates the approximations and displays it
def updateHeatGraph(
    onLoadData,
    n_clicks: int,
    displayMonth: str,
    application: str,
    heatRequirement: int,
    startDate: str,
    endDate: str,
    referenceYear: str,
    zone: str,
    temperature: str,
):

    if n_clicks == 0 or n_clicks is None:
        fig = go.Figure()
        return (
            fig,
            _("Es gibt keine Eingabe"),
            pd.DataFrame.to_dict(pd.DataFrame()),
        )

    changed_id = [p["prop_id"] for p in dash.callback_context.triggered][0]
    # Restructure Option 1: Seperate Graph update and calculation
    # Restrucute Option 2: validate,

    heat = heatLoad(
        int(application),
        heatRequirement,
        startDate,
        endDate,
        referenceYear,
        zone,
        temperature,
    )
    # global heat_approximation
    heatApproximation = heat[1]
    missingValues = heat[0]
    if displayMonth == "All":
        result = heatApproximation
    else:
        result = pd.DataFrame(
            {
                "Last": (
                    heatApproximation.groupby(
                        heatApproximation.Time.dt.month
                    ).get_group(int(displayMonth))
                )["Last"],
                "WW_Last": (
                    heatApproximation.groupby(
                        heatApproximation.Time.dt.month
                    ).get_group(int(displayMonth))
                )["WW_Last"],
                "Time": (
                    heatApproximation.groupby(
                        heatApproximation.Time.dt.month
                    ).get_group(int(displayMonth))
                )["Time"],
                "fehlend": heatApproximation["fehlend"],
            }
        )

    fig = make_subplots(specs=[[{"secondary_y": True}]])
    fig.add_trace(
        go.Scatter(
            name=_("Wärmelastgang in kW"),
            x=result["Time"],
            y=result["Last"],
            mode="lines",
            line=dict(color="#0000ff"),
        ),
        secondary_y=False,
    )
    fig.add_trace(
        go.Scatter(
            name=_("Fehlende Angaben"),
            x=result["Time"],
            y=result["Last"].where(result["fehlend"] == "True"),
            mode="lines",
            line=dict(color="red"),
        ),
        secondary_y=False,
    )
    fig.add_trace(
        go.Scatter(
            name=_("Trinkwarmwasser-Lastgang in kW"),
            x=result["Time"],
            y=result["WW_Last"],
            mode="lines",
            line=dict(color="#f700ff"),
        ),
        secondary_y=True,
    )

    fig.update_xaxes(
        tickangle=90, title_text=_("Datum"), title_font={"size": 20}
    )

    fig.update_yaxes(title_text=_("Wärmelastgang in kW"), title_standoff=25)

    fig.update_yaxes(
        title_text=_("Trinkwarmwasser-Lastgang in kW"), secondary_y=True
    )

    return (
        fig,
        _("Für die ausgewählte Station gibt es ")
        + str(missingValues)
        + _(" fehlende Werte, die in der Grafik rot markiert sind. "),
        pd.DataFrame.to_dict(heatApproximation),
    )


# The download csv Funcionality
@app.callback(
    Output("download-csv", "data"),
    Input("btn-download-csv", "n_clicks"),
    Input("heat_approximationStoring", "data"),
    Input("application", "value"),
    Input("heatRequirement", "value"),
    Input("datePicker", "start_date"),
    Input("datePicker", "end_date"),
    State("application", "options"),
    State("Zone", "value"),
    State("Temp", "value"),
    prevent_initial_call=True,
)
def downloadAsCsv(
    nClicks,
    jsonifiedHeatApproximation: pd.DataFrame,
    application: str,
    heatRequirement: int,
    startDate: str,
    endDate: str,
    labelsApplication,
    zone: str,
    temperature: str,
):
    # To Do Add download for Wärmelast
    changed_id = [p["prop_id"] for p in dash.callback_context.triggered][0]
    if "btn-download-csv" in changed_id:
        heatApproximation = pd.DataFrame.from_dict(jsonifiedHeatApproximation)
        labelsApplication = [
            x["label"] for x in labelsApplication if x["value"] == application
        ]
        heatApproximation.columns = [
            [
                "Jahreswaermebedarf in kWh/a :" + str(heatRequirement),
                "",
                "",
                "",
            ],
            ["Anwendung:" + labelsApplication[0], "", "", ""],
            ["Zeitraum : Von " + startDate + " Bis " + endDate, "", "", ""],
            [
                "Zone:",
                zone,
                "Temperature:",
                temperature,
            ],
            ["", "", "", ""],
            [
                "Datum",
                "WaermeLast in kW",
                "TrinkwasserWärmeLast in kW",
                "FehlendeWerte(Angepasst)",
            ],
        ]
        return dcc.send_data_frame(
            heatApproximation.to_csv,
            "WarmeData.csv",
            index=False,
            encoding="utf-8",
        )


# ------------------------------------------------------------------------------
# Connect the Plotly graphs with Dash Components


@app.callback(
    Output("referenceYear", "options"),
    Output("referenceYear", "placeholder"),
    Output("Zone", "options"),
    Output("Zone", "placeholder"),
    Output("Temp", "options"),
    Output("Temp", "placeholder"),
    Output("application", "options"),
    Output("application", "placeholder"),
    Output("heatRequirement", "placeholder"),
    Output("datePicker", "start_date_placeholder_text"),
    Output("datePicker", "end_date_placeholder_text"),
    Output("approximationStart", "children"),
    Output("btn-download-csv", "children"),
    Input("on-load", "data"),
    allow_duplicate=True,
)
def update_layout(data):
    optionsReferenceYear = template_option_year
    placeholderReferenceYear = _("Berechnungstyp")
    optionsZone = template_option_zone
    placeholderZone = _("Auswahl der Zone")
    optionsTemp = template_option_temperature
    placeholderTemp = _("Auswahl der Temperatur")
    optionsDropdown = template_option_application
    placeholderBuildingType = _("Auswahl des Gebäudetyps")
    heatRequirementPlaceholder = _("Jahreswärmebedarf in kWh/a")
    startDatePlaceholderText = _("Start Datum")
    endDatePlaceholderText = _("End Datum")

    buttonLabelApproximationStart = _("Approximation starten")
    buttonLabelDownloadCsv = _("Download als csv")

    return (
        optionsReferenceYear,
        placeholderReferenceYear,
        optionsZone,
        placeholderZone,
        optionsTemp,
        placeholderTemp,
        optionsDropdown,
        placeholderBuildingType,
        heatRequirementPlaceholder,
        startDatePlaceholderText,
        endDatePlaceholderText,
        buttonLabelApproximationStart,
        buttonLabelDownloadCsv,
    )
