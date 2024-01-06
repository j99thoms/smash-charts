import dash_bootstrap_components as dbc
from dash import dash, dcc, html, Input, Output
from utils import (
    get_dropdown_options
)
from plots import (
    get_hori_bar_chart, 
    get_bar_chart_title,
    get_scatter_plot
)

dropdown_options = get_dropdown_options()

# Setup the dash app
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.JOURNAL])
server = app.server


# UI
app.layout = html.Div([
    dbc.Row(
        # App Title
        dbc.Col([
            html.Div(style={"height": "2px"}),
            html.H1("The Super Smash Dashboard!", style={"text-align": "center"}),
            html.Div(style={"height": "10px"}),
        ])
    ),
    dbc.Row([
        # Scatter plot variable selection (dropdown lists)
        dbc.Col([
                html.Div([
                    html.Div([
                        html.H4("Choose two attributes for scatter plot:", style={"width": "98%", "float": "right", "text-align": "left"}),
                        dcc.Dropdown(
                            id="scatter-dropdown-1",
                            options=dropdown_options,
                            value="Max Air Speed",
                        )
                    ], 
                    style={"width": "63.1%", "color": "black", "float": "left"})
                ], 
                style={"width": "95%",  "float": "right"}),
                html.Div(style={"height": "8px"}),  # Spacer
                html.Div([
                    html.Div([
                        dcc.Dropdown(
                            id="scatter-dropdown-2",
                            options=dropdown_options,
                            value="Max Run Speed",
                        )
                    ], 
                    style={"width": "63.1%", "color": "black", "float": "left"})
                ], 
                style={"width": "95%",  "float": "right"}),
        ]),
        # Bar chart variable selection (dropdown list)
        dbc.Col([
                html.Div([
                    html.Div([
                        html.H4("Choose one attribute for bar chart:", style={"width": "98%", "float": "right", "text-align": "left"}),
                        dcc.Dropdown(
                            id="bar-dropdown",
                            options=dropdown_options,
                            value="Weight",
                        )
                    ], 
                    style={"width": "85%", "color": "black",  "float": "left"})
                ], 
                style={"width": "70.5%", "float": "right"})
        ]), 
    ]),
    dbc.Row(
        # Spacer
        dbc.Col([
            html.Div(style={"height": "10px"}),
        ])
    ),
    dbc.Row([
            # Scatter plot and attribute info
            dbc.Col([
                    # Scatter plot
                    html.Div([
                        html.H3(id='scatter-title', style={"height": "6%", "width": "95%", "float": "left", "margin-top": "10px"}),
                    ], 
                    style={"width": "98%", "float": "right"}),
                    html.Iframe(id="scatter-plot", width="100%", height="500px"),

                    # Attribute info
                    html.Div([
                        html.Div([
                            html.Div([
                                html.H3(children=[html.U("Attribute Info")], style={"text-align": "center"}),
                                html.P(children=[
                                    html.B("Weight "), 
                                    "is a measurement of how much a character can resist knockback, and ",
                                    "is one of several factors used in calculating the amount of knockback a character receives. ",
                                    "Holding all other factors constant, characters with a higher weight (heavy) tend to suffer less knockback, and ",
                                    "characters with a lower weight (light) tend to suffer more knockback."
                                ], style={"text-indent": "20px"}),
                                html.P(children=[
                                    "A character's movement ",
                                    html.B("speed "), 
                                    "is measured in distance units per frame. A ",
                                    html.B("distance unit "),
                                    "(often shortened to ",
                                    html.B("unit"),
                                    "), refers to an arbitrary unit of measurement that determines the in-game position and size of objects. ",
                                    "A unit is roughly equivalent to one decimeter, i.e. 1 unit = 0.1 meters."
                                ], style={"text-indent": "20px"}),
                                html.P(children=[
                                    html.B("Falling speed "),
                                    "is the rate at which a character can move downward in mid-air. ",
                                    "All characters can also ",
                                    html.B("fast-fall "),
                                    "at any time during a descent (by tilting down on the control stick) to increase their falling speed. ",
                                    "The vast majority of characters receive a 60% increase in downwards movement speed while fast-falling, ",
                                    "although there are a few exceptions (e.g. Ken and Ryu)."
                                ], style={"text-indent": "20px"}),
                                html.P(children=[
                                    "While walking, a character's speed is controlled by their ",
                                    html.B("max walk speed"),
                                    ", and while running, a character's speed is controlled by their ",
                                    html.B("max run speed"),
                                    ". The ",
                                    html.B("initial dash "), 
                                    "is the first part of a character's dash, during which a character gains a quick burst of speed before transitioning into their run. ",
                                    "Many characters have a higher ",
                                    html.B("initial dash speed "),
                                    "than their max run speed, although some do not. ",
                                ], style={"text-indent": "20px"}),
                                html.P(children=[
                                    "While airborne, a character's horizontal (left/right) speed is controlled by their ",
                                    html.B("max air speed"),
                                    ", and the rate at which a character can change their horizontal velocity is controlled by their ",
                                    html.B("air acceleration"),
                                    ", which is measured in units/frame^2. ",
                                    "A character's air acceleration is controlled by two values: a base value (",
                                    html.B("base air acceleration"),
                                    ") that determines their minimum acceleration, and an additional value (",
                                    html.B("delta air acceleration"),
                                    ") that is scaled based on how much the player's control stick is tilted. A character's ",
                                    html.B("max air acceleration "),
                                    "is the sum of these two values. ",
                                    "It is most beneficial for a character to have a low base value with a high additional value, ",
                                    "as this combination offers the most precise aerial control."
                                ], style={"text-indent": "20px"}),
                                html.Div([
                                    "These attribute descriptions are based on the descriptions which can be found on ",
                                    html.A("SmashWiki", href="https://www.ssbwiki.com/", target="_blank"),
                                    "."
                                ], style={"margin-top": "30px", "font-size": "85%"})
                            ],
                            style={"width": "98%", "float": "right", }),
                        ],
                        style={"width": "98%", "float": "left", "margin-top": "10px", }),
                    ],
                    style={
                        "width": "95%", "float": "left", "margin-top": "20px", 
                        "background-color": "#5A8EC7", "border-radius": "10px", "border": "3px solid black"
                    }),
            ]),

            # Bar chart
            dbc.Col([
                    html.Div([
                        html.H3(id='bar-title', style={"height": "6%", "width": "82.5%", "float": "right", "margin-top": "10px"}),
                    ], 
                    style={"width": "98%", "float": "right"}),
                    html.Iframe(id="bar-chart", width="100%", height="1450px", style={"width": "90%", "float": "right"}),
            ]),
        ]),
        dbc.Row([
             # Credits
            html.Div([
                html.Div([
                    html.A(
                        "The Super Smash Dashboard", 
                        href="https://github.com/J99thoms/Super-Smash-Dashboard",
                        target="_blank"
                    ), 
                    " was created by ",
                    html.A(
                        "Jakob Thoms", 
                        href="https://github.com/J99thoms", 
                        target="_blank"
                    ),
                    "."
                ], style={"float": "right", "width": "30%"," font-size": "90%"}),
            ], style={"width": "100%", "margin-top": "20px",}),
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

    plot, title = get_scatter_plot(
         var_1=scatter_var_1,
         var_2=scatter_var_2,
         plot_height=PLOT_HEIGHT,
         plot_width=PLOT_WIDTH
    )

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
    PLOT_HEIGHT = 300
    PLOT_WIDTH = 1300

    plot = get_hori_bar_chart(
        var=bar_var, 
        plot_height=PLOT_HEIGHT,
        plot_width=PLOT_WIDTH
    )

    title = get_bar_chart_title(bar_var)

    return plot.to_html(), title

# Run in debug mode if the app is started via the console
if __name__ == "__main__":
    app.run_server(debug=True)