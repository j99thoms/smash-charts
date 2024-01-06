import dash
import dash_bootstrap_components as dbc
import dash_vega_components as dvc
from dash import dcc, html, Input, Output, callback
from utils import (
    get_dropdown_options, 
    get_screen_width
)
from plots import (
    get_hori_bar_chart, 
    get_vert_bar_chart, 
    get_bar_chart_title
)

# Prepare options for dropdown lists
dropdown_options = get_dropdown_options()

dash.register_page(__name__)

layout = html.Div(
    className="page-container",
    children=[
        dbc.Row([
            # Attribute selection (1x dropdown list)
            html.Div(
                [
                    html.Div(
                        [
                            html.H4(
                                "Choose an attribute:",
                                style={
                                    "width": "240px", 
                                    "color": "black",  
                                    "float": "right",
                                    "text-align": "left"
                                }
                            ),
                        ],
                        style={
                            "width": "270px",   
                            "float": "left"
                        }
                    )
                ], 
                style={"width": "95%", "float": "right"}
            ), 
            html.Div(
                [
                    html.Div(
                        [
                            dcc.Dropdown(
                                id="bar-dropdown",
                                options=dropdown_options,
                                value="Weight",
                            )
                        ], 
                        style={
                            "width": "270px", 
                            "color": "black",  
                            "float": "left"
                        }
                    )
                ], 
                style={"width": "95%", "float": "right"}
            ), 
        ]),
        dbc.Row([
            # Spacer
            html.Div(style={"height": "10px"})
        ]),
        dbc.Row([
            # Bar chart
            html.Div(
                [
                    html.H3(id='bar-title'),
                ], 
                style={
                    "height": "6%", 
                    "width": "100%", 
                    "text-align": "center", 
                    "margin-top": "10px"
                }
            ),
            dvc.Vega(
                id="bar-chart",
                className="bar-chart-frame",
                opt={"renderer": "svg", "actions": False}
            ),
        ]),
    ]
)


# Update the bar chart
@callback(
    Output("bar-chart", "spec"),
    Output('bar-title', 'children'),
    Input("bar-dropdown", "value"),
    Input("display-size", "children"),
)
def update_bar_chart(
    bar_var, display_size_str
):
    screen_width = get_screen_width(display_size_str)

    if screen_width > 900:  # Horizontal bar chart
        plot = get_hori_bar_chart(var=bar_var, screen_width=screen_width, verbose=True)
    else:   # Vertical bar chart
        plot = get_vert_bar_chart(var=bar_var, screen_width=screen_width, verbose=True)

    title = get_bar_chart_title(bar_var)

    return plot.to_dict(), title
