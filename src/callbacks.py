from dash import html, Input, Output, State, ctx
from utils import get_screen_width, get_page_title, get_app_title
from navigation import (
    get_sidebar_style_outputs,
    get_page_container_style
)

def get_callbacks(app, num_pages, drawer_pages, sidebar_pages):

    # Update the page title
    # based on the current page's url and the user's screen size
    @app.callback(
        Output('page-title-container', 'children'),
        Input('url', 'pathname'),
        Input('display-size', 'children')
    )
    def update_page_title(page_url, display_size_str):
        # Some pages use the app's title as the page title,
        # other pages have a specific title for that page instead.
        app_title_pages = [
            "/",
            "/attribute-info"
        ]
        specific_title_pages = [
            "/attribute-correlations",
            "/attribute-distributions"
        ]

        if page_url in specific_title_pages:
            page_title = get_page_title(page_url)
        elif page_url in app_title_pages:
            # Choose the size of the app title based on the user's screen width
            screen_width = get_screen_width(display_size_str)
            page_title = get_app_title(screen_width)
        else:
            page_title = html.H1("404 - Page not found", id='page-title')

        return page_title
        
    # Update the active navlink (for both the drawer and the sidebar)
    # based on the current page's url
    @app.callback(
        Output('sidebar-navlink-/', 'active'),
        Output('sidebar-navlink-/attribute-correlations', 'active'),
        Output('sidebar-navlink-/attribute-distributions', 'active'),
        Output('sidebar-navlink-/attribute-info', 'active'),
        Output('drawer-navlink-/', 'active'),
        Output('drawer-navlink-/attribute-correlations', 'active'),
        Output('drawer-navlink-/attribute-distributions', 'active'),
        Output('drawer-navlink-/attribute-info', 'active'),
        Input('url', 'pathname'),
    )
    def update_active_navlink(page_url):
        home_active = (page_url == "/")
        correlations_active = (page_url == "/attribute-correlations")
        distributions_active = (page_url == "/attribute-distributions")
        info_active = (page_url == "/attribute-info")
        
        return 2 * (
            home_active,
            correlations_active,
            distributions_active,
            info_active
        )

    # Update the sidebar's status (expanded / collapsed / hidden)
    # based on the current page's url and the user's screen size
    @app.callback(
        Output('sidebar-navlink-/', 'styles'),
        Output('sidebar-navlink-/attribute-correlations', 'styles'),
        Output('sidebar-navlink-/attribute-distributions', 'styles'),
        Output('sidebar-navlink-/attribute-info', 'styles'),
        Output('sidebar-navlink-/', 'style'),
        Output('sidebar-navlink-/attribute-correlations', 'style'),
        Output('sidebar-navlink-/attribute-distributions', 'style'),
        Output('sidebar-navlink-/attribute-info', 'style'),
        Output('sidebar', 'style'),
        Output('dummy-sidebar', 'style'),
        Output('page-container', 'style'),
        Output('sidebar-container', 'style'),
        Output('dummy-sidebar-container', 'style'),
        Output('hamburger-menu-button-drawer-outer', 'style'),
        Input("display-size", "children"),
        Input('url', 'pathname'),
    )
    def update_sidebar_status(display_size_str, page_url):
        screen_width = get_screen_width(display_size_str)

        # Collapse / expand the sidebar depending on the user's screen width.
        # If the user is on a page with a drawer (no sidebar),
        # then this happens behind the scenes so that the sidebar
        # is the correct size when the user navigates to a page with a sidebar.
        if screen_width < 900:
            # Collapse the sidebar
            sidebar_styles = get_sidebar_style_outputs(
                is_collapsed=True,
                num_pages=num_pages
            )
            page_container_style = get_page_container_style(
                sidebar_status="collapsed"
            )
        else:
            # Expand the sidebar
            sidebar_styles = get_sidebar_style_outputs(
                is_collapsed=False,
                num_pages=num_pages
            )
            page_container_style = get_page_container_style(
                sidebar_status="expanded"
            )

        # Update the page's layout depending on the current page's url
        if page_url in sidebar_pages:
            # Display the sidebar, hide the drawer's hamburger menu
            sidebar_container_style = None
            drawer_hamburger_menu_style = {"display": "none"}
        elif page_url in drawer_pages:
            # Hide the sidebar, display the drawer's hamburger menu
            sidebar_container_style = {"display": "none"}
            drawer_hamburger_menu_style = None
            page_container_style = get_page_container_style(
                sidebar_status="hidden"
            )
        else:
            # This only happens if the user navigates to a non-existent page
            # (i.e. a 404 error)
            sidebar_container_style = {"display": "none"}
            drawer_hamburger_menu_style = {"display": "none"}
            page_container_style = get_page_container_style(
                sidebar_status="hidden"
            )

        dummy_sidebar_container_style = sidebar_container_style

        return (
            *sidebar_styles,
            page_container_style,
            sidebar_container_style,
            dummy_sidebar_container_style,
            drawer_hamburger_menu_style
        )

    # Update the drawer's status (opened / closed)
    # based on the current page's url
    # and whether the user has clicked on a hamburger menu button
    @app.callback(
        Output("drawer", "opened", allow_duplicate=True),
        Input("hamburger-menu-button-drawer-outer", "n_clicks"),
        Input("hamburger-menu-button-drawer-inner", "n_clicks"),
        Input("url", "pathname"),
        State("drawer", "opened"),
        prevent_initial_call=True
    )
    def update_drawer_status(n_outer, n_inner, page_url, is_opened):
        triggered_id = ctx.triggered_id
        
        if (
            triggered_id == "hamburger-menu-button-drawer-outer"
            or triggered_id == "hamburger-menu-button-drawer-inner"
        ):
            # A hamburger menu was clicked
            is_opened = not is_opened
        elif page_url in sidebar_pages:
            # The user has navigated to a page that uses a sidebar (no drawer)
            is_opened = False

        return is_opened

    # Keep track of the user's screen width
    app.clientside_callback(
        """(wBreakpoint, w) => {
            console.log("Width breakpoint threshold crossed.")
            return `Breakpoint name: ${wBreakpoint}, width: ${w}px`
        }""",
        Output("display-size", "children"),
        Input("breakpoints", "widthBreakpoint"),
        State("breakpoints", "width"),
    )
