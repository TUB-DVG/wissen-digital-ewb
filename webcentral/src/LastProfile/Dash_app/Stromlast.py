import os
import pathlib

import pandas as pd
import plotly.graph_objects as go
from project_listing.models import *
from django_plotly_dash import DjangoDash
from dash.exceptions import PreventUpdate
from django.utils.translation import gettext as _
from django.contrib.sessions.models import Session
import dash
from dash import (
    dcc,
    html,
    Input,
    Output,
    State,
)  # pip install dash (version 2.0.0 or higher)

from .Stromlastapproximation_Csv import currentApproximation

PATH = pathlib.Path(__file__).parent.resolve()
DATA_PATH = os.path.join(PATH, "Hauptblatt2.csv")
DF_MAIN = pd.read_csv(DATA_PATH)
data = []
app = DjangoDash("Stromlast")  # replaces dash.Dash
# App layout
app.layout = html.Div(
    [
        # Title
        dcc.Store(id="on-load", data="loaded"),
        html.H1(
            _("Stromlast Approximation"),
            style={"text-align": "center"},
            id="headingApp",
        ),
        # Dropdown for the available applications
        dcc.Dropdown(
            options=[
                {"label": _("Gewerbe allgemein "), "value": "2"},
                {"label": _("Gewerbe werktags 8-18 "), "value": "3"},
                {"label": _("Gewerbe Verbrauch Abend"), "value": "4"},
                {"label": _("Gewerbe durchlaufend"), "value": "5"},
                {"label": _("Laden Friseur  "), "value": "6"},
                {"label": _("Bäckerei mit Backstube "), "value": "7"},
                {"label": _("Wochenendbetrieb "), "value": "8"},
                {"label": _("Haushaltskunden "), "value": "9"},
                {"label": _("Landwirtschaftsbetriebe "), "value": "10"},
                {
                    "label": _("Landwirts. mit Milchwirts Tierzucht "),
                    "value": "11",
                },
                {"label": _("Übrige Landwirtschaftsbe "), "value": "12"},
            ],
            id="application",
        ),
        # Input Field for the
        dcc.Input(
            id="powerRequirement",
            type="number",
            placeholder=_("Jahresstrombedarf in kWh/a"),
            style={"width": "200px"},
            debounce=True,
        ),
        dcc.RadioItems(
            options=[
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
                {"label": "All", "value": "All"},
            ],
            value="All",
            id="displayMonth",
            inline=True,
        ),
        html.Button(
            _("Approximation starten"), id="approximation_start", n_clicks=0
        ),
        # Download data as csv
        html.Button(_("Download als csv"), id="btnDownloadCsv"),
        dcc.Download(id="downloadCsv"),
        # Graph
        dcc.Loading(
            id="ls-loading",
            children=[html.Div([dcc.Graph(id="powerGraph", figure={})])],
            type="circle",
            fullscreen=False,
        ),
        # style is used to control css output directly from dash
    ],
    style={
        "font-family": "Roboto, sans-serif",
        "color": "rgb(116, 117, 121)",
        "font-size": " 18.75px",
        "font-weight": "400",
        "line-height": "22.5px",
    },
)
# ------------------------------------------------------------------------------
# Connect the Plotly graph with Dash Components


@app.callback(
    Output("application", "options"),
    Output("displayMonth", "options"),
    Output("approximation_start", "children"),
    Output("btnDownloadCsv", "children"),
    Output("headingApp", "children"),
    Output("powerRequirement", "placeholder"),
    Input("on-load", "data"),
    allow_duplicate=True,
    # Input('url', 'pathname'),  # Assuming you have a `dcc.Location` component with id='url'
    # prevent_initial_call=True
)
def update_layout(hi):
    optionsDropdown = [
        {"label": _("Gewerbe allgemein "), "value": "2"},
        {"label": _("Gewerbe werktags 8-18 "), "value": "3"},
        {"label": _("Gewerbe Verbrauch Abend"), "value": "4"},
        {"label": _("Gewerbe durchlaufend"), "value": "5"},
        {"label": _("Laden Friseur  "), "value": "6"},
        {"label": _("Bäckerei mit Backstube "), "value": "7"},
        {"label": _("Wochenendbetrieb "), "value": "8"},
        {"label": _("Haushaltskunden "), "value": "9"},
        {"label": _("Landwirtschaftsbetriebe "), "value": "10"},
        {"label": _("Landwirts. mit Milchwirts Tierzucht "), "value": "11"},
        {"label": _("Übrige Landwirtschaftsbe "), "value": "12"},
    ]
    optionsRadio = [
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
        {"label": "All", "value": "All"},
    ]
    buttonLabelApproximationStart = _("Approximation starten")
    buttonLabelDownloadCsv = _("Download als csv")
    headingApp = _("Stromlast Approximation")
    placeholderInput = _("Jahresstrombedarf in kWh/a")
    # Set the labels of the dropdown options and radio items based on the current language
    return (
        optionsDropdown,
        optionsRadio,
        buttonLabelApproximationStart,
        buttonLabelDownloadCsv,
        headingApp,
        placeholderInput,
    )


# Stromapproximation
@app.callback(
    Output("powerGraph", "figure"),
    # Output('application', 'children'),
    # Output('application', 'children'),
    Input("approximation_start", "n_clicks"),
    Input("displayMonth", "value"),
    Input("powerRequirement", "value"),
    Input("application", "value"),
    allow_duplicate=True,
    # Input('url', 'pathname'),
    # prevent_initial_call=True
)
def updatePowerGraph(
    click: int,
    displayMonth: str,
    powerRequirement: int,
    application: str,
):

    # breakpoint()
    if application != None:
        WW = currentApproximation(int(application), powerRequirement)
        days = DF_MAIN["Datum/ Uhrzeit"]
        global data
        data = {"Time": days[0:8760], "Last": WW}
        data = pd.DataFrame(data)
        data["Time"] = pd.to_datetime(data["Time"], errors="coerce")
        if displayMonth == "All":
            result = data
        else:
            result = {
                "Last": (
                    data.groupby(data.Time.dt.month).get_group(
                        int(displayMonth)
                    )
                )["Last"],
                "Time": (
                    data.groupby(data.Time.dt.month).get_group(
                        int(displayMonth)
                    )
                )["Time"],
            }
        from plotly.subplots import make_subplots

        fig = make_subplots()
        fig.add_trace(
            go.Scatter(
                name="Stromlastgang in kW",
                x=result["Time"],
                y=result["Last"],
                mode="lines",
                line=dict(color="#0000ff"),
            )
        )

        fig.update_xaxes(
            tickangle=90, title_text=_("Datum"), title_font={"size": 20}
        )

        fig.update_yaxes(title_text=_("Stromlastgang in kW"), title_standoff=25)
        return fig
    else:
        return {}


# The download csv Funcionality
@app.callback(
    Output("downloadCsv", "data"),
    Output("application", "children"),
    Input("btnDownloadCsv", "n_clicks"),
    Input("application", "value"),
    Input("powerRequirement", "value"),
    State("application", "options"),
    prevent_initial_call=True,
)
def downloadAsCsv(nClicks, application: str, powerRequirement: int, state):
    if not nClicks:
        raise PreventUpdate
    else:
        label = [x["label"] for x in state if x["value"] == application]
        data.columns = [
            [_("Jahresstrombedarf in KWh/a :") + str(powerRequirement), ""],
            [_("Anwendung: ") + label[0], ""],
            ["", ""],
            [_("Datum"), _("Last")],
        ]
        return dcc.send_data_frame(
            data.to_csv, "Stromlastgang.csv", index=False
        )


# ------------------------------------------------------------------------------
# Connect the Plotly powerGraphs with Dash Components
