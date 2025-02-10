from datetime import datetime, timedelta

import dash
import dash_bootstrap_components as dbc
import dash_vega_components as dvc
from dash import Input, Output, State, callback, ctx, dcc, html
from dash.exceptions import PreventUpdate

from plots import DEFAULT_BAR_CHART_ATTRIBUTE, get_bar_chart, get_bar_chart_title
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
                        # Invisible divs used to track last selected var:
                        html.Div(
                            id='last-selected-bar-var',
                            children=DEFAULT_BAR_CHART_ATTRIBUTE,
                            style={'display': 'None'},
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
        dcc.Store(id='bar-prev-excluded-char-ids-mem', storage_type='session'),
    ],
)


# Update dropdown list when game is changed
@callback(
    Output('bar-dropdown-container', 'children'),
    Input('game-selector-buttons', 'value'),
    State('last-selected-bar-var', 'children'),
)
def update_bar_dropdown(
    selected_game,
    last_selected_attribute,
):
    if last_selected_attribute in get_fighter_attributes_df(game=selected_game).columns:
        default_value = last_selected_attribute
    else:
        default_value = DEFAULT_BAR_CHART_ATTRIBUTE

    dropdown = get_attribute_selector_dropdown(
        div_id='bar-dropdown',
        default_value=default_value,
        game=selected_game,
    )

    return dropdown


# Track which variable was selected last
@callback(
    Output('last-selected-bar-var', 'children'),
    Input('bar-dropdown', 'value'),
    State('last-selected-bar-var', 'children'),
)
def update_last_selected_bar_var(
    selected_attribute,
    last_selected_attribute,
):
    if selected_attribute is not None:
        last_selected_attribute = selected_attribute

    return last_selected_attribute


# Update the bar chart
@callback(
    Output('bar-chart', 'spec'),
    Output('bar-title', 'children'),
    Output('bar-prev-excluded-char-ids-mem', 'data'),
    Input('bar-dropdown', 'value'),
    Input('display-size', 'children'),
    Input('excluded-char-ids-mem', 'data'),
    Input('game-selector-buttons', 'value'),
    State('last-selected-bar-var', 'children'),
    State('bar-prev-excluded-char-ids-mem', 'data'),
    State('excluded-char-ids-mem', 'modified_timestamp'),
    State('settings-btn-last-press', 'data'),
)
def update_bar_chart(
    selected_attribute,
    display_size_str,
    excluded_char_ids_mem,
    selected_game,
    last_selected_attribute,
    prev_excluded_char_ids_mem,
    excluded_char_ids_last_update,
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
            delta = timedelta(seconds=2)
            if last_press_time <= now <= (last_press_time + delta):
                raise PreventUpdate('Halting because update is unnecessary.')

        if (
            excluded_char_ids_last_update is not None
            and excluded_char_ids_last_update > 0
        ):
            last_update_unix = excluded_char_ids_last_update / 1000
            last_update_time = datetime.fromtimestamp(last_update_unix)
            delta = timedelta(seconds=2)
            if last_update_time <= now <= (last_update_time + delta):
                raise PreventUpdate('Halting because update is unnecessary.')

    if selected_attribute is None:
        selected_attribute = last_selected_attribute

    plot = get_bar_chart(
        var=selected_attribute,
        screen_width=screen_width,
        excluded_fighter_ids=excluded_char_ids,
        selected_game=selected_game,
    )

    title = get_bar_chart_title(selected_attribute)

    return plot.to_dict(), title, excluded_char_ids_mem
