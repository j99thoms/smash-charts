from dash import html
import dash_bootstrap_components as dbc
import pandas as pd
import re

def Footer():
    return html.Div(
        id="footer",
        children=[get_credits()]
)

def get_logo():
    logo = html.A(
        children=[html.Img(src='assets/logo.png')],
        className='logo',
        href="/",
        target="_self",
    )
    return logo

def get_credits():
    credits = html.Div(
        [
            html.A(
                "Smash Charts", 
                href="https://github.com/J99thoms/Super-Smash-Dashboard",
                target="_blank",
                style={"color": "white"}
            ), 
            " was created by ",
            html.A(
                "Jakob Thoms", 
                href="https://github.com/J99thoms", 
                target="_blank",
                style={"color": "white"}
            ),
            "."
        ], 
        style={"text-align": "right", "padding-right": "10px", "padding-left": "10px", "font-size": "83%"}
    )
    
    return credits


def get_attribute_info_block():
    attribute_info_paragraphs = get_attribute_info()

    smash_wiki_credits = "These attribute descriptions are based on the descriptions which can be found on "
    smash_wiki_hyperlink = html.A(
                                "SmashWiki", 
                                href="https://www.ssbwiki.com/",
                                target="_blank"
                            )

    attr_info = dbc.Col([
        html.Div(
            id="attribute-info-block",
            children=[
                html.Div([
                    html.Div([
                        html.H4(
                            [html.U("Attribute Info")], 
                            style={"text-align": "center"}
                        ),
                        *attribute_info_paragraphs,
                        html.Div([
                            smash_wiki_credits,
                            smash_wiki_hyperlink,
                            "."
                        ], style={"margin-top": "30px", "font-size": "85%"})
                    ],
                    style={"width": "98%", "float": "right"}),
                ],
                style={"width": "98%", "float": "left", "margin-top": "10px"}),
            ],
        )
    ])
    
    return attr_info

def get_introduction_block():
    introduction_paragraphs = get_introduction()

    intro_block = html.Div(
        id="introduction-container",
        children=[
            html.Div(
                children=[
                    html.Div(
                        children=introduction_paragraphs,
                        style={"width": "98%", "height": "100%", "float": "right"}
                    )
                ],
                style={"width": "98%", "height": "100%", "float": "left", "margin-top": "10px"}
            )
        ]
    )

    return intro_block

def get_attribute_info():
    with open("assets/attribute_info.txt", "r") as text:
        lines = text.readlines()

    paragraphs = []
    p_children = []

    for line in lines:
        if line.endswith("\n"):
            if line.find("\n") != 0:
                for segment in parse_bolds(line[:-1]):
                    p_children.append(segment)
            else:
                paragraphs.append(
                    html.P(
                        children=p_children, 
                        className="attribute-info-paragraph"
                    )
                )
                p_children = []
        else:
            for segment in parse_bolds(line):
                p_children.append(segment)

    if len(p_children) > 0:
        paragraphs.append(
            html.P(
                children=p_children, 
                className="attribute-info-paragraph"
            )
        )

    return paragraphs

def get_introduction():
    with open("assets/introduction.txt", "r") as text:
        lines = text.readlines()

    paragraphs = []
    p_children = []

    for line in lines:
        if line.endswith("\n"):
            if line.find("\n") != 0:
                for segment in parse_bolds(line[:-1]):
                    p_children.append(segment)
            else:
                paragraphs.append(
                    html.P(
                        children=p_children,
                        className="introduction-paragraph"
                    )
                )
                p_children = []
        else:
            for segment in parse_bolds(line):
                p_children.append(segment)

    if len(p_children) > 0:
        paragraphs.append(
            html.P(
                children=p_children,
                className="introduction-paragraph"
            )
        )

    return paragraphs

def parse_bolds(line):
    # Regex pattern to match text surrounded by '**'
    bold_pattern = r'(\*\*.*\*\*)'
    
    if re.search(bold_pattern, line):
        first_delim = line.find("**")
        second_delim = line[first_delim + 2:].find("**") + first_delim + 2
        if first_delim > 0:
            parsed_line = [line[:first_delim]] + [html.B(line[first_delim + 2:second_delim])] + parse_bolds(line[second_delim + 2:])
        else:
            parsed_line = [html.B(line[first_delim + 2:second_delim])] + parse_bolds(line[second_delim + 2:])
    else:
        parsed_line = [line]

    return parsed_line

def get_character_data():
    character_attributes_df = pd.read_csv("../data/character_data.csv").drop(
        columns=['percent_incr_fall_speed']  # Unused column
    )

    return character_attributes_df

def get_dropdown_options():
    character_attributes_df = get_character_data()

    # The first column is 'character', the last column is 'img_url'
    attribute_names = character_attributes_df.columns.to_series().iloc[1:-1]

    dropdown_options = [
        {'value': attribute_name, 'label': attribute_name}
        for attribute_name in attribute_names
    ]
    
    return dropdown_options

def make_dash_table(df):
    """ Return a dash definition of an HTML table for a Pandas dataframe """
    table = []
    for index, row in df.iterrows():
        html_row = []
        for i in range(len(row)):
            html_row.append(html.Td([row[i]]))
        table.append(html.Tr(html_row))
        
    return table

