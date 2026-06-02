# P2: Python Project
## Leslie Alhakim

### Load libraries and dataset
import pandas as pd
import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.express as px

df = pd.read_csv('~/Downloads/Data Viz/P2/NEW.csv')
app = dash.Dash(__name__)

### Build a dashboard
region_options = [{"label": region, "value": region} for region in df["region"].unique()]

app.layout = html.Div([
    html.H1("COVID-19 Interactive Dashboard", style={"textAlign": "center"}),

    ### Dropdown: Add a dropdown menu to select a specific WHO region.
    html.Label("Select WHO Region:"),
    dcc.Dropdown(
        id="region_dropdown",
        options=region_options,
        value=region_options[0]["value"], 
        clearable=False
    ),

    ### Slider: Add a slider to adjust the deaths displayed on visualizations.
    html.Br(),
    html.Label("Number of Deaths:"),
    dcc.Slider(
        id="death_slider",
        min=0,
        max=df["deaths"].max(),
        step=10000,
        value=df["deaths"].max()
    ),

    dcc.Graph(id="covid_graph")
])

### Callback 
@app.callback(
    Output("covid_graph", "figure"),
    [Input("region_dropdown", "value"),
     Input("death_slider", "value")]
)
def update_graph(selected_region, max_deaths):
    filt_df = df[(df["region"] == selected_region) & (df["deaths"] <= max_deaths)]

    fig = px.scatter(
        filt_df,
        x="confirmed",
        y="deaths",
        color="country",
        hover_name="country",
        title=f"Confirmed v Deaths: {selected_region}",
        labels={"confirmed": "Confirmed Cases", 
                "deaths": "Deaths"})

    return fig

if __name__ == "__main__":
    app.run(debug=True)
