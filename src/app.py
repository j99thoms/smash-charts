import pandas as pd
import altair as alt
import dash_bootstrap_components as dbc
from dash import dash, dcc, html, Input, Output, dash_table

# Load dataset
attributes_df = pd.read_csv("../data/attributes.csv")
attributes_df = attributes_df.rename(columns={'character': 'character_name'})
attributes_df = attributes_df.drop(columns=['percent_incr_fall_speed'])

# Prepare options for dropdown lists
attributes = attributes_df.columns.to_series().iloc[1:]
attribute_labels = attributes.str.replace('_', ' ').str.replace('acc', 'acceleration')
dropdown_options = zip(attributes, attribute_labels)
dropdown_options=[{'value': val, 'label': label} for val, label in dropdown_options]

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.SANDSTONE])
server = app.server
app.layout = html.Div(
    [
        html.Div(style={"height": "5px"}),
        html.H1("The Super Smash Dashboard!"),
        html.Div(style={"height": "10px"}),
        html.Div([
            html.Div([
                html.H4("Choose attributes for scatter plot:"),
                html.Div([
                    html.Div([
                        html.Div([
                                dcc.Dropdown(
                                    id="scatter-dropdown-1",
                                    options=dropdown_options,
                                    value="max_run_speed",
                                )
                        ], 
                        style={"width": "100%"})
                    ], 
                    style={"display": "flex", "width": "50%",  "float": "left"})
                ], 
                style={"display": "flex", "width": "100%"}),
                html.Div([
                    html.Div([
                        html.Div([
                                dcc.Dropdown(
                                    id="scatter-dropdown-2",
                                    options=dropdown_options,
                                    value="max_air_speed",
                                )
                        ], 
                        style={"width": "100%"})
                    ], 
                    style={"display": "flex", "width": "50%",  "float": "left"})
                ], 
                style={"display": "flex", "width": "100%"}),
            ], 
            style={"width": "50%",  "float": "left"}),        
            html.Div([
                html.H4("Choose attribute for bar chart:"),
                html.Div([
                    html.Div([
                        html.Div([
                                dcc.Dropdown(
                                    id="bar-dropdown",
                                    options=dropdown_options,
                                    value="weight",
                                )
                        ], 
                        style={"width": "100%"})
                    ], 
                    style={"display": "flex", "width": "50%",  "float": "left"})
                ],
                style={"display": "flex", "width": "100%"}),
            ], 
            style={"width": "50%",  "float": "right"}),
        ],
        style={"width": "95%", "margin": "auto", "height": "150px"}),
        html.Div(
            children=[
                html.Div(
                    children=[
                        html.H4("Scatter plot"),
                        html.Iframe(id="scatter-plot", width="100%", height="500px"),
                    ],
                    style={"width": "50%", "float": "left"},
                ),
                html.Div(
                    children=[
                        html.H4("Bar Chart"),
                        html.Iframe(id="bar-chart", width="100%", height="1200px"),
                    ],
                    style={"width": "50%", "float": "right"},
                ),
            ],
            style={"width": "95%", "margin": "auto"},
        ),
    ]
)


@app.callback(
    Output("scatter-plot", "srcDoc"),
    Input("scatter-dropdown-1", "value"),
    Input("scatter-dropdown-2", "value"),
)
def update_scatter_plot(
    scatter_var_1, scatter_var_2
):
    if scatter_var_1 is None or scatter_var_2 is None:
         return alt.Chart().mark_point().to_html()
    if scatter_var_1 == scatter_var_2:
         return alt.Chart().mark_point().to_html()
    
    plot_df = attributes_df[['character_name', scatter_var_1, scatter_var_2]]
    plot_df = plot_df.dropna()

    plot = alt.Chart(plot_df).encode(
        alt.X(scatter_var_1),
        alt.Y(scatter_var_2),
        alt.Tooltip(['character_name', scatter_var_1, scatter_var_2]),
    ).mark_point().properties(height=400, width=400)

    return plot.to_html()

@app.callback(
    Output("bar-chart", "srcDoc"),
    Input("bar-dropdown", "value"),
)
def update_bar_chart(
    bar_var
):
    if bar_var is None:
         return alt.Chart().mark_bar().to_html()
    
    plot_df = attributes_df[['character_name', bar_var]]
    plot_df = plot_df.dropna()

    plot = alt.Chart(plot_df).encode(
        alt.X(bar_var),
        alt.Y('character_name', sort='x'),
        alt.Tooltip(['character_name', bar_var]),
        # alt.Color(
        # bar_var,
        # bin=alt.Bin(maxbins=4), 
        # scale=alt.Scale(scheme='dark2'),
        # title=bar_var
        # ),
    ).mark_bar().properties(height=1100, width=300)

    return plot.to_html()


if __name__ == "__main__":
    app.run_server(debug=True)