from dash import html
from utils import get_logo
from navigation import (
    get_sidebar,
    get_drawer,
    get_hamburger_menu
)

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
    hamburger_menu_drawer_outer = get_hamburger_menu(
        div_id="hamburger-menu-button-drawer-outer",
        initial_load=True
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
            page_title
        ]
    )

    return header

def get_page_container(dash_page_container):
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
                        children=[dash_page_container],
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
