import dash
from dash import html

from utils import get_introduction_block, get_window_title

dash.register_page(__name__,  title=get_window_title(__name__), path='/')

layout = html.Div(
    className='inner-page-container',
    children=[get_introduction_block()],
)
