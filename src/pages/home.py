import dash
from dash import html
from utils import get_introduction_block

dash.register_page(__name__, path='/')

layout = html.Div(
    className="inner-page-container",
    children=[get_introduction_block()]
)
