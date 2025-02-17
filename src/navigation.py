import dash_mantine_components as dmc
from dash import html

from utils import get_icon, get_logo

COLLAPSED_SIDEBAR_WIDTH = 76
EXPANDED_SIDEBAR_WIDTH = 240

COLLAPSED_SIDEBAR_NAVLINK_MARGIN = 6
EXPANDED_SIDEBAR_NAVLINK_MARGIN = 12

COLLAPSED_SIDEBAR_NAVLINK_WIDTH = (
    COLLAPSED_SIDEBAR_WIDTH - 0 * COLLAPSED_SIDEBAR_NAVLINK_MARGIN
)
EXPANDED_SIDEBAR_NAVLINK_WIDTH = EXPANDED_SIDEBAR_WIDTH - EXPANDED_SIDEBAR_NAVLINK_MARGIN

DRAWER_SIZE = EXPANDED_SIDEBAR_WIDTH + EXPANDED_SIDEBAR_NAVLINK_MARGIN


def get_menu_button(div_id, button_type, initial_load=False):
    # Don't display during the initial load:
    style = {'visibility': 'hidden'} if initial_load else None

    icons_dict = {
        'hamburger': 'ci:hamburger-md',
        'settings': 'ci:settings',
    }

    icon = icons_dict.get(button_type, 'ph:square')

    return dmc.ActionIcon(
        get_icon(icon, height=36),
        id=div_id,
        className=f'{button_type}-menu-button',
        color='dark',
        radius='20px',
        style=style,
    )


def get_sidebar_contents(pages):
    return [get_navlink(page, 'sidebar') for page in pages]


def get_drawer_contents(pages):
    return [get_navlink(page, 'drawer') for page in pages]


def get_page_icon(page_name, height=24, variant=None):
    variant = '_' + variant if variant else ''  # append '_' to variant if not None

    icons_dict = {
        'Home': f'ph:house{variant}',
        'Attribute correlations': f'ph:chart-scatter{variant}',
        'Attribute distributions': f'ph:chart-bar{variant}',
        'Attribute info': f'ph:info{variant}',
    }

    icon = icons_dict.get(page_name, f'ph:square{variant}')

    return get_icon(icon=icon, height=height)


def get_navlink(page, nav_type):
    return dmc.NavLink(
        label=page['name'].title(),
        href=page['relative_path'],
        icon=get_page_icon(page_name=page['name'], height=32),
        id=f'{nav_type}-navlink-' + page['relative_path'],
        color='dark',
        variant='light',
        style=get_navlink_style(),
        styles=get_navlink_styles(),
    )


def get_sidebar(pages):
    sidebar_contents = get_sidebar_contents(pages)

    return html.Div(
        id='sidebar-container',
        children=[
            dmc.Navbar(
                children=sidebar_contents,
                id='sidebar',
                style=get_sidebar_style(initial_load=True),
                fixed=True,
            ),
        ],
    )


def get_drawer(pages):
    logo = get_logo()
    hamburger_menu_drawer_inner = get_menu_button(
        div_id='hamburger-menu-button-drawer-inner',
        button_type='hamburger',
    )
    drawer_header = html.Div(
        id='drawer-header',
        children=[hamburger_menu_drawer_inner, logo],
    )

    drawer_contents = get_drawer_contents(pages)

    return dmc.Drawer(
        children=[drawer_header, *drawer_contents],
        id='drawer',
        withCloseButton=False,
        transitionDuration=100,
        size=DRAWER_SIZE,
        padding=0,
        zIndex=90000,
    )


def get_navlink_styles(is_collapsed=False):
    # Navlink 'styles' refers to the styles of the children of the navlink,
    # not to the style of the navlink itself.

    if is_collapsed:
        navlink_styles = {
            'label': {
                'overflow': 'visible',
                'font-size': '11px',
                'line-height': '0.85',
                # "background-color": "yellow"
            },
            'body': {
                'overflow': 'visible',
                'position': 'relative',
                'left': '-58px',
                'top': '28px',
                'text-align': 'center',
                'min-height': '48px',
                'min-width': f'{COLLAPSED_SIDEBAR_NAVLINK_WIDTH}px',
                'line-height': '0.0em',
                # "background-color": "red",
            },
            'icon': {
                'position': 'relative',
                'top': '-12px',
                'left': '8px',
                # "background-color": "blue"
            },
        }
    else:
        navlink_styles = {
            'label': {
                'overflow': 'visible',
                'font-size': '15px',
                'position': 'relative',
                'left': f'{COLLAPSED_SIDEBAR_NAVLINK_MARGIN - 8}px',
            },
            'body': {
                'overflow': 'visible',
            },
            'icon': {
                'position': 'relative',
                'left': f'{COLLAPSED_SIDEBAR_NAVLINK_MARGIN - 4}px',
            },
        }

    return navlink_styles


def get_navlink_style(is_collapsed=False):
    if is_collapsed:
        navlink_style = {
            'height': '72px',
            'width': f'{COLLAPSED_SIDEBAR_NAVLINK_WIDTH}px',
            'border-radius': '10px',
            'margin-left': f'{COLLAPSED_SIDEBAR_NAVLINK_MARGIN}px',
            'margin-right': f'{COLLAPSED_SIDEBAR_NAVLINK_MARGIN}px',
        }
    else:
        navlink_style = {
            'height': '48px',
            'width': f'{EXPANDED_SIDEBAR_NAVLINK_WIDTH}px',
            'border-radius': '10px',
            'margin-left': f'{EXPANDED_SIDEBAR_NAVLINK_MARGIN}px',
            'margin-right': f'{EXPANDED_SIDEBAR_NAVLINK_MARGIN}px',
        }

    return navlink_style


def get_sidebar_style(is_collapsed=False, initial_load=False):
    if initial_load:
        sidebar_style = {
            'display': 'none',
            'width': f'{EXPANDED_SIDEBAR_WIDTH}px',
        }
    elif is_collapsed:
        sidebar_style = {
            'width': f'{COLLAPSED_SIDEBAR_WIDTH}px',
        }
    else:
        sidebar_style = {
            'width': f'{EXPANDED_SIDEBAR_WIDTH}px',
        }

    return sidebar_style


def get_dummy_sidebar_style(is_collapsed=False, initial_load=False):
    dummy_sidebar_style = get_sidebar_style(
        is_collapsed=is_collapsed,
        initial_load=initial_load,
    )
    if not initial_load:
        dummy_sidebar_style['float'] = 'left'

    return dummy_sidebar_style


def get_sidebar_style_outputs(is_collapsed, num_pages):
    navlink_styles = get_navlink_styles(is_collapsed)
    navlink_style = get_navlink_style(is_collapsed)
    sidebar_style = get_sidebar_style(is_collapsed)
    dummy_sidebar_style = get_dummy_sidebar_style(is_collapsed)

    return tuple(
        num_pages * [navlink_styles]
        + num_pages * [navlink_style]
        + [sidebar_style, dummy_sidebar_style],
    )


def get_page_container_style(sidebar_status):
    if sidebar_status not in ['hidden', 'collapsed', 'expanded']:
        raise ValueError(
            """
                Error during get_page_container_style.
                The input 'sidebar_status' should be one of \
                "collapsed", "expanded", or "hidden".
            """,
        )

    if sidebar_status == 'hidden':
        page_container_style = {
            'width': '99%',
        }
    else:
        if sidebar_status == 'collapsed':
            sidebar_offset = int(
                COLLAPSED_SIDEBAR_WIDTH
                + (2 / 3) * COLLAPSED_SIDEBAR_NAVLINK_MARGIN,  # idk, it just works
            )
        else:  # expanded
            sidebar_offset = int(
                EXPANDED_SIDEBAR_WIDTH
                + (2 / 3) * EXPANDED_SIDEBAR_NAVLINK_MARGIN,  # idk, it just works
            )
        page_container_style = {
            'width': f'calc(100vw - {sidebar_offset}px)',
        }

    return page_container_style
