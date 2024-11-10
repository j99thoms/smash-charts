import dash
import dash_bootstrap_components as dbc
import dash_vega_components as dvc
from dash import html, Input, Output, State, callback
from utils import (
    get_attribute_selector_dropdown,
    get_vertical_spacer,
    get_screen_width
)
from plots import (
    get_scatter_plot,
    get_scatter_plot_title,
    get_corr_matrix_plot,
    DEFAULT_SCATTER_PLOT_ATTRIBUTE_1,
    DEFAULT_SCATTER_PLOT_ATTRIBUTE_2
)

dash.register_page(__name__)

layout = html.Div(
    className="inner-page-container",
    children=[
        dbc.Row([
            # Attribute selection (2x dropdown lists)
            html.Div(
                children=[
                    html.Div(
                        children=html.H4("Choose two attributes:"),
                        style={
                            "width": "270px",  
                            "padding-left": "5px"
                        }
                    ),
                    html.Div(
                        children=[
                            get_attribute_selector_dropdown(
                                div_id="scatter-dropdown-1",
                                default_value=DEFAULT_SCATTER_PLOT_ATTRIBUTE_1,
                                data_type="continuous"
                            ),
                            get_vertical_spacer(height=8),
                            get_attribute_selector_dropdown(
                                div_id="scatter-dropdown-2",
                                default_value=DEFAULT_SCATTER_PLOT_ATTRIBUTE_2,
                                data_type="continuous"
                            )
                        ],
                        style={"width": "270px"}
                    ),
                    # Invisible divs used to track last selected vars:
                    html.Div(
                        id='last-selected-scatter-var-1',
                        children=DEFAULT_SCATTER_PLOT_ATTRIBUTE_1,
                        style={'display': 'None'}
                    ),
                    html.Div(
                        id='last-selected-scatter-var-2',
                        children=DEFAULT_SCATTER_PLOT_ATTRIBUTE_2,
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
            # Plots
            dbc.Col([
                # Scatter plot
                html.H3(
                    id='scatter-title',
                    style={
                        "height": "6%", 
                        "width": "95%"
                    }
                ),
                dvc.Vega(
                    id="scatter-plot",
                    className="scatter-plot-frame", #TODO: Dynamic height
                    opt={"renderer": "svg", "actions": False}
                )
            ]),
            dbc.Col([
                # Correlation matrix plot
                html.H3(
                    "Correlations",
                    style={
                        "height": "6%", 
                        "width": "90%",
                        "text-align": "center"
                    }
                ),
                dvc.Vega(
                    id="corr-matrix-plot",
                    className="corr-matrix-plot-frame", #TODO: Dynamic height
                    opt={"renderer": "svg", "actions": False}
                )
            ])
        ])
    ]
)

# Track which variables were selected last
@callback(
    Output('last-selected-scatter-var-1', 'children'),
    Output('last-selected-scatter-var-2', 'children'),
    Input("scatter-dropdown-1", "value"),
    Input("scatter-dropdown-2", "value"),
    State("last-selected-scatter-var-1", "children"),
    State("last-selected-scatter-var-2", "children")
)
def update_last_selected_scatter_vars(
    scatter_var_1, scatter_var_2, last_selected_var_1, last_selected_var_2
):
    if scatter_var_1 is not None:
        last_selected_var_1 = scatter_var_1
    if scatter_var_2 is not None:
        last_selected_var_2 = scatter_var_2

    return last_selected_var_1, last_selected_var_2

# Update the scatter plot
@callback(
    Output("scatter-plot", "spec"),
    Output('scatter-title', 'children'),
    Input("scatter-dropdown-1", "value"),
    Input("scatter-dropdown-2", "value"),
    Input("display-size", "children"),
    State("last-selected-scatter-var-1", "children"),
    State("last-selected-scatter-var-2", "children")
)
def update_scatter_plot(
    scatter_var_1, scatter_var_2, display_size_str,
    last_selected_var_1, last_selected_var_2
):
    screen_width = get_screen_width(display_size_str)

    if scatter_var_1 is None:
        scatter_var_1 = last_selected_var_1
    if scatter_var_2 is None:
        scatter_var_2 = last_selected_var_2
   
    plot = get_scatter_plot(
         var_1=scatter_var_1,
         var_2=scatter_var_2,
         screen_width=screen_width,
         verbose=True
    )

    title = get_scatter_plot_title(scatter_var_1, scatter_var_2)

    return plot.to_dict(), title

# Update the correlation matrix plot
@callback(
    Output("corr-matrix-plot", "spec"),
    Input("scatter-dropdown-1", "value"),
    Input("scatter-dropdown-2", "value"),
    Input("display-size", "children"),
    State("last-selected-scatter-var-1", "children"),
    State("last-selected-scatter-var-2", "children")
)
def update_corr_matrix_plot(
    scatter_var_1, scatter_var_2, display_size_str,
    last_selected_var_1, last_selected_var_2
):
    screen_width = get_screen_width(display_size_str)

    if scatter_var_1 is None:
        scatter_var_1 = last_selected_var_1
    if scatter_var_2 is None:
        scatter_var_2 = last_selected_var_2

    plot = get_corr_matrix_plot(
        var_1=scatter_var_1,
        var_2=scatter_var_2,
        screen_width=screen_width,
        verbose=True
    )

    return plot.to_dict()
