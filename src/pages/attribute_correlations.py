import dash
import dash_bootstrap_components as dbc
import dash_vega_components as dvc
from dash import Input, Output, State, callback, dcc, html
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
    get_excluded_fighter_ids,
    get_fighter_attributes_df,
    get_screen_width,
    get_vertical_spacer,
    get_window_title,
)

dash.register_page(__name__, title=get_window_title(__name__))

layout = html.Div(
    className='inner-page-container',
    children=[
        dbc.Row(
            [
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
                    ],
                    style={
                        'width': '95%',
                        'float': 'right',
                    },
                ),
            ],
        ),
        dbc.Row(
            [
                # Spacer
                get_vertical_spacer(height=20),
            ],
        ),
        dbc.Row(
            [
                # Plots
                dbc.Col(
                    [
                        # Scatter plot
                        html.H3(
                            id='scatter-title',
                            style={
                                'height': '6%',
                                'width': '95%',
                            },
                        ),
                        html.Div(
                            [
                                dvc.Vega(  # TODO: Dynamic height for scatter plot
                                    id='scatter-plot',
                                    className='scatter-plot-frame',
                                    opt={'renderer': 'svg', 'actions': False},
                                ),
                            ],
                            style={
                                'position': 'relative',
                                'float': 'left',
                                'width': '90%',
                            },
                        ),
                        html.Div(
                            [
                                dcc.Slider(
                                    id='scatter-image-size-slider',
                                    value=1,
                                    min=0,
                                    max=2,
                                    marks=None,
                                    vertical=True,
                                    updatemode='drag',
                                    tooltip={
                                        'placement': 'right',
                                        'transform': 'imageSizeMultiplier',
                                    },
                                ),
                            ],
                            style={
                                'position': 'relative',
                                'float': 'left',
                                'width': '5%',
                            },
                        ),
                    ],
                ),
                dbc.Col(
                    [
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
                            className='corr-matrix-plot-frame',  # TODO: Dynamic height
                            opt={'renderer': 'svg', 'actions': False},
                            style={'margin-bottom': '30px'},
                        ),
                    ],
                ),
            ],
        ),
        dcc.Store(
            id='scatter-plot-params',
            storage_type='memory',
            data={
                'var_1': DEFAULT_SCATTER_PLOT_ATTRIBUTE_1,
                'var_2': DEFAULT_SCATTER_PLOT_ATTRIBUTE_2,
                'screen_width': 900,
                'excluded_fighter_ids': [],
                'selected_game': 'ultimate',
                'image_size_multiplier': 1.0,
            },
        ),
    ],
)


# Update dropdown list when game is changed
@callback(
    Output('scatter-dropdown-container', 'children'),
    Input('game-selector-buttons', 'value'),
    State('scatter-plot-params', 'data'),
)
def update_scatter_dropdowns(selected_game, scatter_plot_params):
    valid_attributes = get_fighter_attributes_df(game=selected_game).columns
    prev_scatter_var_1 = scatter_plot_params['var_1']
    prev_scatter_var_2 = scatter_plot_params['var_2']

    if prev_scatter_var_1 in valid_attributes:
        default_value_1 = prev_scatter_var_1
    else:
        default_value_1 = DEFAULT_SCATTER_PLOT_ATTRIBUTE_1

    if prev_scatter_var_2 in valid_attributes:
        default_value_2 = prev_scatter_var_2
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


# Update scatter plot parameters object
@callback(
    Output('scatter-plot-params', 'data'),
    Input('scatter-dropdown-1', 'value'),
    Input('scatter-dropdown-2', 'value'),
    Input('display-size', 'children'),
    Input('excluded-fighter-ids-mem', 'data'),
    Input('game-selector-buttons', 'value'),
    Input('scatter-image-size-slider', 'value'),
    State('scatter-plot-params', 'data'),
)
def update_scatter_plot_params(
    scatter_var_1,
    scatter_var_2,
    display_size_str,
    excluded_fighter_ids_mem,
    selected_game,
    image_size_slider_val,
    scatter_plot_params,
):
    screen_width = get_screen_width(display_size_str)
    excluded_fighter_ids = get_excluded_fighter_ids(excluded_fighter_ids_mem)
    image_size_multiplier = calc_image_size_multiplier(image_size_slider_val)

    prev_scatter_var_1 = scatter_plot_params['var_1']
    prev_scatter_var_2 = scatter_plot_params['var_2']
    prev_screen_width = scatter_plot_params['screen_width']
    prev_excluded_fighter_ids = scatter_plot_params['excluded_fighter_ids']
    prev_selected_game = scatter_plot_params['selected_game']
    prev_image_size_multiplier = scatter_plot_params['image_size_multiplier']

    if scatter_var_1 is None:
        scatter_var_1 = prev_scatter_var_1
    if scatter_var_2 is None:
        scatter_var_2 = prev_scatter_var_2
    if screen_width is None:
        screen_width = prev_screen_width
    if abs(image_size_multiplier - prev_image_size_multiplier) < 0.02:
        image_size_multiplier = prev_image_size_multiplier

    # Prevent unnecessary updates:
    if (
        scatter_var_1 == prev_scatter_var_1
        and scatter_var_2 == prev_scatter_var_2
        and screen_width == prev_screen_width
        and set(excluded_fighter_ids) == set(prev_excluded_fighter_ids)
        and selected_game == prev_selected_game
        and round(image_size_multiplier, 2) == round(prev_image_size_multiplier, 2)
    ):
        raise PreventUpdate

    return {
        'var_1': scatter_var_1,
        'var_2': scatter_var_2,
        'screen_width': screen_width,
        'excluded_fighter_ids': excluded_fighter_ids,
        'selected_game': selected_game,
        'image_size_multiplier': image_size_multiplier,
    }


# Update the scatter plot
@callback(
    Output('scatter-plot', 'spec'),
    Output('scatter-title', 'children'),
    Input('scatter-plot-params', 'data'),
)
def update_scatter_plot(scatter_plot_params):
    title_params = {
        key: scatter_plot_params[key]
        for key in ['var_1', 'var_2']
        if key in scatter_plot_params
    }

    return (
        get_scatter_plot(**scatter_plot_params).to_dict(),
        get_scatter_plot_title(**title_params),
    )


# Update the correlation matrix plot
@callback(
    Output('corr-matrix-plot', 'spec'),
    Input('scatter-plot-params', 'data'),
)
def update_corr_matrix_plot(scatter_plot_params):
    corr_matrix_params = {
        key: scatter_plot_params[key]
        for key in ['var_1', 'var_2', 'screen_width']
        if key in scatter_plot_params
    }

    return get_corr_matrix_plot(**corr_matrix_params).to_dict()


def calc_image_size_multiplier(x):
    if not isinstance(x, int | float):
        return 1.0
    # f(0) = 1/2; f(1) = 1; f(2) = 2
    return (0.25 * x**2) + (0.25 * x) + 0.5
