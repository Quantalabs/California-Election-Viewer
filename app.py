import plotly.express as px
import pandas as pd
import json
from dash import Dash, dcc, html, Input, Output

app = Dash(__name__)

colors = {
    'background': '#111111',
    'text': '#7FDBFF'
}

styles = {
    'pre': {
        'border': 'thin lightgrey solid',
        'overflowX': 'scroll'
    }
}

app.layout = html.Div([
    html.H4('State of California Election Data'),
    html.P("Color by:"),
    dcc.RadioItems(
        id='colorby',
        options=["Eligible", "Total Registered", "Party"],
        value="Eligible",
        inline=True
    ),
    dcc.Graph(id="graph"),
    html.Div([
            dcc.Markdown("""
                **Hover Data**

                Mouse over values in the graph.
            """),
            html.Pre(id='hover-data', style=styles['pre'])
        ], className='three columns'),
])

@app.callback(
    Output('hover-data', 'children'),
    Input('graph', 'hoverData'))
def display_hover_data(hoverData):
    data = {}
    header = ["County","Eligible","Total Registered","Democratic","Republican","American Independent","Green","Libertarian","Peace and Freedom","Unknown","Other","No Party Preference","FIPS","Party"]

    jsondata = json.load(open("data/county_voter_reg_stats.json"))

    for i in range(header.__len__()):
        if header[i] == "County":
            continue
        data[header[i]] = jsondata[hoverData['points'][0]['location']][header[i]]
    
    return json.dumps(data, indent=2)

@app.callback(
    Output("graph", "figure"),
    Input("colorby", "value"))
def display_choropleth(colorby):
    df = pd.read_csv("./data/county_voter_reg_stats.csv",
                     dtype={"fips": str})

    counties = json.load(open("./data/counties.geojson"))

    if colorby != "Party":
        fig = px.choropleth(df, geojson=counties, color=colorby,
                            locations="County", featureidkey="properties.name",
                            color_continuous_scale="sunset")
    else:
        fig = px.choropleth(df, geojson=counties, color=colorby,
                            locations="County", featureidkey="properties.name")

    fig.update_geos(fitbounds="locations", visible=False)
    fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})

    return fig


app.run_server(debug=True)
