import dash
import dash_bootstrap_components as dbc
import dash_vega_components as dvc
from dash import Input, Output, State, callback, dcc, html
from dash.exceptions import PreventUpdate

from layout import get_game_selector_buttons
from plots import (
    DEFAULT_FIGHTER_1,
    DEFAULT_FIGHTER_2,
    get_comparison_plot,
)
from utils import (
    get_fighter_lookup_table,
    get_fighter_selector_dropdown,
    get_icon,
    get_normalization_tooltip,
    get_screen_width,
    get_vertical_spacer,
    get_window_title,
)

dash.register_page(__name__, title=get_window_title(__name__), order=4)

layout = html.Div(
    className='inner-page-container',
    children=[
        html.Div(
            [
                dbc.Row(
                    [
                        # Left column: Fighter selection and normalization controls
                        dbc.Col(
                            [
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
                                get_vertical_spacer(height=20),
                                html.Div(
                                    children=[
                                        html.H4(
                                            'Select Game:', style={'margin-bottom': '8px'}
                                        ),
                                        html.Div(
                                            get_game_selector_buttons(
                                                'game-selector-buttons-comparison'
                                            ),
                                            style={
                                                'display': 'flex',
                                                'flex-direction': 'column',
                                                'gap': '4px',
                                            },
                                        ),
                                    ],
                                    style={'width': '270px', 'padding-left': '5px'},
                                ),
                                get_vertical_spacer(height=20),
                                html.Div(
                                    children=[
                                        html.Div(
                                            [
                                                html.H4(
                                                    'Normalization:',
                                                    style={
                                                        'display': 'inline-block',
                                                        'margin-bottom': '8px',
                                                    },
                                                ),
                                                html.Span(
                                                    get_icon(
                                                        'mdi:information-outline',
                                                        height=20,
                                                    ),
                                                    id='normalization-info-icon',
                                                    style={
                                                        'margin-left': '8px',
                                                        'cursor': 'help',
                                                        'vertical-align': 'middle',
                                                        'opacity': 0.7,
                                                    },
                                                ),
                                                get_normalization_tooltip(),
                                            ],
                                        ),
                                        dcc.RadioItems(
                                            id='normalization-selector',
                                            options=[
                                                {'label': 'None', 'value': 'none'},
                                                {
                                                    'label': 'Min-Max (0-1)',
                                                    'value': 'minmax',
                                                },
                                                {'label': 'Z-Score', 'value': 'zscore'},
                                            ],
                                            value='none',
                                            style={
                                                'display': 'flex',
                                                'flex-direction': 'column',
                                                'gap': '4px',
                                            },
                                        ),
                                    ],
                                    style={'width': '270px', 'padding-left': '5px'},
                                ),
                            ],
                            width=12,
                            md=12,
                            lg=4,
                            style={'margin-bottom': '20px'},
                        ),
                        # Right column: Comparison plot
                        dbc.Col(
                            [
                                dvc.Vega(
                                    id='comparison-plot',
                                    className='comparison-plot-frame',
                                    opt={'renderer': 'svg', 'actions': False},
                                ),
                            ],
                            width=12,
                            md=12,
                            lg=8,
                            style={
                                'display': 'flex',
                                'flex-direction': 'column',
                                'align-items': 'center',
                                'padding-top': '20px',
                                'padding-bottom': '100px',
                            },
                        ),
                    ],
                    style={'margin-bottom': '80px'},
                ),
            ],
            style={
                'max-width': '1400px',
                'margin': '0 auto',
                'width': '100%',
                'float': 'left',
            },
        ),
        dcc.Store(
            id='comparison-plot-params',
            storage_type='memory',
            data={
                'fighter_1': DEFAULT_FIGHTER_1,
                'fighter_2': DEFAULT_FIGHTER_2,
                'screen_width': 900,
                'selected_game': 'ultimate',
                'normalization': 'none',
            },
        ),
    ],
)


# Sync local game selector with global store
@callback(
    Output('game-selector-buttons-comparison', 'value'),
    Input('selected-game-store', 'data'),
)
def sync_game_selector_from_store(selected_game):
    return selected_game if selected_game else 'ultimate'


# Update global store when local game selector changes
@callback(
    Output('selected-game-store', 'data', allow_duplicate=True),
    Input('game-selector-buttons-comparison', 'value'),
    prevent_initial_call=True,
)
def update_store_from_local_selector(selected_game):
    return selected_game


# Update fighter dropdown list when game is changed
@callback(
    Output('comparison-dropdown-container', 'children'),
    Input('game-selector-buttons-comparison', 'value'),
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
    Input('display-size-width', 'children'),
    Input('game-selector-buttons-comparison', 'value'),
    Input('normalization-selector', 'value'),
    State('comparison-plot-params', 'data'),
)
def update_comparison_params(
    fighter_1,
    fighter_2,
    display_size_width_str,
    selected_game,
    normalization,
    comparison_plot_params,
):
    screen_width = get_screen_width(display_size_width_str)

    prev_fighter_1 = comparison_plot_params['fighter_1']
    prev_fighter_2 = comparison_plot_params['fighter_2']
    prev_screen_width = comparison_plot_params['screen_width']
    prev_selected_game = comparison_plot_params['selected_game']
    prev_normalization = comparison_plot_params['normalization']

    if fighter_1 is None:
        fighter_1 = prev_fighter_1
    if fighter_2 is None:
        fighter_2 = prev_fighter_2
    if screen_width is None:
        screen_width = prev_screen_width
    if normalization is None:
        normalization = prev_normalization

    # Prevent unnecessary updates
    if (
        fighter_1 == prev_fighter_1
        and fighter_2 == prev_fighter_2
        and screen_width == prev_screen_width
        and selected_game == prev_selected_game
        and normalization == prev_normalization
    ):
        raise PreventUpdate

    return {
        'fighter_1': fighter_1,
        'fighter_2': fighter_2,
        'screen_width': screen_width,
        'selected_game': selected_game,
        'normalization': normalization,
    }


# Update the comparison plot
@callback(
    Output('comparison-plot', 'spec'),
    Input('comparison-plot-params', 'data'),
)
def update_comparison_plot(comparison_plot_params):
    return get_comparison_plot(**comparison_plot_params)
