import dash
import dash_breakpoints
import dash_mantine_components as dmc
from dash import Dash, dcc, html
from dash_bootstrap_components import themes

from callbacks import get_callbacks
from layout import get_app_html

GOOGLE_FONTS = (
    "https://fonts.googleapis.com/css2"
    "?family=Inter:wght@100;200;300;400;500;900&display=swap"
)

# Setup the dash app
app = Dash(
    __name__,
    use_pages=True,
    external_stylesheets=[
        themes.MATERIA,
        GOOGLE_FONTS, # Include google fonts
    ],
    suppress_callback_exceptions=True,
     update_title=None,
)
app.title = "Smash Charts"
server = app.server

# Specify which pages should use a drawer (instead of a sidebar)
# All pages which don't use a drawer will use a sidebar
pages = [*dash.page_registry.values()]
drawer_pages = [
    "/attribute-correlations",
    "/attribute-distributions",
]
sidebar_pages = [
    page['relative_path']
    for page in pages
    if page['relative_path'] not in drawer_pages
]

# Window size breakpoints - used for dynamic layout updates based on screen size
window_size_breakpoints = dash_breakpoints.WindowBreakpoints(
    id="breakpoints",
    widthBreakpointThresholdsPx=[*range(400, 1800, 50)],
)

app_html = get_app_html(pages, dash.page_container)
app_html += [
    dcc.Location(id='url'),
    html.Div(id="display-size"),
    window_size_breakpoints,
]

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
    children=app_html,
)

get_callbacks(
    app=app,
    num_pages=len(pages),
    drawer_pages=drawer_pages,
    sidebar_pages=sidebar_pages,
)

if __name__ == '__main__':
    app.run(debug=True)
