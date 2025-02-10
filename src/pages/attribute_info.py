import dash
from dash import html

from utils import get_attribute_info_block, get_window_title

dash.register_page(__name__, title=get_window_title(__name__))

layout = html.Div(
    className='inner-page-container',
    children=[get_attribute_info_block()],
)
