import os
import pathlib
import regex as re
import pandas as pd
import numpy as np
import itertools
import plotly.graph_objects as go
from django_plotly_dash import DjangoDash
from dash.exceptions import PreventUpdate
from django.utils.translation import gettext as _
from django.contrib.sessions.models import Session
import dash
from dash import dcc, html, Input, Output, State


PATH = pathlib.Path(__file__).parent.resolve()
data_directory = os.path.join(PATH, "auxillary")
file_path = os.path.join(data_directory, "2024-03-18_MonitoringSurvey.csv")


def change_values(df):

    # change the value to name of tools
    for col in df.columns:
        df[col] = df[col].replace(
            {"nicht gewählt": np.nan, "ausgewählt": col.split(": ")[-1]}
        )

    # change certain values
    df.replace(
        to_replace=r"(?i).?phyton.?", value="Python", inplace=True, regex=True
    )
    df.replace(
        to_replace=r"(?i).?matlab.?", value="MATLAB", inplace=True, regex=True
    )
    df.replace(
        to_replace=r"(?i).?mondas.?", value="Mondas", inplace=True, regex=True
    )
    df.replace(
        to_replace=r"(?i).?nicht zutreffend.?",
        value=np.nan,
        inplace=True,
        regex=True,
    )
    # df.replace(to_replace=r'(?i).?python.?', value='Python', inplace=True, regex=True)
    df.replace(
        to_replace=r"(?i).?speziell.*kirchen.*",
        value="Software für Kirchenbauten",
        inplace=True,
        regex=True,
    )
    return df


def read_and_process_excel(file_path):
    # read Excel file, named by row[1]
    df = pd.read_csv(file_path, header=1, sep=";")
    # manuell, drop certain rows
    # drop_certain_rows(df)
    # regress select columns
    columns_regex = r"({})".format(
        "|".join(
            [
                "Interview-Nummer",
                "Software für Monitoring: ",
                "Datenbank: ",
                "Visualisierung: ",
                "Messkonzept: ",
                "Datenpunkte: ",
                "Protokolle: ",
                "Programmiersprache: ",
            ]
        )
    )

    df = df.filter(regex=columns_regex)

    anzahlcols = df.filter(regex=r"Anzahl").columns
    df_temp = pd.DataFrame(columns=anzahlcols)

    for col in df_temp.columns:
        df_temp.loc[0, col] = int(df[col].sum())
        # rename conlums
    df_temp.columns = [
        col.split(":")[0] if ":" in col else col for col in df_temp.columns
    ]

    # delete the columns end with 'Anzahl', 'Eigene', 'Sonstige', or 'Entwicklung'
    df.drop(
        columns=df.filter(
            regex=r"Anzahl|(Eigene|Sonstige|Entwicklung)$"
        ).columns,
        inplace=True,
    )

    # manuell,change certain values
    df = change_values(df)

    # delete the rows which are all blank columns
    # print(df.isnull().sum(axis=1))

    df.dropna(thresh=int(2), inplace=True)

    # print(df.isnull().sum(axis=1))
    df_temp.loc[0, "entries"] = len(df.iloc[:, 0].dropna())
    df_temp["entries"] = df_temp["entries"].astype(int)

    print(df_temp)

    return df, df_temp


def expand_row_combinations(row, df_columns):
    split_values = [str(x).split(";") for x in row]
    combinations = list(itertools.product(*split_values))
    expanded_rows = [list(comb) for comb in combinations]
    return pd.DataFrame(expanded_rows, columns=df_columns)


def data_relation_process(df):
    # copy file
    df_temp = df.copy()
    # rename conlums
    df_temp.columns = [
        col.split(":")[0] if ":" in col else col for col in df_temp.columns
    ]

    # combine the columns with same name
    unique_columns = df_temp.columns.unique()
    df_relation = pd.DataFrame()
    for col in unique_columns:
        try:
            df_relation[col] = df_temp[col].agg(
                lambda row: ";".join(
                    filter(None, row.dropna().astype(str).unique())
                ),
                axis=1,
            )
        except:
            df_relation[col] = df_temp[col]
    # df_temp = df_temp.groupby(by=df_temp.columns, axis=1).agg(lambda x: ';'.join(x.dropna().astype(str)))

    # operate the value with ';'
    rows_list = []
    for index, row in df_relation.iterrows():
        expanded_rows = expand_row_combinations(row, df_relation.columns)
        rows_list.append(expanded_rows)

    df_relation = pd.concat(rows_list, ignore_index=True)

    return df_relation


def combiTimes(df_relation, columnname="Interview"):

    columns_matched = df_relation.filter(regex=columnname).columns.tolist()

    if not columns_matched:
        raise ValueError(f"No columns match the pattern '{columnname}'.")

    column = columns_matched[0]
    counts = df_relation[column].value_counts()

    df_relation[column] = df_relation[column].map(counts)
    return df_relation


def get_node_color(node_name, color_map, colorred=220):

    if "Keine Antwort ausgewählt" in node_name:
        return f"rgba({colorred}, 50, 50, 0.8)"  # red
    return color_map.get(node_name, color_map)


def add_br_tag_with_ellipsis(s, max_length=20):
    """
    Given a string s, if its length is over max_length,
    truncates it and adds '...' at the end.
    If the length is less than or equal to max_length but over 70,
    finds the first space after around 70 characters and adds the <br> tag to the space.
    """
    if len(s) <= max_length:
        return s
    elif len(s) <= (max_length * 2):
        # Find the first space after around 70 characters
        space_pos = s.find(" ", max_length)
        if space_pos == -1:
            return s
        else:
            # Insert the <br> tag
            return s[:space_pos] + " <br>" + s[space_pos + 1 :]
    else:
        # Truncate and add ellipsis
        space_pos1 = s.find(" ", max_length)
        space_pos2 = s.find(" ", max_length * 2, space_pos1 + 1)
        if space_pos1 == -1:
            return s[:max_length].rstrip() + "..."

        elif space_pos2 == -1:
            return (
                s[:space_pos1]
                + " <br>"
                + s[space_pos1 + 1 : max_length * 2]
                + "..."
            )

        else:
            return (
                s[:space_pos1]
                + " <br>"
                + s[space_pos1 + 1 : space_pos2]
                + "..."
            )


def create_sankey(
    df_relation, df_anzahl, opacity, max_length, colorred, combiTimes=False
):
    # init lists and dicts

    node_indices = {}
    link_counts = {}
    node_weights = {}

    # row>col, count times of each type of link
    for _, row in df_relation.iterrows():
        prev_node = None
        for i, col in enumerate(df_relation.columns[1:]):  # jump first col
            current_node = (
                row[col]
                if row[col] not in [None, ""]
                else "Keine Antwort ausgewählt"
            )
            node_key = f"{col}:{add_br_tag_with_ellipsis(current_node,max_length)}"  # make nodes of each col do not conflict with thesame tool from other col

            # count node_weights
            node_weights[node_key] = node_weights.get(node_key, 0) + 1 / (
                row.iloc[0] ** combiTimes
            )  # adjust

            if prev_node is not None:
                link_key = (prev_node, node_key)
                link_counts[link_key] = link_counts.get(link_key, 0) + 1 / (
                    row.iloc[0] ** combiTimes
                )  # adjust
                # print(link_counts[link_key])
            prev_node = node_key
            # print(1/(row.iloc[0]**combiTimes))

    # sorte nodes by nodes_weights
    sorted_nodes = sorted(node_weights, key=node_weights.get, reverse=True)
    node_indices = {node: i for i, node in enumerate(sorted_nodes)}

    # create links
    links = [
        {
            "source": node_indices[source],
            "target": node_indices[target],
            "value": count,
        }
        for (source, target), count in link_counts.items()
    ]

    # create nodes list
    nodes = [key.split(":")[1] for key in sorted_nodes]

    # map color for each uniq node
    unique_names = list(set(nodes))
    color_palette = [
        f"rgba({np.random.randint(0, 150)}, {np.random.randint(50, 255)}, {np.random.randint(50, 255)}, 0.8)"
        for _ in unique_names
    ]
    color_map = dict(zip(unique_names, color_palette))
    node_colors = [get_node_color(node, color_map, colorred) for node in nodes]

    # read column name
    column_names = df_relation.columns.tolist()[1:]

    # caculate percent value due to len（col)
    num_columns = len(column_names)
    column_positions = [i / (num_columns - 1) for i in range(num_columns)]

    annotations = []
    for name, pos in zip(column_names, column_positions):
        annotations.append(
            dict(
                x=pos,
                y=1.15,  # adjust
                xref="paper",
                yref="paper",
                text=add_br_tag_with_ellipsis(f"{name}: ", 30)
                + "<br>"
                + f"{df_anzahl.loc[0,name]} Antworten",
                # text= add_br_tag_with_ellipsis(f'{name}: ', 30) + '<br>' + f'{len(df_relation[name].unique())} nodes;' +'<br>' + f'{df_anzahl.loc[0,name]} entries',
                showarrow=False,
                font=dict(size=16, color="black"),
                align="center",
            )
        )

    # create diagram
    fig = go.Figure(
        data=[
            go.Sankey(
                node=dict(
                    pad=15,
                    thickness=20,
                    line=dict(color="black", width=0.5),
                    label=nodes,
                    color=node_colors,
                ),
                link=dict(
                    source=[link["source"] for link in links],
                    target=[link["target"] for link in links],
                    value=[link["value"] for link in links],
                    color=f"rgba(50, 115, 220, {opacity})",
                    # color=([f'rgba(50, 115, 220, {np.clip(val, 0, 0.2)})' for val in [link['value'] for link in links]] if combiTimes else 'rgba(50, 115, 220, 0.2)')
                ),
            )
        ]
    )

    unique_nodes = len(set([node for node in nodes if node is not None]))
    if combiTimes:
        title = f'Projektgewichtung Normalisierung. An der Befragung haben {df_anzahl.loc[0,"entries"]} Forschungsprojekte teilgenommen.'
        # title = f'Projektgewichtung Normalisierung mit {unique_nodes} gültigen Werkzeugen und {df_anzahl.loc[0,"entries"]} gültigen Antworten.'
    else:
        title = f'Links Gewichtung Normalisierung. An der Befragung haben {df_anzahl.loc[0,"entries"]} Forschungsprojekte teilgenommen.'
        # title = f'Links Gewichtung Normalisierung mit {unique_nodes} gültigen Werkzeugen und {df_anzahl.loc[0,"entries"]} gültigen Antworten.'

    fig.update_layout(
        annotations=annotations,
        width=1600,
        height=800,
        title_text=title,
        # font_size=10,
        title_x=0.5,
        title_y=0.02,
    )
    # add splitting line
    fig.add_annotation(
        x=0.5,
        y=1.1,
        xref="paper",
        yref="paper",
        text="<span style='font-size:40px;border-bottom:2px solid blue;'>____________________________________________________________________________________________</span>",
        showarrow=False,
        align="center",
    )

    return fig


app = DjangoDash("protocolToolChain")

app.layout = html.Div(
    [
        html.H4("Sankey Diagram monitoring Questionair"),
        dcc.Dropdown(
            id="combi-dropdown",
            options=[
                {"label": "Each project has same weight", "value": True},
                {"label": "Each combination gas same weight", "value": False},
            ],
            value=False,
        ),
        dcc.Graph(id="sankey-graph"),
        html.P("Opacity"),
        dcc.Slider(id="slider", min=0, max=1, value=0.2, step=0.1),
        html.P("Maximum Label Length"),
        dcc.Slider(id="maxlength-slider", min=5, max=30, value=15, step=1),
        html.P("Color of 'None' Nodes"),
        dcc.Slider(
            id="color-of-none-slider", min=0, max=255, value=255, step=10
        ),
        html.Button("Update Diagram", id="update-button", n_clicks=0),
    ]
)


@app.callback(
    Output("sankey-graph", "figure"),
    [Input("update-button", "n_clicks")],
    [
        State("slider", "value"),
        State("combi-dropdown", "value"),
        State("maxlength-slider", "value"),
        State("color-of-none-slider", "value"),
    ],
)
def process_and_visualize_excel(
    n_clicks, opacity, combi, maxlength, color_of_none
):

    df, df_anzahl = read_and_process_excel(file_path)

    df_relation = data_relation_process(df)

    df_relation = combiTimes(df_relation)

    # generate sankey diagram
    fig = create_sankey(
        df_relation,
        df_anzahl,
        opacity,
        maxlength,
        color_of_none,
        combiTimes=combi,
    )
    # create_sankey(df_relation, folder_path, df_anzahl, opacity)
    # create_sankey(df_relation, folder_path, df_anzahl, opacity, combiTimes=True)
    return fig
