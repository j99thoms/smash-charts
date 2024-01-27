from dash import html, Input, Output, State, ctx
from navigation import (
    get_sidebar_style_outputs,
    get_page_container_style
)
from utils import get_screen_width

def get_callbacks(app, pages, drawer_pages, sidebar_pages):

    # Update the page title based on the current page url
    @app.callback(
        Output('page-title-container', 'children'),
        Input('url', 'pathname'),
        Input('display-size', 'children')
    )
    def update_page_title(pathname, display_size_str):

        if pathname == "/":
            # Use default title
            pass
        elif pathname == "/attribute-correlations":
            return html.H1("Attribute Correlations", id='page_title')
        elif pathname == "/attribute-distributions":
            return html.H1("Attribute Distributions", id='page_title')
        elif pathname == "/attribute-info":
            # Use default title
            pass
        else:
            return html.H1("404 - Page not found", id='page-title')
        
        # Choose size for default title based on the user's screen width
        screen_width = get_screen_width(display_size_str)
        if screen_width > 1400:
            title = "Explore Super Smash Bros Characters with Interactive Visualizations!"
            return html.H1(title, id='page-title', style={"font-size": "1.7vw", "padding-top": "10px"})
        elif screen_width > 750:
            title_upper = "Explore Super Smash Bros. Characters"
            title_lower = "with Interactive Visualizations!"
            return [
                html.H1(title_upper, id='page-title-upper', style={"font-size": "24px"}),
                html.H1(title_lower, id='page-title-lower', style={"font-size": "24px", "margin-top": "-10px"})]
        elif screen_width > 650:
            title_upper = "Explore Super Smash Bros. Characters"
            title_lower = "with Interactive Visualizations!"
            return [
                html.H1(title_upper, id='page-title-upper', style={"font-size": "22px"}),
                html.H1(title_lower, id='page-title-lower', style={"font-size": "22px", "margin-top": "-10px"})]
        else:
            title_upper = "Explore Super Smash Bros. Characters"
            title_lower = "with Interactive Visualizations!"
            return [
                html.H1(title_upper, id='page-title-upper', style={"font-size": "19px"}),
                html.H1(title_lower, id='page-title-lower', style={"font-size": "19px", "margin-top": "-10px"})]

    # Update the active navlink based on the current page url
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
    def update_active_navlink(pathname):
        home_active = False
        correlations_active = False
        distributions_active = False
        info_active = False

        if pathname == "/":
            home_active = True
        elif pathname == "/attribute-correlations":
            correlations_active = True
        elif pathname == "/attribute-distributions":
            distributions_active = True
        elif pathname == "/attribute-info":
            info_active = True
        
        return 2 * (home_active, correlations_active, distributions_active, info_active)

    # Collapse / expand the sidebar based on screen size
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
        State("sidebar", "style")
    )
    def collapse_expand_sidebar(display_size_str, pathname, current_sidebar_style):
        triggered_id = ctx.triggered_id
        screen_width = get_screen_width(display_size_str)

        if pathname in sidebar_pages:
            # Collapse the sidebar for small screen widths, expand for larger screen widths
            if screen_width < 900:
                # Collapse the sidebar
                return (
                    *get_sidebar_style_outputs(is_collapsed=True, num_pages=len(pages)),
                    get_page_container_style(sidebar_status='collapsed'),
                    None, None, {"display": "none"}
                )
            else:
                # Expand the sidebar
                return (
                    *get_sidebar_style_outputs(is_collapsed=False, num_pages=len(pages)),
                    get_page_container_style(sidebar_status='expanded'),
                    None, None, {"display": "none"}
                )
        elif pathname in drawer_pages:
            # User is on a page in which the sidebar is hidden
            if screen_width < 900:
                # sidebar is currently collapsed, leave it collapsed behind the scenes
                return (
                    *get_sidebar_style_outputs(is_collapsed=True, num_pages=len(pages)),
                    get_page_container_style(sidebar_status='hidden'),
                    {"display": "none"}, {"display": "none"}, None
                )
            else:
                # sidebar is currently expanded, leave it expanded behind the scenes
                return (
                    *get_sidebar_style_outputs(is_collapsed=False, num_pages=len(pages)),
                    get_page_container_style(sidebar_status='hidden'),
                    {"display": "none"}, {"display": "none"}, None
                )
        else:
            # This should never happen.
            print("Error updating sidebar.")
            print(f"display-size: {display_size_str}")
            print(f"pathname: {pathname}")
            print(f"current_sidebar_style: {current_sidebar_style}")
            print(f"triggered_id: {triggered_id}")

    # Open the drawer
    @app.callback(
        Output("drawer", "opened", allow_duplicate=True),
        Input("hamburger-menu-button-drawer-outer", "n_clicks"),
        prevent_initial_call=True
    )
    def open_drawer(n_clicks):
        return True

    # Close the drawer
    @app.callback(
        Output("drawer", "opened", allow_duplicate=True),
        Input("hamburger-menu-button-drawer-inner", "n_clicks"),
        prevent_initial_call=True
    )
    def close_drawer(n_clicks):
        return False

    # Hide the drawer when the user navigates to a page that uses a side sidebar
    @app.callback(
        Output("drawer", "opened", allow_duplicate=True),
        Input("url", "pathname"),
        State("drawer", "opened"),
        prevent_initial_call=True
    )
    def hide_drawer(pathname, opened):
        if pathname in sidebar_pages:
            return False
        else:
            return opened

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
