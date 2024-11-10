import dash
import dash_bootstrap_components as dbc
import dash_vega_components as dvc
from dash import html, Input, Output, State, callback
from utils import (
    get_attribute_selector_dropdown,
    get_vertical_spacer,
    get_screen_width,
    parse_excluded_character_ids
)
from plots import (
    get_bar_chart,
    get_bar_chart_title,
    DEFAULT_BAR_CHART_ATTRIBUTE
)

dash.register_page(__name__)

layout = html.Div(
    className="inner-page-container",
    children=[
        dbc.Row([
            # Attribute selection (1x dropdown list)
            html.Div(
                children=[
                    html.Div(
                        children=html.H4("Choose an attribute:"),
                        style={
                            "width": "270px",
                            "padding-left": "5px"
                        }
                    ),
                    html.Div(
                        children=[
                            get_attribute_selector_dropdown(
                                div_id="bar-dropdown",
                                default_value=DEFAULT_BAR_CHART_ATTRIBUTE,
                                data_type="quantitative"
                            )
                        ],
                        style={"width": "270px"}
                    ),
                    # Invisible divs used to track last selected var:
                    html.Div(
                        id='last-selected-bar-var',
                        children=DEFAULT_BAR_CHART_ATTRIBUTE,
                        style={'display': 'None'}
                    )
                ],
                style={
                    "width": "95%",
                    "float": "right"
                }
            )
        ]),
        dbc.Row([
            # Spacer
            get_vertical_spacer(height=20)
        ]),
        dbc.Row([
            # Bar chart
            html.H3(
                id='bar-title',
                style={
                    "height": "6%", 
                    "width": "100%", 
                    "text-align": "center"
                }
            ),
            dvc.Vega(
                id="bar-chart",
                className="bar-chart-frame",
                opt={"renderer": "svg", "actions": False}
            )
        ])
    ]
)


# Track which variable was selected last
@callback(
    Output('last-selected-bar-var', 'children'),
    Input("bar-dropdown", "value"),
    State('last-selected-bar-var', 'children')
)
def update_last_selected_bar_var(
    selected_attribute, last_selected_attribute
):
    if selected_attribute is not None:
       last_selected_attribute = selected_attribute

    return last_selected_attribute

# Update the bar chart
@callback(
    Output("bar-chart", "spec"),
    Output('bar-title', 'children'),
    Input("bar-dropdown", "value"),
    Input("display-size", "children"),
    Input("excluded-characters", "children"),
    State('last-selected-bar-var', 'children')
)
def update_bar_chart(
    selected_attribute, display_size_str, excluded_ids_string,
    last_selected_attribute
):
    screen_width = get_screen_width(display_size_str)
    excluded_character_ids = parse_excluded_character_ids(excluded_ids_string)

    if selected_attribute is None:
        selected_attribute = last_selected_attribute

    plot = get_bar_chart(
        var=selected_attribute,
        screen_width=screen_width,
        excluded_character_ids=excluded_character_ids,
        verbose=True
    )

    title = get_bar_chart_title(selected_attribute)

    return plot.to_dict(), title
