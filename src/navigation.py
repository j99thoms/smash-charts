from dash import html
import dash_mantine_components as dmc
from utils import get_icon, get_logo

NAVBAR_WIDTH = 240
NAVBAR_NAVLINK_MARGIN = 12

navbar_navlink_width = NAVBAR_WIDTH - NAVBAR_NAVLINK_MARGIN

def get_navbar_contents(pages):
    navbar_contents = [
        dmc.NavLink(
            label=page['name'].title(),
            href=page['relative_path'],
            icon=get_icon(icon="bi:house-door-fill", height=24), #TODO: page icons
            id="navbar-navlink-" + page['relative_path'],
            color='dark',
            variant="light",
            style=get_navlink_style(),
            styles=get_navlink_styles()
        )
        for page in pages
    ]

    return navbar_contents

def get_drawer_contents(pages):
    drawer_contents = [
        dmc.NavLink(
            label=page['name'].title(),
            href=page['relative_path'],
            icon=get_icon(icon="bi:house-door-fill", height=24), #TODO: page icons
            id="drawer-navlink-" + page['relative_path'],
            color='dark',
            variant="light",
            style=get_navlink_style(),
            styles=get_navlink_styles()
        )
        for page in pages
    ]

    return drawer_contents

def get_hamburger_menu(div_id, initial_load=False):
    if initial_load:
        hamburger_menu= dmc.ActionIcon(
            get_icon("ci:hamburger-md", height=36),
            id=div_id,
            className='hamburger-menu',
            color="dark",
            radius="20px",
            style={'display': 'none'}
            # variant="outline"
        )
    else:
        hamburger_menu= dmc.ActionIcon(
            get_icon("ci:hamburger-md", height=36),
            id=div_id,
            className='hamburger-menu',
            color="dark",
            radius="20px",
            # variant="outline"
        )

    return hamburger_menu

def get_navbar(pages):
    hamburger_menu = get_hamburger_menu(
        div_id="hamburger-menu-button-navbar"
    )
    logo=get_logo()

    navbar_contents = get_navbar_contents(pages)

    navbar = html.Div(
        id='navbar-container',
        children=[
            dmc.Navbar(
                # children=[hamburger_menu, logo] + navbar_contents,
                children=navbar_contents,
                id="navbar",
                style=get_navbar_style(initial_load=True),
                fixed=True,
            )
        ]
    )

    return navbar

def get_drawer(pages):
    hamburger_menu_drawer_inner = get_hamburger_menu(
        div_id="hamburger-menu-button-drawer-inner"
    )
    logo=get_logo()

    drawer_header = html.Div(
        children=[logo, hamburger_menu_drawer_inner],
         id='drawer-header'
    )

    drawer_contents = get_drawer_contents(pages)

    drawer = dmc.Drawer(
        # children=[hamburger_menu_drawer_inner, logo] + drawer_contents,
        children=[drawer_header] + drawer_contents,
        id="drawer",
        withCloseButton=False,
        transitionDuration=100,
        size=(NAVBAR_WIDTH+NAVBAR_NAVLINK_MARGIN),
        padding=0,
        zIndex=90000,
    )

    return drawer


def get_navlink_styles():
    navlink_styles = {
        "label": {
            "overflow": "visible",
            "font-size": "15px",
            "position": "relative", 
            "left": "6px",
        },
        "body": {
            "overflow": "visible"
        },
        "icon": {
            "position": "relative", 
            "left": "6px", 
        }
    }

    return navlink_styles

def get_navlink_style():
    navlink_style = {
        "height": "48px", 
        "width": f"{navbar_navlink_width}px",
        "border-radius": "10px", 
        "margin-left": f"{NAVBAR_NAVLINK_MARGIN}px", 
        "margin-right": f"{NAVBAR_NAVLINK_MARGIN}px", 
    }

    return navlink_style

def get_navbar_style(initial_load=False):
    if initial_load:
        return {"display": "none", "width": f"{NAVBAR_WIDTH}px"}

    navbar_style = {
        "width": f"{NAVBAR_WIDTH}px",
        # "border-right": "2px solid black",
    }
    
    return navbar_style
    

def get_dummy_navbar_style(initial_load=False):
    if initial_load:
        return {"display": "none", "width": f"{NAVBAR_WIDTH}px"}
    
    dummy_navbar_style = {
        "width": f"{NAVBAR_WIDTH}px",
        'float': 'left',
    }
    
    return dummy_navbar_style

def get_navbar_style_outputs(num_pages):
    navlink_styles = get_navlink_styles()
    navlink_style = get_navlink_style()
    navbar_style = get_navbar_style()
    dummy_navbar_style = get_dummy_navbar_style()

    return tuple(
            num_pages * [navlink_styles]
            +
            num_pages * [navlink_style]
            +
            [
                navbar_style,
                dummy_navbar_style
            ]
        )

def get_app_container_style(navbar_status):
    navbar_offset = int(
        NAVBAR_WIDTH + (2/3)*NAVBAR_NAVLINK_MARGIN # idk, it just works
    )

    app_container_style_with_navbar = {
        "width": f"calc(100vw - {navbar_offset}px)"
    }
    app_container_style_hidden_navbar = {
        "width": "99%"
    }

    if navbar_status == "shown":
        return app_container_style_with_navbar
    elif navbar_status == "hidden":
        return app_container_style_hidden_navbar
    else:
        raise ValueError(
            """
                Error during get_app_container_style. 
                The input 'navbar_status' should be one of \
                "shown" or "hidden".
            """
        )