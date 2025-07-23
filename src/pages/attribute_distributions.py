import dash
import dash_bootstrap_components as dbc
import dash_vega_components as dvc
from dash import Input, Output, State, callback, dcc, html
from dash.exceptions import PreventUpdate

from plots import DEFAULT_BAR_CHART_ATTRIBUTE, get_bar_chart, get_bar_chart_title
from utils import (
    get_attribute_selector_dropdown,
    get_excluded_fighter_ids,
    get_screen_width,
    get_valid_attributes,
    get_vertical_spacer,
    get_window_title,
)

dash.register_page(__name__, title=get_window_title(__name__), order=2)

layout = html.Div(
    className='inner-page-container',
    children=[
        dbc.Row(
            [
                # Attribute selection (1x dropdown list)
                html.Div(
                    children=[
                        html.Div(
                            children=html.H4('Choose an attribute:'),
                            style={
                                'width': '270px',
                                'padding-left': '5px',
                            },
                        ),
                        html.Div(
                            id='bar-dropdown-container',
                            children=[
                                get_attribute_selector_dropdown(
                                    div_id='bar-dropdown',
                                    default_value=DEFAULT_BAR_CHART_ATTRIBUTE,
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
                # Bar chart
                html.H3(
                    id='bar-title',
                    style={
                        'height': '6%',
                        'width': '100%',
                        'text-align': 'center',
                    },
                ),
                dvc.Vega(
                    id='bar-chart',
                    className='bar-chart-frame',
                    opt={'renderer': 'svg', 'actions': False},
                ),
            ],
        ),
        dcc.Store(
            id='bar-chart-params',
            storage_type='memory',
            data={
                'var': DEFAULT_BAR_CHART_ATTRIBUTE,
                'screen_width': 900,
                'excluded_fighter_ids': [],
                'selected_game': 'ultimate',
            },
        ),
    ],
)


# Update dropdown list when game is changed
@callback(
    Output('bar-dropdown-container', 'children'),
    Input('game-selector-buttons', 'value'),
    State('bar-chart-params', 'data'),
)
def update_bar_dropdown(selected_game, bar_chart_params):
    prev_selected_var = bar_chart_params['var']

    if prev_selected_var in get_valid_attributes(data_type='all', game=selected_game):
        default_value = prev_selected_var
    else:
        default_value = DEFAULT_BAR_CHART_ATTRIBUTE

    return get_attribute_selector_dropdown(
        div_id='bar-dropdown',
        default_value=default_value,
        game=selected_game,
    )


# Update bar chart parameters object
@callback(
    Output('bar-chart-params', 'data'),
    Input('bar-dropdown', 'value'),
    Input('display-size', 'children'),
    Input('excluded-fighter-ids-mem', 'data'),
    Input('game-selector-buttons', 'value'),
    State('bar-chart-params', 'data'),
)
def update_scatter_plot_params(
    selected_var,
    display_size_str,
    excluded_fighter_ids_mem,
    selected_game,
    bar_chart_params,
):
    screen_width = get_screen_width(display_size_str)
    excluded_fighter_ids = get_excluded_fighter_ids(excluded_fighter_ids_mem)

    prev_selected_var = bar_chart_params['var']
    prev_screen_width = bar_chart_params['screen_width']
    prev_excluded_fighter_ids = bar_chart_params['excluded_fighter_ids']
    prev_selected_game = bar_chart_params['selected_game']

    if selected_var is None:
        selected_var = prev_selected_var
    if screen_width is None:
        screen_width = prev_screen_width

    # Prevent unnecessary updates:
    if (
        selected_var == prev_selected_var
        and screen_width == prev_screen_width
        and set(excluded_fighter_ids) == set(prev_excluded_fighter_ids)
        and selected_game == prev_selected_game
    ):
        raise PreventUpdate

    return {
        'var': selected_var,
        'screen_width': screen_width,
        'excluded_fighter_ids': excluded_fighter_ids,
        'selected_game': selected_game,
    }


# Update the bar chart
@callback(
    Output('bar-chart', 'spec'),
    Output('bar-title', 'children'),
    Input('bar-chart-params', 'data'),
)
def update_bar_chart(bar_chart_params):
    return (
        get_bar_chart(**bar_chart_params),
        get_bar_chart_title(bar_chart_params['var']),
    )
