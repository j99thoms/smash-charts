import dash
import dash_bootstrap_components as dbc
import dash_vega_components as dvc
from dash import dcc, html, Input, Output, callback
from utils import (
    get_dropdown_options, 
    get_screen_width
)
from plots import (
    get_scatter_plot, 
    get_corr_matrix_plot
)

# Prepare options for dropdown lists
dropdown_options = get_dropdown_options()

dash.register_page(__name__)

layout = html.Div(
    className="page-container",
    children=[
        dbc.Row([
            # Attribute selection (2x dropdown lists)
            html.Div(
                [
                    html.Div(
                        [
                            html.H4(
                                "Choose two attributes:",
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
                                id="scatter-dropdown-1",
                                options=dropdown_options,
                                value="Max Air Speed",
                            ),
                            html.Div(style={"height": "8px"}),  # Spacer
                            dcc.Dropdown(
                                id="scatter-dropdown-2",
                                options=dropdown_options,
                                value="Max Run Speed",
                            )
                        ], 
                        style={
                            "width": "270px", 
                            "color": "black",  
                            "float": "left"
                        }
                    )
                ], 
                style={"width": "95%",  "float": "right"}
            ),
        ]),
        dbc.Row([
            # Spacer
            dbc.Col([
                html.Div(style={"height": "10px"}),
            ])
        ]),
        dbc.Row([
            # Plot
            dbc.Col([
                    # Scatter plot
                    # html.Div([
                        html.H3(
                            id='scatter-title', 
                            style={
                                "height": "6%", 
                                "width": "95%", 
                                "float": "left", 
                                "margin-top": "10px"
                            }
                        ),
                    # ], 
                    # style={"width": "98%", "float": "right"}),
                    dvc.Vega(
                        id="scatter-plot",
                        className="scatter-plot-frame",
                        opt={"renderer": "svg", "actions": False}
                    ), #TODO: Dynamic height
            ]), 
            dbc.Col([
                    # Correlation matrix plot
                    # html.Div([
                        html.H3(
                            "Correlations", 
                            style={
                                "height": "6%", 
                                "width": "90%", 
                                "float": "left", 
                                "text-align": "center"
                            }
                        ),
                    # ], 
                    # style={"width": "98%", "float": "right"}),
                    dvc.Vega(
                        id="corr-matrix-plot",
                        className="corr-matrix-plot-frame",
                        opt={"renderer": "svg", "actions": False}
                    ), #TODO: Dynamic height
            ]),           
        ]),
    ]
)


# Update the scatter plot
@callback(
    Output("scatter-plot", "spec"),
    Output('scatter-title', 'children'),
    Input("scatter-dropdown-1", "value"),
    Input("scatter-dropdown-2", "value"),
    Input("display-size", "children"),
)
def update_scatter_plot(
    scatter_var_1, scatter_var_2, display_size_str
):
    print("--scatter--")
    screen_width = get_screen_width(display_size_str)
    if screen_width > 1200:
        plot_width = int(screen_width / 2.8)
    elif screen_width > 900:
        plot_width = int(screen_width / 3.2)
    elif screen_width > 650:
        plot_width = int(screen_width / 3.6)
    elif screen_width > 450:
        plot_width = int(screen_width / 4.0)
    else:
        plot_width = int(screen_width / 4.5)
    print(f"scatter_plot_width: {plot_width}")

    plot_height = plot_width

    MAX_IMAGE_SIZE = 40
    MIN_IMAGE_SIZE = 15
    image_size = min(int(plot_width / 14), MAX_IMAGE_SIZE)
    image_size = max(image_size, MIN_IMAGE_SIZE)
    print(f"scatter_image_size: {image_size}")

    MAX_AXIS_TITLE_SIZE = 20
    MIN_AXIS_TITLE_SIZE = 12
    axis_title_size = min(int(plot_width / 19), MAX_AXIS_TITLE_SIZE)
    axis_title_size = max(axis_title_size, MIN_AXIS_TITLE_SIZE)
    print(f"scatter_axis_title_size: {axis_title_size}")

    MAX_AXIS_LABEL_SIZE = 16
    MIN_AXIS_LABEL_SIZE = 10
    axis_label_size = min(int(plot_width / 24), MAX_AXIS_LABEL_SIZE)
    axis_label_size = max(axis_label_size, MIN_AXIS_LABEL_SIZE)
    print(f"scatter_axis_label_size: {axis_label_size}")

    plot, title = get_scatter_plot(
         var_1=scatter_var_1,
         var_2=scatter_var_2,
         plot_height=plot_height,
         plot_width=plot_width,
         image_size=image_size,
         axis_title_size=axis_title_size,
         axis_label_size=axis_label_size
    )
    
    return plot.to_dict(), title

# Update the correlation matrix plot
@callback(
    Output("corr-matrix-plot", "spec"),
    Input("scatter-dropdown-1", "value"),
    Input("scatter-dropdown-2", "value"),
    Input("display-size", "children"),
)
def update_corr_matrix_plot(
    scatter_var_1, scatter_var_2, display_size_str
):
    screen_width = get_screen_width(display_size_str)

    print("--corr_plot--")
    if screen_width > 1200:
        plot_width = int(screen_width / 3.2)
    elif screen_width > 900:
        plot_width = int(screen_width / 3.6)
    elif screen_width > 650:
        plot_width = int(screen_width / 4.0)
    elif screen_width > 450:
        plot_width = int(screen_width / 4.4)
    else:
        plot_width = int(screen_width / 4.5)
    print(f"corr_plot_width: {plot_width}")

    plot_height = plot_width

    MAX_AXIS_LABEL_SIZE = 16
    MIN_AXIS_LABEL_SIZE = 10
    axis_label_size = min(int(plot_width / 26), MAX_AXIS_LABEL_SIZE)
    axis_label_size = max(axis_label_size, MIN_AXIS_LABEL_SIZE)
    print(f"corr_axis_label_size: {axis_label_size}")

    circle_radius = plot_width / 20
    circle_size = int(3.14159 * (circle_radius ** 2))
    print(f"corr_circle_size: {circle_size}")


    plot = get_corr_matrix_plot(
        var_1=scatter_var_1, 
        var_2=scatter_var_2,
        plot_height=plot_height,
        plot_width=plot_width,
        axis_label_size=axis_label_size,
        circle_size=circle_size
    )
    
    return plot.to_dict()
