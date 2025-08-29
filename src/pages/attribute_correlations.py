from json import loads

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
    get_icon,
    get_screen_height,
    get_screen_width,
    get_valid_attributes,
    get_vertical_spacer,
    get_window_title,
)

dash.register_page(__name__, title=get_window_title(__name__), order=3)

# Define preset attribute pairs for quick selection
PRESET_PAIRS = [
    {
        'label': 'Fastfall Speed vs. Run Speed',
        'x': 'fastfall_speed',
        'y': 'run_speed',
    },
    {
        'label': 'Run Speed vs. Initial Dash Speed',
        'x': 'run_speed',
        'y': 'initial_dash_speed',
    },
    {
        'label': 'Weight vs. Gravity',
        'x': 'weight',
        'y': 'gravity',
    },
]

preset_buttons = [
    dbc.Button(
        preset['label'],
        id={'type': 'preset-button', 'index': i},
        color='light',
        size='sm',
        className='w-100 mb-2',
    )
    for i, preset in enumerate(PRESET_PAIRS)
]

plot_controls_card = dbc.Card(
    className='mb-3',
    children=[
        dbc.CardBody(
            [
                html.H4('Choose Attributes', className='mb-3'),
                html.Div(
                    id='scatter-dropdown-container',
                    children=[
                        html.Label('X-Axis:', className='mb-1'),
                        get_attribute_selector_dropdown(
                            div_id='scatter-dropdown-1',
                            default_value=DEFAULT_SCATTER_PLOT_ATTRIBUTE_1,
                            data_type='continuous',
                        ),
                        get_vertical_spacer(height=12),
                        html.Label('Y-Axis:', className='mb-1'),
                        get_attribute_selector_dropdown(
                            div_id='scatter-dropdown-2',
                            default_value=DEFAULT_SCATTER_PLOT_ATTRIBUTE_2,
                            data_type='continuous',
                        ),
                    ],
                ),
                get_vertical_spacer(height=16),
                dbc.Button(
                    [get_icon('mdi:swap-vertical', height=18), ' Swap Axes'],
                    id='swap-axes-button',
                    color='light',
                    size='sm',
                    className='w-100',
                ),
                get_vertical_spacer(height=20),
                html.H5('Quick Selections', className='mb-2'),
                html.Div(
                    id='preset-buttons-container',
                    children=preset_buttons,
                ),
                get_vertical_spacer(height=20),
                html.H5('Chart Options', className='mb-2'),
                html.Label('Fighter Icon Size:', className='mb-1'),
                dcc.Slider(
                    id='scatter-image-size-slider',
                    value=1,
                    min=0,
                    max=2,
                    step=0.1,
                    marks={0: 'S', 1: 'M', 2: 'L'},
                    updatemode='drag',
                ),
                get_vertical_spacer(height=15),
                dbc.Switch(
                    id='scatter-aspect-mode',
                    label='Maintain Square Aspect Ratio',
                    value=True,
                ),
                dbc.Tooltip(
                    [
                        'When enabled, plot maintains 1:1 aspect ratio. ',
                        html.Br(),
                        'When disabled, plot expands to fill available space.',
                    ],
                    target='scatter-aspect-mode',
                    trigger='hover',
                    placement='right',
                ),
            ]
        )
    ],
)

correlation_matrix_card = dbc.Card(
    [
        dbc.CardBody(
            [
                html.Div(
                    [
                        html.H5(
                            'Correlation Matrix',
                            style={'display': 'inline-block'},
                        ),
                        html.Span(
                            get_icon(
                                'mdi:information-outline',
                                height=20,
                            ),
                            id='correlation-info-icon',
                            style={
                                'margin-left': '8px',
                                'cursor': 'help',
                                'vertical-align': 'middle',
                                'opacity': 0.7,
                            },
                        ),
                        dbc.Tooltip(
                            'Correlation is a value between -1 and 1 that '
                            'measures how closely two attributes are related. '
                            'Positive means they increase together, '
                            'negative means they move oppositely. '
                            'Values near ±1 mean a stronger link, '
                            'values near 0 mean a weaker link.',
                            target='correlation-info-icon',
                            placement='right',
                        ),
                    ],
                    className='mb-2',
                ),
                dbc.Collapse(
                    dvc.Vega(
                        id='corr-matrix-plot',
                        className='corr-matrix-plot-frame',
                        opt={'renderer': 'svg', 'actions': False},
                        style={'margin-top': '10px'},
                    ),
                    id='correlation-collapse',
                    is_open=False,
                ),
                dbc.Button(
                    id='toggle-correlation-button',
                    children=[
                        get_icon('mdi:chevron-right', height=18),
                        ' Show Matrix',
                    ],
                    color='link',
                    size='sm',
                    className='p-0',
                ),
            ]
        ),
    ],
)

scatter_plot_card = dbc.Card(
    [
        dbc.CardBody(
            style={'overflow': 'hidden'},
            children=[
                html.Div(
                    [
                        html.H3(
                            id='scatter-title',
                            style={'display': 'inline-block'},
                        ),
                    ],
                    className='mb-3',
                ),
                dvc.Vega(
                    id='scatter-plot',
                    className='scatter-plot-frame',
                    opt={'renderer': 'svg', 'actions': False},
                ),
            ],
        ),
    ],
)

layout = html.Div(
    className='inner-page-container',
    style={'margin-top': '20px'},
    children=[
        dbc.Row(
            [
                # Left column: Controls
                dbc.Col(
                    [
                        plot_controls_card,
                        correlation_matrix_card,
                    ],
                    width=12,
                    lg=3,
                    className='mb-3',
                ),
                # Right column: Scatter plot
                dbc.Col(
                    [
                        scatter_plot_card,
                    ],
                    width=12,
                    lg=9,
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
                'screen_height': 600,
                'excluded_fighter_ids': [],
                'selected_game': 'ultimate',
                'image_size_multiplier': 1.0,
                'maintain_square_aspect': True,
            },
        ),
    ],
)


# Toggle correlation matrix collapse
@callback(
    Output('correlation-collapse', 'is_open'),
    Output('toggle-correlation-button', 'children'),
    Input('toggle-correlation-button', 'n_clicks'),
    State('correlation-collapse', 'is_open'),
)
def toggle_correlation_collapse(n_clicks, is_open):
    if not n_clicks:
        raise PreventUpdate

    is_open = not is_open
    button_text = ' Hide Matrix' if is_open else ' Show Matrix'
    icon = 'mdi:chevron-down' if is_open else 'mdi:chevron-right'

    return is_open, [get_icon(icon, height=18), button_text]


# Update selected attributes when swap axes button is clicked
@callback(
    Output('scatter-dropdown-1', 'value'),
    Output('scatter-dropdown-2', 'value'),
    Input('swap-axes-button', 'n_clicks'),
    State('scatter-dropdown-1', 'value'),
    State('scatter-dropdown-2', 'value'),
)
def swap_axes(n_clicks, var_1, var_2):
    if not n_clicks:
        raise PreventUpdate
    return var_2, var_1


# Handle preset button clicks
@callback(
    Output('scatter-dropdown-1', 'value', allow_duplicate=True),
    Output('scatter-dropdown-2', 'value', allow_duplicate=True),
    Input({'type': 'preset-button', 'index': dash.dependencies.ALL}, 'n_clicks'),
    State('game-selector-buttons', 'value'),
    prevent_initial_call=True,
)
def handle_preset_buttons(n_clicks_list, selected_game):
    if not any(n_clicks_list):
        raise PreventUpdate

    # Find which button was clicked
    ctx = dash.callback_context
    if not ctx.triggered:
        raise PreventUpdate

    button_id = ctx.triggered[0]['prop_id'].split('.')[0]
    button_index = loads(button_id)['index']

    if not n_clicks_list[button_index]:
        raise PreventUpdate

    preset = PRESET_PAIRS[button_index]

    return preset['x'], preset['y']


# Update dropdown list when game is changed
@callback(
    Output('scatter-dropdown-container', 'children'),
    Input('game-selector-buttons', 'value'),
    State('scatter-plot-params', 'data'),
)
def update_scatter_dropdowns(selected_game, scatter_plot_params):
    valid_attributes = get_valid_attributes(data_type='continuous', game=selected_game)
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

    return [
        html.Label('X-Axis:', className='mb-1'),
        get_attribute_selector_dropdown(
            div_id='scatter-dropdown-1',
            default_value=default_value_1,
            data_type='continuous',
            game=selected_game,
        ),
        get_vertical_spacer(height=12),
        html.Label('Y-Axis:', className='mb-1'),
        get_attribute_selector_dropdown(
            div_id='scatter-dropdown-2',
            default_value=default_value_2,
            data_type='continuous',
            game=selected_game,
        ),
    ]


# Update scatter plot parameters object
@callback(
    Output('scatter-plot-params', 'data'),
    Input('scatter-dropdown-1', 'value'),
    Input('scatter-dropdown-2', 'value'),
    Input('display-size-width', 'children'),
    Input('display-size-height', 'children'),
    Input('excluded-fighter-ids-mem', 'data'),
    Input('game-selector-buttons', 'value'),
    Input('scatter-image-size-slider', 'value'),
    Input('scatter-aspect-mode', 'value'),
    State('scatter-plot-params', 'data'),
)
def update_scatter_plot_params(
    scatter_var_1,
    scatter_var_2,
    display_size_width_str,
    display_size_height_str,
    excluded_fighter_ids_mem,
    selected_game,
    image_size_slider_val,
    maintain_square_aspect,
    scatter_plot_params,
):
    screen_width = get_screen_width(display_size_width_str)
    screen_height = get_screen_height(display_size_height_str)
    excluded_fighter_ids = get_excluded_fighter_ids(excluded_fighter_ids_mem)
    image_size_multiplier = calc_image_size_multiplier(image_size_slider_val)

    prev_scatter_var_1 = scatter_plot_params['var_1']
    prev_scatter_var_2 = scatter_plot_params['var_2']
    prev_screen_width = scatter_plot_params['screen_width']
    prev_screen_height = scatter_plot_params['screen_height']
    prev_excluded_fighter_ids = scatter_plot_params['excluded_fighter_ids']
    prev_selected_game = scatter_plot_params['selected_game']
    prev_image_size_multiplier = scatter_plot_params['image_size_multiplier']
    prev_maintain_square_aspect = scatter_plot_params['maintain_square_aspect']

    if scatter_var_1 is None:
        scatter_var_1 = prev_scatter_var_1
    if scatter_var_2 is None:
        scatter_var_2 = prev_scatter_var_2
    if screen_width is None:
        screen_width = prev_screen_width
    if screen_height is None:
        screen_height = prev_screen_height
    if abs(image_size_multiplier - prev_image_size_multiplier) < 0.02:
        image_size_multiplier = prev_image_size_multiplier
    if maintain_square_aspect is None:
        maintain_square_aspect = prev_maintain_square_aspect

    # Prevent unnecessary updates:
    if (
        scatter_var_1 == prev_scatter_var_1
        and scatter_var_2 == prev_scatter_var_2
        and screen_width == prev_screen_width
        and screen_height == prev_screen_height
        and set(excluded_fighter_ids) == set(prev_excluded_fighter_ids)
        and selected_game == prev_selected_game
        and round(image_size_multiplier, 2) == round(prev_image_size_multiplier, 2)
        and maintain_square_aspect == prev_maintain_square_aspect
    ):
        raise PreventUpdate

    return {
        'var_1': scatter_var_1,
        'var_2': scatter_var_2,
        'screen_width': screen_width,
        'screen_height': screen_height,
        'excluded_fighter_ids': excluded_fighter_ids,
        'selected_game': selected_game,
        'image_size_multiplier': image_size_multiplier,
        'maintain_square_aspect': maintain_square_aspect,
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
        get_scatter_plot(**scatter_plot_params),
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

    return get_corr_matrix_plot(**corr_matrix_params)


def calc_image_size_multiplier(x):
    if not isinstance(x, int | float):
        return 1.0
    # f(0) = 1/2; f(1) = 1; f(2) = 2
    return (0.25 * x**2) + (0.25 * x) + 0.5
