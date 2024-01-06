import dash
import dash_bootstrap_components as dbc
from dash import html
from utils import get_attribute_info_block

dash.register_page(__name__)

layout = html.Div(
    className="page-container",
    children=[
        dbc.Row([
            # Attribute info
            get_attribute_info_block(),
        ]),
    ]
)
