import re
import pandas as pd
from dash import html, dcc
from dash_iconify import DashIconify

IMG_DIR = "assets/img"
TXT_DIR = "assets/txt"
DATA_DIR = "../data"

def get_icon(icon, height=16):
    return DashIconify(icon=icon, height=height)

def get_logo():
    logo = html.A(
        className='logo',
        children=[html.Img(src=f'{IMG_DIR}/logo.png')],
        href="/",
        target="_self"
    )

    return logo

def create_text_block(children):
    text_block = html.Div(
        className="text-block",
        children=[
            html.Div(
                children=[
                    html.Div(
                        children=children,
                        style={
                            "width": "98%",
                            "float": "right"
                        }
                    )
                ],
                style={
                    "width": "98%",
                    "float": "left",
                    "margin-top": "10px"
                }
            )
        ]
    )

    return text_block    

def get_attribute_info_block():
    attribute_info_header = html.H4(
        children=[html.U("Attribute Info")],
        style={"text-align": "center"}
    )
    attribute_info_paragraphs = get_attribute_info_paragraphs()
    smash_wiki_credits = get_smash_wiki_credits()

    attribute_info_block = create_text_block(
        children=[
            attribute_info_header,
            *attribute_info_paragraphs,
            smash_wiki_credits
        ]
    )
    
    return attribute_info_block

def get_introduction_block():
    introduction_paragraphs = get_introduction_paragraphs()

    introduction_block = create_text_block(
        children=introduction_paragraphs
    )

    return introduction_block

def get_attribute_info_paragraphs():
    with open(f"{TXT_DIR}/attribute_info.txt", "r") as text:
        attribute_info_txt = text.readlines()

    attribute_info_paragraphs = parse_paragraphs(
        lines=attribute_info_txt,
        paragraph_class_name="attribute-info-paragraph"
    )

    return attribute_info_paragraphs

def get_introduction_paragraphs():
    with open(f"{TXT_DIR}/introduction.txt", "r") as text:
        introduction_txt = text.readlines()

    introduction_paragraphs = parse_paragraphs(
        lines=introduction_txt,
        paragraph_class_name="introduction-paragraph"
    )

    return introduction_paragraphs

def get_smash_wiki_credits():
    smash_wiki_hyperlink = html.A(
        children="SmashWiki",
        href="https://www.ssbwiki.com/",
        target="_blank"
    )
    smash_wiki_credits = html.Div(
        children=[
            "These attribute descriptions are based on ",
            "the descriptions which can be found on ",
            smash_wiki_hyperlink,
            "."
        ],
        style={
            "margin-top": "30px",
            "font-size": "85%"
        }
    )
    
    return smash_wiki_credits

def get_attribute_selector_dropdown(div_id, default_value, data_type):
    dropdown_options = get_dropdown_options(data_type=data_type)
    attribute_selector_dropdown = dcc.Dropdown(
        id=div_id,
        options=dropdown_options,
        value=default_value
    )
   
    return attribute_selector_dropdown

def get_vertical_spacer(height):
    vertical_spacer = html.Div(style={"height": f"{height}px"})

    return vertical_spacer

def parse_paragraphs(lines, paragraph_class_name):
    paragraphs = []
    p_children = []

    for line in lines:
        if line != "\n":
            if line.endswith("\n"):
                line = line[:-1]
            for segment in parse_bolds(line):
                p_children.append(segment)
        else:
            # Current line is "\n", so end the paragraph and start a new one
            paragraphs.append(
                html.P(
                    className=paragraph_class_name,
                    children=p_children
                )
            )
            p_children = []

    if len(p_children) > 0:
        # This only happens if there is no newline at the end of the txt file
        paragraphs.append(
            html.P(
                className=paragraph_class_name,
                children=p_children
            )
        )

    return paragraphs

def parse_bolds(line):
    # Regex pattern to match text surrounded by '**'
    bold_pattern = r'(\*\*.*\*\*)'
    
    if not re.search(bold_pattern, line):
        # There are no bold segments in the line,
        # so the line has only one segment (the whole line)
        line_segments = [line]
    else:
        # There is at least one bold segment in the line
        line_segments = []

        # Find the locations of the start and end of the first bold segment
        first_delim = line.find("**")
        second_delim = line[first_delim + 2:].find("**") + first_delim + 2

        if first_delim > 0:
            line_segments.append(line[:first_delim])
            
        line_segments.append(html.B(line[first_delim + 2:second_delim]))

        for segment in parse_bolds(line[second_delim + 2:]):
            line_segments.append(segment)

    return line_segments

def get_page_title(page_url):
    title_text = page_url.strip("/").replace("-", " ").title()
    page_title = html.H1(title_text, id='page_title')

    return page_title

def get_app_title(screen_width):
    if screen_width > 1400:
            # App title is all on one line
            title_text = (
                "Explore Super Smash Bros Characters "
                "with Interactive Visualizations!"
            )
            app_title = html.H1(
                title_text,
                id='page-title',
                style={"font-size": "1.7vw", "padding-top": "10px"}
            )
    else:
        # App title is split across two lines
        title_text_upper = "Explore Super Smash Bros. Characters"
        title_text_lower = "with Interactive Visualizations!"
        if screen_width > 750:
            font_size = 24
        elif screen_width > 650:
            font_size = 22
        else:
            font_size = 19

        app_title = [
            html.H1(title_text_upper,
                    id='page-title-upper',
                    style={"font-size": f"{font_size}px"}
            ),
            html.H1(title_text_lower,
                    id='page-title-lower',
                    style={"font-size": f"{font_size}px", "margin-top": "-10px"}
                )
            ]

    return app_title

def get_screen_width(display_size_str):
    # display_size_str looks like "Breakpoint name: <=1500px, width: 1440px"
    screen_width = display_size_str.split(" ")[4] # Looks like "1440px"
    screen_width = int(screen_width.strip("px"))

    return screen_width

def get_character_attributes_df(data_type="all"):
    character_attributes_df = pd.read_csv(f"{DATA_DIR}/character_data.csv")

    # Drop non-playable characters
    non_playable_characters = [
        "Giga Bowser", "Mob Smash Mii Enemy (Brawler)",
        "Mob Smash Mii Enemy (Swordfighter)", "Mob Smash Mii Enemy (Gunner)"
    ]
    character_attributes_df = character_attributes_df[
        ~character_attributes_df['Character'].isin(non_playable_characters)
    ]

    boolean_columns = [
        "Has Walljump", "Has Crawl", "Has Wallcling", "Has Zair"
    ]
    ordinal_columns = ["Number of Jumps"]

    data_type = data_type.lower()
    if data_type == "continuous":
        character_attributes_df = character_attributes_df.drop(
            columns=(boolean_columns + ordinal_columns)
        )
    elif data_type == "quantitative":
        character_attributes_df = character_attributes_df.drop(
            columns=boolean_columns
        )
    elif data_type == "all":
        pass
    else:
        raise ValueError("data_type should be one of 'continuous', 'quantitative', or 'all'.")

    return character_attributes_df

def get_correlations_df():
    # TODO: Pre-compute correlations (save in file and load when needed)
    character_attributes_df = get_character_attributes_df(data_type="continuous")

    corr_df = character_attributes_df.corr(numeric_only=True, method='pearson')
    corr_df = corr_df.reset_index().melt(id_vars='index').rename(
        columns={
            'index': 'Attribute 1',
            'variable': 'Attribute 2',
            'value': 'Correlation'
        }
    )
    
    corr_df['Correlation'] = corr_df['Correlation'].round(4)
    corr_df['corr_2dec'] = corr_df['Correlation'].round(2)
    corr_df['corr_1dec'] = corr_df['Correlation'].round(1)
    corr_df['abs_corr'] = corr_df['Correlation'].abs()

    return corr_df

def get_dropdown_options(data_type):
    character_attributes_df = get_character_attributes_df(data_type=data_type)

    # The first column is 'Character #', the 2nd column is 'Character', 
    # and the last column is 'img_url'
    attribute_names = character_attributes_df.columns.to_series().iloc[2:-1]

    dropdown_options = [
        {
            'value': attribute_name,
            'label': attribute_name
        }
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
