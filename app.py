import pandas as pd
from dash import Dash, dcc, html, Input, Output
import plotly.express as px

df = pd.read_csv("Space_Corrected.csv")
df = df.loc[:, ~df.columns.str.contains("^Unnamed")]
df["Datum"] = pd.to_datetime(df["Datum"], errors="coerce")
df["Year"] = df["Datum"].dt.year

app = Dash(__name__)
server = app.server

app.layout = html.Div([
    html.H1("Space Industry Growth Over Time"),

    html.Label("Select Time Range:"),
    dcc.Dropdown(
        id="year-filter",
        options=[
            {"label": "All Time", "value": "all"},
            {"label": "2000-Present", "value": "modern"}
        ],
        value="all",
        clearable=False
    ),

    dcc.Graph(id="line-chart"),
    dcc.Graph(id="bar-chart"),

    html.H2("Key Findings"),
    html.Ul([
        html.Li("Space missions were highest during the Cold War."),
        html.Li("Activity declined and then increased again recently."),
        html.Li("Modern growth is driven by multiple companies, not just governments."),
    ])
])

@app.callback(
    Output("line-chart", "figure"),
    Output("bar-chart", "figure"),
    Input("year-filter", "value")
)
def update_graphs(selected):
    if selected == "modern":
        data = df[df["Year"] >=2000]
        title1 = "Space Industry Growth Since 2000"
        title2 = "Top Companies (2000-Present)"
    else:
        data = df
        title1 = "Space Industry Growth Over Time"
        title2 = "Top Companies (All Time)"
    
    missions = data.groupby("Year").size().reset_index()
    missions.columns = ["Year", "Missions"]
    fig1 = px.line(missions, x="Year", y="Missions", title=title1)

    companies = data["Company Name"].value_counts().head(10).reset_index()
    companies.columns = ["Company Name", "Missions"]
    fig2 = px.bar(companies, x="Company Name", y="Missions", title=title2)

    return fig1, fig2

if __name__ == "__main__":
    app.run(debug=True, port=8051)
    