from dash import html, Input, Output, State, ctx
from dash.exceptions import PreventUpdate
from datetime import datetime, timedelta
from utils import get_screen_width, get_page_title, get_app_title, get_excluded_char_ids
from navigation import (
    get_sidebar_style_outputs,
    get_page_container_style
)
from plots import get_character_selector_chart

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
            drawer_hamburger_menu_style = {"visibility": "hidden"}
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
    def update_navigation_drawer_status(n_outer, n_inner, page_url, is_opened):
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

    # Update the settings menu's status (opened / closed)
    # based on the current page's url
    # and whether the user has clicked on the settings menu button
    @app.callback(
        Output("settings-menu-drawer", "opened", allow_duplicate=True),
        Output("settings-menu-button", "style", allow_duplicate=True),
        Input("settings-menu-button", "n_clicks"),
        Input("url", "pathname"),
        State("settings-menu-button", "opened"),
        prevent_initial_call=True
    )
    def update_settings_drawer_status(n_clicks, page_url, is_opened):
        triggered_id = ctx.triggered_id
        button_style = None

        if triggered_id == "settings-menu-button":
            # Menu button was clicked
            is_opened = not is_opened
        elif page_url in sidebar_pages:
            # The user has navigated to a page that does not display the
            # settings menu
            is_opened = False
            button_style = {"display": "none"}

        return is_opened, button_style

    # Record the last time the user pressed the settings menu button
    @app.callback(
        Output("settings-btn-last-press", "data"),
        Input("settings-menu-button", "n_clicks"),
        prevent_initial_call=True
    )
    def record_settings_btn_last_press(n_clicks):
      return {'time': datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

    # Update character selector chart
    @app.callback(
        Output("character-selector-chart", "spec"),
        Input("settings-menu-drawer", "opened"),
        State("excluded-char-ids-mem", "data")
    )
    def update_character_selector_chart(is_opened, excluded_char_ids_mem):
        excluded_char_ids = get_excluded_char_ids(excluded_char_ids_mem)
        return get_character_selector_chart(excluded_char_ids).to_dict()

    # Update excluded characters
    @app.callback(
        Output("char-selector-mem", "data"),
        Output("excluded-char-ids-mem", "data"),
        Input("character-selector-chart", "signalData"),
        State("char-selector-mem", "data"),
        State("excluded-char-ids-mem", "data"),
        State("settings-btn-last-press", "data"),
        prevent_initial_call=True
    )
    def update_selected_characters(
        selector_signal, selector_mem, 
        excluded_char_ids_mem, settings_btn_last_press
    ):
        selector_dict = selector_signal['character_selector']

        if '_vgsid_' in selector_dict:
            selected_char_ids_string = selector_dict['_vgsid_'].strip("Set()")
        else:
            selected_char_ids_string = ""

        # See https://github.com/j99thoms/smash-charts/issues/18:
        if settings_btn_last_press is not None and (
            selected_char_ids_string == "999" or selected_char_ids_string == ""
        ):
            last_press_time = settings_btn_last_press['time']
            last_press_time = datetime.strptime(last_press_time, '%Y-%m-%d %H:%M:%S')
            delta = timedelta(seconds = 1.25)
            if last_press_time <= datetime.now() <= (last_press_time + delta):
                return {'selected': []}, excluded_char_ids_mem

        # Get character ids currently selected in the chart's selection_point:
        if not selected_char_ids_string:
            selected_char_ids = []
        else:
            ids = selected_char_ids_string.split(',')
            selected_char_ids = [int(id) - 1 for id in ids] # Altair off-by-one
            if 998 in selected_char_ids:
                selected_char_ids.remove(998)

        # Get character ids previously selected in the chart's selection_point:
        if not selector_mem:
            prev_selected_char_ids = []
        else:
            prev_selected_char_ids = selector_mem['selected']

        # All changes between new/old selections:
        diff = list(set(selected_char_ids) ^ set(prev_selected_char_ids))
        if (len(diff) != 1):
            # Should not have > 1 change except if chart was reset,
            # which is already dealt with above
            return selector_mem, excluded_char_ids_mem
        else:
            pressed_id = diff[0]

        excluded_char_ids = get_excluded_char_ids(excluded_char_ids_mem)
        if (pressed_id in excluded_char_ids):
            excluded_char_ids.remove(pressed_id)
        else:
            excluded_char_ids.append(pressed_id)

        return {'selected': selected_char_ids}, {'ids': excluded_char_ids}

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
