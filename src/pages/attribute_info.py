import dash
from dash import html
from utils import get_attribute_info_block

dash.register_page(__name__)

layout = html.Div(
    className="page-container",
    children=[get_attribute_info_block()]
)
