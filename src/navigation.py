from dash import html
import dash_mantine_components as dmc
from utils import get_icon, get_logo

COLLAPSED_NAVBAR_WIDTH = 76
EXPANDED_NAVBAR_WIDTH = 240

COLLAPSED_NAVBAR_NAVLINK_MARGIN = 6
EXPANDED_NAVBAR_NAVLINK_MARGIN = 12

collapsed_sidebar_navlink_width = (
    COLLAPSED_NAVBAR_WIDTH - 0*COLLAPSED_NAVBAR_NAVLINK_MARGIN
)
expanded_sidebar_navlink_width = (
    EXPANDED_NAVBAR_WIDTH - EXPANDED_NAVBAR_NAVLINK_MARGIN
)

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

def get_sidebar_contents(pages):
    sidebar_contents = [
        dmc.NavLink(
            label=page['name'].title(),
            href=page['relative_path'],
            icon=get_icon(icon="bi:house-door-fill", height=24), #TODO: page icons
            id="sidebar-navlink-" + page['relative_path'],
            color='dark',
            variant="light",
            style=get_navlink_style(),
            styles=get_navlink_styles()
        )
        for page in pages
    ]

    return sidebar_contents

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


def get_sidebar(pages):
    hamburger_menu = get_hamburger_menu(
        div_id="hamburger-menu-button-sidebar"
    )
    logo=get_logo()

    sidebar_contents = get_sidebar_contents(pages)

    sidebar = html.Div(
        id='sidebar-container',
        children=[
            dmc.Navbar(
                # children=[hamburger_menu, logo] + sidebar_contents,
                children=sidebar_contents,
                id="sidebar",
                style=get_sidebar_style(initial_load=True),
                fixed=True,
            )
        ]
    )

    return sidebar

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
        size=(EXPANDED_NAVBAR_WIDTH+EXPANDED_NAVBAR_NAVLINK_MARGIN),
        padding=0,
        zIndex=90000,
    )

    return drawer


def get_navlink_styles(is_collapsed=False):
    collapsed_navlink_styles = {
        "label": {
            "overflow": "visible",
            "font-size": "11px",
            # "background-color": "yellow"
        },
        "body": {
            "overflow": "visible", 
            "position": "relative", 
            "left": "-48px", 
            "top": "20px", 
            "text-align" : "center", 
            "min-height": "48px",
            "min-width": f"{collapsed_sidebar_navlink_width}px",
            "line-height": "0.0em",
            # "background-color": "red",
        },
        "icon": {
            "position": "relative", 
            "top": "-12px", 
            "left": "12px",
            # "background-color": "blue"
        }
    }
    expanded_navlink_styles = {
        "label": {
            "overflow": "visible",
            "font-size": "15px",
            "position": "relative", 
            "left": f"{COLLAPSED_NAVBAR_NAVLINK_MARGIN}px", # Line up with collapsed navlinks
        },
        "body": {
            "overflow": "visible"
        },
        "icon": {
            "position": "relative", 
            "left": f"{COLLAPSED_NAVBAR_NAVLINK_MARGIN}px",  # Line up with collapsed navlinks
        }
    }

    if is_collapsed:
        return collapsed_navlink_styles
    else:
        return expanded_navlink_styles

def get_navlink_style(is_collapsed=False):
    collapsed_navlink_style = {
        "height": "72px", 
        "width": f"{collapsed_sidebar_navlink_width}px",
        "border-radius": "10px", 
        "margin-left": f"{COLLAPSED_NAVBAR_NAVLINK_MARGIN}px", 
        "margin-right": f"{COLLAPSED_NAVBAR_NAVLINK_MARGIN}px", 
    }
    expanded_navlink_style = {
        "height": "48px", 
        "width": f"{expanded_sidebar_navlink_width}px",
        "border-radius": "10px", 
        "margin-left": f"{EXPANDED_NAVBAR_NAVLINK_MARGIN}px", 
        "margin-right": f"{EXPANDED_NAVBAR_NAVLINK_MARGIN}px", 
    }

    if is_collapsed:
        return collapsed_navlink_style
    else:
        return expanded_navlink_style

def get_sidebar_style(is_collapsed=False, initial_load=False):
    if initial_load:
        return {"display": "none", "width": f"{EXPANDED_NAVBAR_WIDTH}px"}

    collapsed_sidebar_style = {
        "width": f"{COLLAPSED_NAVBAR_WIDTH}px",
        # "border-right": "2px solid black",
    }
    expanded_sidebar_style = {
        "width": f"{EXPANDED_NAVBAR_WIDTH}px",
        # "border-right": "2px solid black",
    }
    
    if is_collapsed:
        return collapsed_sidebar_style
    else:
        return expanded_sidebar_style
    

def get_dummy_sidebar_style(is_collapsed=False, initial_load=False):
    if initial_load:
        return {"display": "none", "width": f"{EXPANDED_NAVBAR_WIDTH}px"}
    
    collapsed_dummy_sidebar_style = {
        "width": f"{COLLAPSED_NAVBAR_WIDTH}px",
        'float': 'left',
    }
    expanded_dummy_sidebar_style = {
        "width": f"{EXPANDED_NAVBAR_WIDTH}px",
        'float': 'left',
    }
    
    if is_collapsed:
        return collapsed_dummy_sidebar_style
    else:
        return expanded_dummy_sidebar_style

def get_sidebar_style_outputs(is_collapsed, num_pages):
    navlink_styles = get_navlink_styles(is_collapsed)
    navlink_style = get_navlink_style(is_collapsed)
    sidebar_style = get_sidebar_style(is_collapsed)
    dummy_sidebar_style = get_dummy_sidebar_style(is_collapsed)

    return tuple(
            num_pages * [navlink_styles]
            +
            num_pages * [navlink_style]
            +
            [
                sidebar_style,
                dummy_sidebar_style
            ]
        )

def get_page_container_style(sidebar_status):
    collapsed_sidebar_offset = int(
        COLLAPSED_NAVBAR_WIDTH + (2/3)*COLLAPSED_NAVBAR_NAVLINK_MARGIN # idk, it just works
    )
    expanded_sidebar_offset = int(
        EXPANDED_NAVBAR_WIDTH + (2/3)*EXPANDED_NAVBAR_NAVLINK_MARGIN # idk, it just works
    )

    page_container_style_collapsed_sidebar = {
        "width": f"calc(100vw - {collapsed_sidebar_offset}px)"
    }
    page_container_style_expanded_sidebar = {
        "width": f"calc(100vw - {expanded_sidebar_offset}px)"
    }
    page_container_style_hidden_sidebar = {
        "width": "99%"
    }

    if sidebar_status == "collapsed":
        return page_container_style_collapsed_sidebar
    elif sidebar_status == "expanded":
        return page_container_style_expanded_sidebar
    elif sidebar_status == "hidden":
        return page_container_style_hidden_sidebar
    else:
        raise ValueError(
            """
                Error during get_page_container_style. 
                The input 'sidebar_status' should be one of \
                "collapsed", "expanded", or "hidden".
            """
        )
