import dash
import dash_bootstrap_components as dbc
import dash_vega_components as dvc
from dash import Input, Output, State, callback, dcc, html
from dash.exceptions import PreventUpdate

from plots import (
    DEFAULT_FIGHTER_1,
    DEFAULT_FIGHTER_2,
    get_comparison_plot,
)
from utils import (
    get_fighter_lookup_table,
    get_fighter_selector_dropdown,
    get_screen_width,
    get_vertical_spacer,
    get_window_title,
)

dash.register_page(__name__, title=get_window_title(__name__), order=4)

layout = html.Div(
    className='inner-page-container',
    children=[
        dbc.Row(
            [
                # Fighter selection (2x dropdown lists)
                html.Div(
                    children=[
                        html.Div(
                            children=html.H4('Choose two fighters:'),
                            style={
                                'width': '270px',
                                'padding-left': '5px',
                            },
                        ),
                        html.Div(
                            id='comparison-dropdown-container',
                            children=[
                                get_fighter_selector_dropdown(
                                    div_id='fighter-comparison-dropdown-1',
                                    default_value=DEFAULT_FIGHTER_1,
                                ),
                                get_vertical_spacer(height=8),
                                get_fighter_selector_dropdown(
                                    div_id='fighter-comparison-dropdown-2',
                                    default_value=DEFAULT_FIGHTER_2,
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
                # Comparison plot
                html.Div(
                    [
                        dvc.Vega(
                            id='comparison-plot',
                            className='comparison-plot-frame',
                            opt={'renderer': 'svg', 'actions': False},
                        ),
                    ],
                    style={
                        'display': 'flex',
                        'flex-direction': 'column',
                        'align-items': 'center',
                        'width': '100%',
                        'margin-bottom': '50px',
                    },
                ),
            ],
        ),
        dcc.Store(
            id='comparison-plot-params',
            storage_type='memory',
            data={
                'fighter_1': DEFAULT_FIGHTER_1,
                'fighter_2': DEFAULT_FIGHTER_2,
                'screen_width': 900,
                'selected_game': 'ultimate',
            },
        ),
    ],
)


# Update fighter dropdown list when game is changed
@callback(
    Output('comparison-dropdown-container', 'children'),
    Input('game-selector-buttons', 'value'),
    State('comparison-plot-params', 'data'),
)
def update_fighter_dropdowns(selected_game, comparison_plot_params):
    fighter_lookup = get_fighter_lookup_table(game=selected_game)
    available_fighter_numbers = fighter_lookup['fighter_number'].tolist()
    prev_fighter_1 = comparison_plot_params['fighter_1']
    prev_fighter_2 = comparison_plot_params['fighter_2']

    if prev_fighter_1 in available_fighter_numbers:
        default_fighter_1 = prev_fighter_1
    else:
        default_fighter_1 = DEFAULT_FIGHTER_1

    if prev_fighter_2 in available_fighter_numbers:
        default_fighter_2 = prev_fighter_2
    else:
        default_fighter_2 = DEFAULT_FIGHTER_2

    return [
        get_fighter_selector_dropdown(
            div_id='fighter-comparison-dropdown-1',
            default_value=default_fighter_1,
            game=selected_game,
        ),
        get_vertical_spacer(height=8),
        get_fighter_selector_dropdown(
            div_id='fighter-comparison-dropdown-2',
            default_value=default_fighter_2,
            game=selected_game,
        ),
    ]


# Update comparison plot parameters object
@callback(
    Output('comparison-plot-params', 'data'),
    Input('fighter-comparison-dropdown-1', 'value'),
    Input('fighter-comparison-dropdown-2', 'value'),
    Input('display-size', 'children'),
    Input('game-selector-buttons', 'value'),
    State('comparison-plot-params', 'data'),
)
def update_comparison_params(
    fighter_1,
    fighter_2,
    display_size_str,
    selected_game,
    comparison_plot_params,
):
    screen_width = get_screen_width(display_size_str)

    prev_fighter_1 = comparison_plot_params['fighter_1']
    prev_fighter_2 = comparison_plot_params['fighter_2']
    prev_screen_width = comparison_plot_params['screen_width']
    prev_selected_game = comparison_plot_params['selected_game']

    if fighter_1 is None:
        fighter_1 = prev_fighter_1
    if fighter_2 is None:
        fighter_2 = prev_fighter_2
    if screen_width is None:
        screen_width = prev_screen_width

    # Prevent unnecessary updates
    if (
        fighter_1 == prev_fighter_1
        and fighter_2 == prev_fighter_2
        and screen_width == prev_screen_width
        and selected_game == prev_selected_game
    ):
        raise PreventUpdate

    return {
        'fighter_1': fighter_1,
        'fighter_2': fighter_2,
        'screen_width': screen_width,
        'selected_game': selected_game,
    }


# Update the comparison plot
@callback(
    Output('comparison-plot', 'spec'),
    Input('comparison-plot-params', 'data'),
)
def update_comparison_plot(comparison_plot_params):
    return get_comparison_plot(**comparison_plot_params)
