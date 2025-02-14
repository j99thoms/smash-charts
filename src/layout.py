import dash_mantine_components as dmc
import dash_vega_components as dvc
from dash import dcc, html

from navigation import get_drawer, get_menu_button, get_sidebar
from utils import get_icon, get_logo, get_vertical_spacer, initialize_excluded_fighters


def get_app_html(pages, dash_page_container):
    header = get_header()
    sidebar = get_sidebar(pages)
    drawer = get_drawer(pages)
    page_container = get_page_container(dash_page_container)
    footer = get_footer()

    app_html = [
        html.Div(
            id='user-window',
            children=[
                header,
                drawer,
                sidebar,
                page_container,
                footer,
            ],
        ),
    ]

    return app_html


def get_header():
    logo = get_logo()

    # For opening the drawer
    hamburger_menu_drawer_outer = get_menu_button(
        div_id='hamburger-menu-button-drawer-outer',
        button_type='hamburger',
        initial_load=True,
    )

    # For opening the settings menu
    settings_menu_button = get_menu_button(
        div_id='settings-menu-button',
        button_type='settings',
        initial_load=False,
    )

    page_title = html.Div(
        children=[html.H1(html.Br(), id='page-title')],
        id='page-title-container',
    )

    header = html.Div(
        id='header',
        children=[
            hamburger_menu_drawer_outer,
            logo,
            page_title,
            settings_menu_button,
        ],
    )

    return header


def get_game_selector_buttons():
    game_selector_buttons = dcc.RadioItems(
        options={
            'ultimate': 'SSB Ultimate',
            'melee': 'SSB Melee',
        },
        value='ultimate',
        id='game-selector-buttons',
        style={'display': 'none'},  # Just for the initial load
    )

    return game_selector_buttons


def get_settings_menu():
    settings_menu_contents = html.Div(
        id='settings-menu-wrapper',
        children=[
            html.H3('Settings'),
            get_vertical_spacer(height=10),
            html.H5('Select Game:'),
            get_game_selector_buttons(),
            get_vertical_spacer(height=5),
            html.H5('Select Fighters:'),
            dvc.Vega(
                id='fighter-selector-chart',
                spec=None,
                signalsToObserve=['fighter_selector'],
                opt={'renderer': 'svg', 'actions': False},
                style={'z-index': '9999'},
            ),
            dcc.Store(id='cache-breaker', storage_type='memory', data=999),
            dcc.Store(id='char-selector-mem', storage_type='memory'),
            dcc.Store(id='excluded-char-ids-mem', storage_type='memory'),
            dcc.Store(id='settings-btn-last-press', storage_type='memory'),
            dcc.Store(
                id='excluded-fighter-numbers',
                storage_type='memory',
                data=initialize_excluded_fighters(),
            ),
            dmc.Button(
                html.Span('Select All'),
                leftIcon=get_icon('ci:select-multiple', height=30),
                id='fighter-selector-reset-button',
                color='dark',
                radius='15px',
                variant='outline',
            ),
            dmc.Button(
                html.Span('Remove All'),
                leftIcon=get_icon('mdi:clear-circle-outline', height=30),
                id='fighter-selector-clear-all-button',
                color='dark',
                radius='15px',
                variant='outline',
            ),
        ],
    )

    settings_menu = dmc.Drawer(
        children=settings_menu_contents,
        id='settings-menu-drawer',
        withCloseButton=True,
        transitionDuration=100,
        size=350,
        position='right',
        padding=15,
        zIndex=999,
    )

    return settings_menu


def get_page_container(dash_page_container):
    settings_menu = get_settings_menu()

    page_container = html.Div(
        id='wrapper-outer',
        children=[
            html.Div(
                id='wrapper-inner',
                children=[
                    html.Div(
                        id='dummy-sidebar-container',
                        children=html.Div(
                            id='dummy-sidebar',
                        ),
                    ),
                    html.Div(
                        id='page-container',
                        children=[settings_menu, dash_page_container],
                        style={'display': 'none'},  # Just for the initial load
                    ),
                ],
            ),
        ],
    )

    return page_container


def get_footer():
    return html.Div(
        id='footer',
        children=[get_credits()],
    )


def get_credits():
    app_credits = html.Div(
        children=[
            html.A(
                'Smash Charts',
                href='https://github.com/J99thoms/Super-Smash-Dashboard',
                target='_blank',
                style={'color': 'white'},
            ),
            ' was created by ',
            html.A(
                'Jakob Thoms',
                href='https://github.com/J99thoms',
                target='_blank',
                style={'color': 'white'},
            ),
            '.',
        ],
        style={
            'text-align': 'right',
            'padding-right': '10px',
            'padding-left': '10px',
            'font-size': '83%',
        },
    )

    return app_credits
