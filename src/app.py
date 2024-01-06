from dash import Dash, html, Input, Output, dcc
import dash
from utils import Footer, get_logo
import dash_bootstrap_components as dbc
import dash_mantine_components as dmc

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
nav = dbc.Nav(
    [
        dbc.NavItem(dbc.NavLink(page['name'].title(), active="exact", href=page['relative_path']))
        for page in pages
    ],
    pills=True
)


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
                    html.Div(children=[html.H1(html.Br(), id='page-title')],id='page-title-container')
                ]
            ),
            dbc.Row([nav]),
            html.Div(
                id='wrapper-outer',
                children=[
                    html.Div(
                        id='wrapper-inner',
                        children=[
                            html.Div(
                                id='app-container',
                                children=[dash.page_container]
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

if __name__ == '__main__':
    app.run(debug=True)
