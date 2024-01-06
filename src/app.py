from dash import Dash, html, Input, Output, State, dcc
import dash
import dash_bootstrap_components as dbc
import dash_mantine_components as dmc
from utils import Footer, get_logo
from navigation import (
    get_hamburger_menu,
    get_navbar,
    get_drawer,
    get_navbar_style_outputs,
    get_app_container_style,
    NAVBAR_WIDTH
)

google_fonts = "https://fonts.googleapis.com/css2"
google_fonts += "?family=Inter:wght@100;200;300;400;500;900&display=swap"

# Setup the dash app
app = Dash(
    __name__,
    use_pages=True,
    external_stylesheets=[
        dbc.themes.MATERIA,
        google_fonts # include google fonts
    ],
    suppress_callback_exceptions=True
)
server = app.server
app.title = "Smash Charts"

logo=get_logo()

pages = [*dash.page_registry.values()]

drawer_pages = [
    "/attribute-correlations",
    "/attribute-distributions"
]
navbar_pages = [
    page['relative_path'] for page in pages if page['relative_path'] not in drawer_pages
]

hamburger_menu_drawer_outer = get_hamburger_menu(
    div_id="hamburger-menu-button-drawer-outer",
    initial_load=True
)
hamburger_menu_navbar = get_hamburger_menu(
    div_id="hamburger-menu-button-navbar",
    initial_load=True
)

navbar = get_navbar(pages)
drawer = get_drawer(pages)



app.layout = dmc.MantineProvider(
    theme={
        "fontFamily": "'Inter', sans-serif",
        "primaryColor": "indigo",
        "components": {
            "Button": {"styles": {"root": {"fontWeight": 400}}},
            "Alert": {"styles": {"title": {"fontWeight": 500}}},
            "AvatarGroup": {"styles": {"truncated": {"fontWeight": 500}}},
        },
    },
    inherit=True,
    withGlobalStyles=True,
    withNormalizeCSS=True,
    children=[
        html.Div([
            # Original image is 21752 x 4029
            # html.Div(
            #     id="header-image",
            #     children=[
            #         html.Img(src="assets/everyone_is_here_compressed.png")
            #     ]
            # ),
             html.Div(
                id='header',
                children=[
                    logo,
                    hamburger_menu_drawer_outer, 
                    # hamburger_menu_navbar, 
                    html.Div(children=[html.H1(html.Br(), id='page-title')],id='page-title-container')
                ]
            ),
            drawer,
            navbar,
            html.Div(
                id='wrapper-outer',
                children=[
                    html.Div(
                        id='wrapper-inner',
                        children=[
                            html.Div(
                                id='dummy-navbar-container',
                                children=html.Div(
                                    id='dummy-navbar',
                                )
                            ),
                            html.Div(
                                id='app-container',
                                children=[dash.page_container],
                                style={'display': 'none'} # Just for the initial load
                            ),
                        ],
                    )
                ],
            ),
            Footer(),
            dcc.Location(id='url'),
        ], id='user-window')
    ],
)


# Update the page title based on the current page url
@app.callback(
    Output('page-title-container', 'children'),
    Input('url', 'pathname')
)
def update_page_title(pathname):

    if pathname == "/":
        title = "Explore Super Smash Bros Characters with Interactive Visualizations!"
        return html.H1(title, id='page-title', style={"font-size": "1.7vw", "padding-top": "10px"})
    elif pathname == "/attribute-correlations":
        return html.H1("Attribute Correlations", id='page_title')
    elif pathname == "/attribute-distributions":
        return html.H1("Attribute Distributions", id='page_title')
    elif pathname == "/attribute-info":
        title = "Explore Super Smash Bros Characters with Interactive Visualizations!"
        return html.H1(title, id='page-title', style={"font-size": "1.7vw", "padding-top": "10px"})
    else:
        return html.H1("404 - Page not found", id='page-title')
    

# Update the active navlink based on the current page url
@app.callback(
    Output('navbar-navlink-/', 'active'),
    Output('navbar-navlink-/attribute-correlations', 'active'),
    Output('navbar-navlink-/attribute-distributions', 'active'),
    Output('navbar-navlink-/attribute-info', 'active'),
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

# Collapse / expand the navbar when the hamburger menu button is clicked
@app.callback(
    Output('navbar-navlink-/', 'styles'),
    Output('navbar-navlink-/attribute-correlations', 'styles'),
    Output('navbar-navlink-/attribute-distributions', 'styles'),
    Output('navbar-navlink-/attribute-info', 'styles'),
    Output('navbar-navlink-/', 'style'),
    Output('navbar-navlink-/attribute-correlations', 'style'),
    Output('navbar-navlink-/attribute-distributions', 'style'),
    Output('navbar-navlink-/attribute-info', 'style'),
    Output('navbar', 'style'),
    Output('dummy-navbar', 'style'),
    Output('app-container', 'style'),
    Output('navbar-container', 'style'),
    Output('dummy-navbar-container', 'style'),
    # Output('hamburger-menu-button-navbar', 'style'),
    Output('hamburger-menu-button-drawer-outer', 'style'),
    Input('url', 'pathname')
)
def collapse_expand_navbar(pathname):

    if pathname in navbar_pages:
       return (
            *get_navbar_style_outputs(num_pages=len(pages)),
            get_app_container_style(navbar_status='shown'),
            None, None, {"display": "none"}
        )
    elif pathname in drawer_pages:
        return (
            *get_navbar_style_outputs(num_pages=len(pages)),
            get_app_container_style(navbar_status='hidden'),
            {"display": "none"}, {"display": "none"}, None
        )
    else:
        # This should never happen.
        print("Error updating navbar.")
        print(f"pathname: {pathname}")


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

# Hide the drawer when the user navigates to a page that uses a side navbar
@app.callback(
    Output("drawer", "opened", allow_duplicate=True),
    Input("url", "pathname"),
    State("drawer", "opened"),
    prevent_initial_call=True
)
def hide_drawer(pathname, opened):
    if pathname in navbar_pages:
        return False
    else:
        return opened

if __name__ == '__main__':
    app.run(debug=True)
