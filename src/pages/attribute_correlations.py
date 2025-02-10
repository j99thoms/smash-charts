from datetime import datetime, timedelta

import dash
import dash_bootstrap_components as dbc
import dash_vega_components as dvc
from dash import Input, Output, State, callback, ctx, dcc, html
from dash.exceptions import PreventUpdate

from plots import (
    DEFAULT_SCATTER_PLOT_ATTRIBUTE_1,
    DEFAULT_SCATTER_PLOT_ATTRIBUTE_2,
    get_corr_matrix_plot,
    get_scatter_plot,
    get_scatter_plot_title,
)
from utils import (
    get_attribute_selector_dropdown,
    get_excluded_char_ids,
    get_fighter_attributes_df,
    get_screen_width,
    get_vertical_spacer,
    get_window_title,
)

dash.register_page(__name__, title=get_window_title(__name__))

layout = html.Div(
    className='inner-page-container',
    children=[
        dbc.Row([
            # Attribute selection (2x dropdown lists)
            html.Div(
                children=[
                    html.Div(
                        children=html.H4('Choose two attributes:'),
                        style={
                            'width': '270px',
                            'padding-left': '5px',
                        },
                    ),
                    html.Div(
                        id='scatter-dropdown-container',
                        children=[
                            get_attribute_selector_dropdown(
                                div_id='scatter-dropdown-1',
                                default_value=DEFAULT_SCATTER_PLOT_ATTRIBUTE_1,
                                data_type='continuous',
                            ),
                            get_vertical_spacer(height=8),
                            get_attribute_selector_dropdown(
                                div_id='scatter-dropdown-2',
                                default_value=DEFAULT_SCATTER_PLOT_ATTRIBUTE_2,
                                data_type='continuous',
                            ),
                        ],
                        style={'width': '270px'},
                    ),
                    # Invisible divs used to track last selected vars:
                    html.Div(
                        id='last-selected-scatter-var-1',
                        children=DEFAULT_SCATTER_PLOT_ATTRIBUTE_1,
                        style={'display': 'None'},
                    ),
                    html.Div(
                        id='last-selected-scatter-var-2',
                        children=DEFAULT_SCATTER_PLOT_ATTRIBUTE_2,
                        style={'display': 'None'},
                    ),
                ],
                style={
                    'width': '95%',
                    'float': 'right',
                },
            ),
        ]),
        dbc.Row([
            # Spacer
            get_vertical_spacer(height=20),
        ]),
        dbc.Row([
            # Plots
            dbc.Col([
                # Scatter plot
                html.H3(
                    id='scatter-title',
                    style={
                        'height': '6%',
                        'width': '95%',
                    },
                ),
                html.Div([
                    dvc.Vega(
                        id='scatter-plot',
                        className='scatter-plot-frame', #TODO: Dynamic height
                        opt={'renderer': 'svg', 'actions': False},
                    )],
                    style={'position': 'relative', 'float': 'left', 'width': '90%'},
                ),
                html.Div([
                    dcc.Slider(
                        id='scatter-image-size-slider',
                        value=1, min=0, max=2,
                        marks=None,
                        vertical=True,
                        updatemode='drag',
                        tooltip={'placement': 'right', 'transform': 'imageSizeMultiplier'},
                    )],
                    style={'position': 'relative', 'float': 'left', 'width': '5%'},
                ),
            ]),
            dbc.Col([
                # Correlation matrix plot
                html.H3(
                    'Correlations',
                    style={
                        'height': '6%',
                        'width': '90%',
                        'text-align': 'center',
                    },
                ),
                dvc.Vega(
                    id='corr-matrix-plot',
                    className='corr-matrix-plot-frame', #TODO: Dynamic height
                    opt={'renderer': 'svg', 'actions': False},
                    style={'margin-bottom': '30px'},
                ),
            ]),
        ]),
        dcc.Store(id='scatter-prev-excluded-char-ids-mem', storage_type='session'),
    ],
)


# Update dropdown list when game is changed
@callback(
    Output('scatter-dropdown-container', 'children'),
    Input('game-selector-buttons', 'value'),
    State('last-selected-scatter-var-1', 'children'),
    State('last-selected-scatter-var-2', 'children'),
)
def update_scatter_dropdowns(
    selected_game, last_selected_var_1, last_selected_var_2,
):
    valid_attributes = get_fighter_attributes_df(game=selected_game).columns

    if last_selected_var_1 in valid_attributes:
        default_value_1 = last_selected_var_1
    else:
        default_value_1 = DEFAULT_SCATTER_PLOT_ATTRIBUTE_1

    if last_selected_var_2 in valid_attributes:
        default_value_2 = last_selected_var_2
    else:
        default_value_2 = DEFAULT_SCATTER_PLOT_ATTRIBUTE_2

    dropdowns = [
        get_attribute_selector_dropdown(
            div_id='scatter-dropdown-1',
            default_value=default_value_1,
            data_type='continuous',
            game=selected_game,
        ),
        get_vertical_spacer(height=8),
        get_attribute_selector_dropdown(
            div_id='scatter-dropdown-2',
            default_value=default_value_2,
            data_type='continuous',
            game=selected_game,
        ),
    ]

    return dropdowns

# Track which variables were selected last
@callback(
    Output('last-selected-scatter-var-1', 'children'),
    Output('last-selected-scatter-var-2', 'children'),
    Input('scatter-dropdown-1', 'value'),
    Input('scatter-dropdown-2', 'value'),
    State('last-selected-scatter-var-1', 'children'),
    State('last-selected-scatter-var-2', 'children'),
)
def update_last_selected_scatter_vars(
    scatter_var_1, scatter_var_2, last_selected_var_1, last_selected_var_2,
):
    if scatter_var_1 is not None:
        last_selected_var_1 = scatter_var_1
    if scatter_var_2 is not None:
        last_selected_var_2 = scatter_var_2

    return last_selected_var_1, last_selected_var_2

# Update the scatter plot
@callback(
    Output('scatter-plot', 'spec'),
    Output('scatter-title', 'children'),
    Output('scatter-prev-excluded-char-ids-mem', 'data'),
    Input('scatter-dropdown-1', 'value'),
    Input('scatter-dropdown-2', 'value'),
    Input('display-size', 'children'),
    Input('excluded-char-ids-mem', 'data'),
    Input('game-selector-buttons', 'value'),
    Input('scatter-image-size-slider', 'value'),
    State('last-selected-scatter-var-1', 'children'),
    State('last-selected-scatter-var-2', 'children'),
    State('scatter-prev-excluded-char-ids-mem', 'data'),
    State('excluded-char-ids-mem', 'modified_timestamp'),
    State('settings-btn-last-press', 'data'),
)
def update_scatter_plot(
    scatter_var_1, scatter_var_2, display_size_str,
    excluded_char_ids_mem, selected_game, image_size_slider_val,
    last_selected_var_1, last_selected_var_2,
    prev_excluded_char_ids_mem, excluded_char_ids_last_update,
    settings_btn_last_press,
):
    screen_width = get_screen_width(display_size_str)

    excluded_char_ids = get_excluded_char_ids(excluded_char_ids_mem)
    prev_excluded_char_ids = get_excluded_char_ids(prev_excluded_char_ids_mem)

    # Prevent unnecessary updates:
    if (
        excluded_char_ids_mem is not None
          and set(excluded_char_ids) == set(prev_excluded_char_ids)
          and ctx.triggered_id == 'excluded-char-ids-mem'
    ):
        now = datetime.now()

        if settings_btn_last_press is not None:
            last_press_time = settings_btn_last_press['time']
            last_press_time = datetime.strptime(last_press_time, '%Y-%m-%d %H:%M:%S')
            delta = timedelta(seconds = 2)
            if last_press_time <= now <= (last_press_time + delta):
                raise PreventUpdate('Halting because update is unnecessary.')

        if excluded_char_ids_last_update is not None and excluded_char_ids_last_update > 0:
            last_update_unix = excluded_char_ids_last_update / 1000
            last_update_time = datetime.fromtimestamp(last_update_unix)
            delta = timedelta(seconds = 2)
            if last_update_time <= now <= (last_update_time + delta):
                raise PreventUpdate('Halting because update is unnecessary.')

    if scatter_var_1 is None:
        scatter_var_1 = last_selected_var_1
    if scatter_var_2 is None:
        scatter_var_2 = last_selected_var_2

    if isinstance(image_size_slider_val, int | float):
        # f(0) = 1/2; f(1) = 1; f(2) = 2
        val = image_size_slider_val
        image_size_multiplier = (0.25 * val ** 2) + (0.25 * val) + 0.5
    else:
        image_size_multiplier = 1

    plot = get_scatter_plot(
         var_1=scatter_var_1,
         var_2=scatter_var_2,
         screen_width=screen_width,
         excluded_fighter_ids=excluded_char_ids,
         selected_game=selected_game,
         image_size_multiplier=image_size_multiplier,
    )

    title = get_scatter_plot_title(scatter_var_1, scatter_var_2)

    return plot.to_dict(), title, excluded_char_ids_mem

# Update the correlation matrix plot
@callback(
    Output('corr-matrix-plot', 'spec'),
    Input('scatter-dropdown-1', 'value'),
    Input('scatter-dropdown-2', 'value'),
    Input('display-size', 'children'),
    State('last-selected-scatter-var-1', 'children'),
    State('last-selected-scatter-var-2', 'children'),
)
def update_corr_matrix_plot(
    scatter_var_1, scatter_var_2, display_size_str,
    last_selected_var_1, last_selected_var_2,
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
    )

    return plot.to_dict()
