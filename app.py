import json

import pandas as pd
import plotly.express as px
from dash import Dash, Input, Output, State, dcc, html

from src import federal, local, utils

app = Dash(__name__)

colors = {"background": "#111111", "text": "#7FDBFF"}

styles = {
    "pre": {
        "border": "thin lightgrey solid",
        "overflowX": "scroll",
        "width": "48%",
        "margin-right": "2%",
    }
}


def display_choropleth():
    df = pd.read_csv("./data/county_voter_reg_stats.csv", dtype={"fips": str})

    counties = json.load(open("./data/counties.geojson"))
    fig = px.choropleth(
        df,
        geojson=counties,
        color="Party",
        locations="County",
        featureidkey="properties.name",
    )
    fig.update_geos(fitbounds="locations", visible=False)
    fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})

    fig.layout.dragmode = False

    return fig


app.layout = html.Div(
    [
        html.H4("State of California Election Data"),
        html.Div(
            [
                dcc.Graph(
                    id="graph",
                    figure=display_choropleth(),
                    config={},
                    style={"width": "98%", "margin-right": "2%"},
                ),
                dcc.Input(
                    id="address",
                    type="text",
                    placeholder="Enter your address to get your representatives",  # noqa: E501
                    style={"width": "80%"},
                ),
                html.Button(
                    "Submit",
                    id="addr-submit-val",
                    n_clicks=0,
                    style={"margin-right": "2%"},
                ),
                dcc.Input(
                    id="reprinfo",
                    type="text",
                    placeholder="Enter name of representative to get their sponsored bills ",  # noqa: E501
                    style={"width": "80%"},
                ),
                html.Button(
                    "Submit",
                    id="reprinfo-submit-val",
                    n_clicks=0,
                    style={"margin-right": "2%"},
                ),
            ],
            style={"float": "left", "width": "50%"},
        ),
        html.Div(
            [
                html.Div(
                    [
                        dcc.Markdown(
                            """
                **Data for given county**

                Click on a county to view more detailed stats.
            """
                        ),
                        html.Pre(id="hover-data", style=styles["pre"]),
                    ],
                    className="three columns",
                ),
                html.Div(
                    [
                        dcc.Markdown(
                            """
                **Data for given address**

                Enter your address to get your representatives
                    """
                        ),
                        dcc.Loading(
                            id="address-loading",
                            children=[
                                html.Pre(
                                    id="address-data", style=styles["pre"]
                                )
                            ],
                            type="circle",
                        ),
                    ],
                ),
                html.Div(
                    [
                        dcc.Markdown(
                            """
                **Data for representative**

                Enter name of representative to get their sponsored bills. (This takes a bit, since some representatives might have sponsored a lot of bills.)"""  # noqa: E501
                        ),
                        dcc.Loading(
                            id="reprinfo-loading",
                            children=[
                                html.Pre(
                                    id="reprinfo-data", style=styles["pre"]
                                )
                            ],
                            type="circle",
                        ),
                    ],
                ),
            ]
        ),
    ]
)


@app.callback(
    Output("reprinfo-data", "children"),
    Input("reprinfo-submit-val", "n_clicks"),
    State("reprinfo", "value"),
)
def display_reprinfo(n_clicks, reprinfo):
    if reprinfo is None:
        return "Enter name of representative to get their sponsored bills"

    representativeinfo = local.getbills.byrepresentative(
        local.getrepresentatives.byname(reprinfo)["id"]
    )

    return json.dumps(representativeinfo, indent=2)


@app.callback(
    Output("address-data", "children"),
    Input("addr-submit-val", "n_clicks"),
    State("address", "value"),
)
def display_representatives(n_clicks, address):
    if address is None:
        return "Enter a valid address"

    localrepresentatives = local.getrepresentatives.byaddress(address)
    senate = federal.getchamberinfo.Senate()
    senators = senate.senators()

    returnvalue = {"Local": localrepresentatives, "US Senate": senators}

    return json.dumps(returnvalue, indent=2)


@app.callback(
    Output("hover-data", "children"),
    [Input("graph", "clickData")],
)
def display_hover_data(hoverdata):
    data = {}
    header = [
        "County",
        "Eligible",
        "Total Registered",
        "Democratic",
        "Republican",
        "American Independent",
        "Green",
        "Libertarian",
        "Peace and Freedom",
        "Unknown",
        "Other",
        "No Party Preference",
        "FIPS",
        "Party",
    ]

    jsondata = json.load(open("data/county_voter_reg_stats.json"))

    for i in range(header.__len__()):
        if hoverdata is None:
            break
        if header[i] == "County":
            continue
        county = hoverdata["points"][0]["location"]
        data[header[i]] = jsondata[county][header[i]]

    returnvalue = (
        json.dumps(data, indent=2)
        if data != {}
        else "Click on a county to see data"
    )

    return returnvalue


app.run_server(debug=True)
