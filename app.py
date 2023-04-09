import json

import pandas as pd
import plotly.express as px
from dash import Dash, Input, Output, dcc, html

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
        dcc.Graph(
            id="graph",
            figure=display_choropleth(),
            config={},
            style={"width": "48%", "float": "left", "margin-right": "2%"},
        ),
        html.Div(
            [
                dcc.Markdown(
                    """
                **Hover Data**

                Mouse over values in the graph.
            """
                ),
                html.Pre(id="hover-data", style=styles["pre"]),
            ],
            className="three columns",
        ),
    ]
)


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
