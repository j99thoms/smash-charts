import pandas as pd
import altair as alt
import dash_bootstrap_components as dbc
from dash import dash, dcc, html, Input, Output, dash_table

# Load dataset
attributes_df = pd.read_csv("../data/attributes.csv")
attributes_df = attributes_df.rename(columns={'character': 'character_name'})
attributes_df = attributes_df.drop(columns=['percent_incr_fall_speed'])

# Prepare options for dropdown lists
attributes = attributes_df.columns.to_series().iloc[1:] # The first column is 'character'
attribute_labels = attributes.str.replace('_', ' ')
attribute_labels = attribute_labels.str.replace('acc', 'acceleration')
attribute_labels = attribute_labels.str.title()
dropdown_options = zip(attributes, attribute_labels)
dropdown_options = [{'value': val, 'label': label} for val, label in dropdown_options]

attribute_labels_df = pd.DataFrame(dropdown_options)

# Setup the dash app
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.DARKLY])
server = app.server

# UI
app.layout = html.Div([
    dbc.Row(
        dbc.Col([
            html.Div(style={"height": "2px"}),
            html.H1("The Super Smash Dashboard!", style={"text-align": "center"}),
            html.Div(style={"height": "10px"}),
        ])
    ),
    dbc.Row([
        dbc.Col([
                html.H4("Choose two attributes for scatter plot:"),
                html.Div([
                    html.Div([
                        html.Div([
                                dcc.Dropdown(
                                    id="scatter-dropdown-1",
                                    options=dropdown_options,
                                    value="max_air_acc",
                                )
                        ], 
                        style={"width": "100%", "color": "black"})
                    ], 
                    style={"display": "flex", "width": "75%",  "float": "left"})
                ], 
                style={"display": "flex", "width": "100%"}),
                html.Div([
                    html.Div([
                        html.Div([
                                dcc.Dropdown(
                                    id="scatter-dropdown-2",
                                    options=dropdown_options,
                                    value="fast-fall_speed",
                                )
                        ], 
                        style={"width": "100%", "color": "black"})
                    ], 
                    style={"display": "flex", "width": "75%",  "float": "left"})
                ], 
                style={"display": "flex", "width": "100%"}),
        ]),
        dbc.Col([
                html.H4("Choose one attribute for bar chart:"),
                html.Div([
                    html.Div([
                        html.Div([
                                dcc.Dropdown(
                                    id="bar-dropdown",
                                    options=dropdown_options,
                                    value="max_run_speed",
                                )
                        ], 
                        style={"width": "100%", "color": "black"})
                    ], 
                    style={"display": "flex", "width": "75%",  "float": "left"})
                ],
                style={"display": "flex", "width": "100%"}),
        ]), 
    ]),
    dbc.Row(
        dbc.Col([
            html.Div(style={"height": "10px"}),
        ])
    ),
    dbc.Row([
            dbc.Col([
                    html.H3(id='scatter-title', style={"height": "6%", "margin-top": "10px"}),
                    html.Iframe(id="scatter-plot", width="100%", height="500px"),
            ]),
            dbc.Col([
                    html.H3(id='bar-title', style={"height": "6%", "margin-top": "10px"}),
                    html.Iframe(id="bar-chart", width="100%", height="1200px"),
            ]),
        ]),
], style={"width": "97%", "height": "97%", "margin": "auto"})


# Update the scatter plot
@app.callback(
    Output("scatter-plot", "srcDoc"),
    Output('scatter-title', 'children'),
    Input("scatter-dropdown-1", "value"),
    Input("scatter-dropdown-2", "value"),
)
def update_scatter_plot(
    scatter_var_1, scatter_var_2
):
    PLOT_HEIGHT = 400
    PLOT_WIDTH = 400

    if scatter_var_1 is None or scatter_var_2 is None:
         plot = alt.Chart().mark_point().properties(height=PLOT_HEIGHT, width=PLOT_WIDTH)
         return plot.to_html(), "Scatter Plot of Chosen Attributes"
    if scatter_var_1 == scatter_var_2:
         plot = alt.Chart().mark_point().properties(height=PLOT_HEIGHT, width=PLOT_WIDTH)
         return plot.to_html(), "Scatter Plot of Chosen Attributes"
    
    scatter_atr_name_1 = attribute_labels_df.query(
         "value == @scatter_var_1"
    ).iloc[0].loc['label']
    scatter_atr_name_2 = pd.DataFrame(dropdown_options).query(
         "value == @scatter_var_2"
    ).iloc[0].loc['label']

    plot_df = attributes_df[['character_name', scatter_var_1, scatter_var_2]]
    plot_df = plot_df.dropna()

    plot = alt.Chart(plot_df).encode(
        alt.X(scatter_var_1),
        alt.Y(scatter_var_2),
        alt.Tooltip(['character_name', scatter_var_1, scatter_var_2]),
    ).mark_point().properties(height=PLOT_HEIGHT, width=PLOT_WIDTH)

    title = f"Scatter Plot of {scatter_atr_name_1} vs. {scatter_atr_name_2}"

    return plot.to_html(), title

# Update the bar chart
@app.callback(
    Output("bar-chart", "srcDoc"),
    Output('bar-title', 'children'),
    Input("bar-dropdown", "value"),
)
def update_bar_chart(
    bar_var
):
    PLOT_HEIGHT = 1100
    PLOT_WIDTH = 300

    if bar_var is None:
        plot = alt.Chart().mark_point().properties(height=PLOT_HEIGHT, width=PLOT_WIDTH)
        return plot.to_html(), "Bar Chart of Chosen Attribute"
    
    bar_atr_name = attribute_labels_df.query(
         "value == @bar_var"
    ).iloc[0].loc['label']
    
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
    ).mark_bar().properties(height=PLOT_HEIGHT, width=PLOT_WIDTH)

    title = f"Bar Chart of {bar_atr_name}s"

    return plot.to_html(), title

# Run in debug mode if the app is started via the console
if __name__ == "__main__":
    app.run_server(debug=True)