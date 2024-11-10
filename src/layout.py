from dash import html
import dash_vega_components as dvc
import dash_mantine_components as dmc
from utils import get_logo, get_vertical_spacer
from navigation import (
    get_sidebar,
    get_drawer,
    get_menu_button
)
from plots import get_character_selector_chart

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
                footer
            ]
        )
    ]

    return app_html

def get_header():
    logo = get_logo()

    # For opening the drawer
    hamburger_menu_drawer_outer = get_menu_button(
        div_id="hamburger-menu-button-drawer-outer",
        type="hamburger",
        initial_load=True
    )

    # For opening the settings menu
    settings_menu_button = get_menu_button(
        div_id="settings-menu-button",
        type="settings",
        initial_load=False
    )

    page_title = html.Div(
        children=[html.H1(html.Br(), id='page-title')],
        id='page-title-container'
    )

    header = html.Div(
        id='header',
        children=[
            logo,
            hamburger_menu_drawer_outer,
            page_title,
            settings_menu_button
        ]
    )

    return header

def get_settings_menu():
    settings_menu_contents = html.Div(
        id="settings-menu-wrapper",
        children=[
            html.H3("Settings"),
            get_vertical_spacer(height=10),
            html.H5("Select Characters:"),
            dvc.Vega(
                id="character-selector-chart",
                spec=get_character_selector_chart().to_dict(),
                signalsToObserve=["character_selector"],
                opt={"renderer": "svg", "actions": False}
            ),
            html.Div(id='excluded-characters', style={'display': 'None'})
        ]
    )

    settings_menu = dmc.Drawer(
        children=settings_menu_contents,
        id="settings-menu-drawer",
        withCloseButton=True,
        transitionDuration=100,
        size=350,
        position="right",
        padding=15,
        zIndex=80000
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
                        )
                    ),
                    html.Div(
                        id='page-container',
                        children=[settings_menu, dash_page_container],
                        style={'display': 'none'} # Just for the initial load
                    ),
                ],
            )
        ],
    )

    return page_container

def get_footer():
    return html.Div(
        id="footer",
        children=[get_credits()]
    )

def get_credits():
    app_credits = html.Div(
        children=[
            html.A(
                "Smash Charts", 
                href="https://github.com/J99thoms/Super-Smash-Dashboard",
                target="_blank",
                style={"color": "white"}
            ),
            " was created by ",
            html.A(
                "Jakob Thoms", 
                href="https://github.com/J99thoms",
                target="_blank",
                style={"color": "white"}
            ),
            "."
        ],
        style={
            "text-align": "right", 
            "padding-right": "10px", 
            "padding-left": "10px", 
            "font-size": "83%"
        }
    )
    
    return app_credits
