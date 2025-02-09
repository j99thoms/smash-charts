import math
import re
from itertools import product

import pandas as pd
from dash import dcc, html
from dash_iconify import DashIconify

IMG_DIR = "assets/img"
TXT_DIR = "assets/txt"
DATA_DIR = "../data/clean"

def get_icon(icon, height=16):
    return DashIconify(icon=icon, height=height)

def get_logo():
    logo = html.A(
        className='logo',
        children=[html.Img(src=f'{IMG_DIR}/logo-small.png')],
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

def get_attribute_selector_dropdown(div_id, default_value, data_type="all", game="ultimate"):
    dropdown_options = get_dropdown_options(data_type=data_type, game=game)
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
                "Explore Super Smash Bros Fighters "
                "with Interactive Visualizations!"
            )
            app_title = html.H1(
                title_text,
                id='page-title',
                style={"font-size": "1.7vw", "padding-top": "10px"}
            )
    else:
        # App title is split across two lines
        title_text_upper = "Explore Super Smash Bros. Fighters"
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

def get_fighter_attributes_df(data_type="all", game="ultimate", excluded_fighter_ids=None):
    fighter_attributes_df = pd.read_csv(f"{DATA_DIR}/{game}_fighter_params.csv")

    fighter_attributes_df = fighter_attributes_df.iloc[:-1] # rm Giga Bowser

    ordinal_columns = ["number_of_jumps", "jump_frames"]

    data_type = data_type.lower()
    if data_type == "continuous":
        fighter_attributes_df = fighter_attributes_df.drop(
            columns=(ordinal_columns), errors='ignore'
        )
    elif data_type == "all":
        pass
    else:
        raise ValueError("data_type should be either 'continuous' or 'all'.")

    fighter_attributes_df = append_row_col_for_fighter_selector(fighter_attributes_df)

    fighter_attributes_df['img_url'] = (
        IMG_DIR + "/heads/"
        + fighter_attributes_df['fighter_number'] + "_"
        + fighter_attributes_df['fighter'].\
            str.lower().\
            str.replace(" ", "_", regex=False).\
            str.replace("&", "and", regex=False).\
            str.replace("\.|\(|\)", "", regex=True)
        + ".png"
    )

    if excluded_fighter_ids is not None:
       fighter_attributes_df = fighter_attributes_df.loc[
           ~fighter_attributes_df.index.isin(excluded_fighter_ids)
        ]

    return fighter_attributes_df

def get_correlations_df():
    fighter_attributes_df = get_fighter_attributes_df(
        data_type="continuous"
    ).drop(columns=['row_number', 'col_number'])

    column_names = fighter_attributes_df.columns.tolist()
    formatted_names = [
        format_attribute_name(column_name) for column_name in column_names
    ]
    fighter_attributes_df = fighter_attributes_df.rename(
        columns=dict(zip(column_names, formatted_names))
    )

    corr_df = fighter_attributes_df.corr(numeric_only=True, method='pearson')
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

def get_dropdown_options(data_type, game):
    fighter_attributes_df = get_fighter_attributes_df(data_type=data_type, game=game)

    # The first 2 columns are 'fighter_number' and 'fighter'.
    # The last 3 columns are 'img_url', 'row_number', and 'col_number'.
    attribute_columns = fighter_attributes_df.columns.to_series().iloc[2:-3]
    attribute_names = [
        format_attribute_name(column_name) for column_name in attribute_columns
    ]

    dropdown_options = [
        {'value': column, 'label': name}
        for column, name in zip(attribute_columns, attribute_names)
    ]
    
    return dropdown_options

def format_attribute_name(column_name):
    return column_name.replace("_", " ").title()

def append_row_col_for_fighter_selector(fighter_df):
    fighter_df = fighter_df.sort_values(by="fighter_number", ignore_index=True)

    # Calculate number of rows and columns needed for a square grid
    n_fighters = len(fighter_df)
    n_rows = math.ceil(math.sqrt(n_fighters))
    n_cols  = math.ceil(n_fighters / n_rows)

    # Generate row-column pairs and add them as new columns
    row_cols = [*product(range(n_rows), range(n_cols))][:n_fighters]
    fighter_df['row_number'], fighter_df['col_number'] = zip(*row_cols)

    return fighter_df

def get_excluded_char_ids(excluded_char_ids_mem):
    if excluded_char_ids_mem is None:
        return []

    ids = excluded_char_ids_mem['ids']
    return [] if ids is None else ids

def convert_excluded_char_ids(excluded_fighter_numbers, selected_game):
    excluded_fighter_numbers_df = pd.DataFrame(excluded_fighter_numbers)
    fighter_df = get_fighter_attributes_df(game=selected_game)[['fighter_number']]

    excluded_mask = excluded_fighter_numbers_df['excluded']
    excluded_numbers = excluded_fighter_numbers_df.loc[excluded_mask, 'fighter_number']

    fighter_df['excluded'] = fighter_df['fighter_number'].isin(excluded_numbers)
    excluded_ids = fighter_df[fighter_df['excluded']].index.tolist()

    return excluded_ids

def update_excluded_fighter_numbers(cur_excluded_fighters, ids, selected_game):
    cur_excluded_fighters_df = pd.DataFrame(cur_excluded_fighters)
    fighter_df = get_fighter_attributes_df(game=selected_game)[['fighter_number']]

    fighter_df['excluded_in_selected'] = fighter_df.index.isin(ids)

    excluded_fighters_df = pd.merge(
        cur_excluded_fighters_df, fighter_df, how='left', on='fighter_number'
    )
    excluded_fighters_df['excluded'] = excluded_fighters_df['excluded_in_selected'].\
        fillna(excluded_fighters_df['excluded'])

    return excluded_fighters_df[['fighter_number', 'excluded']].to_dict()

def initialize_excluded_fighters():
    df = pd.DataFrame({
        'fighter_number': ["01", "02", "03", "04", "04E", "05", "06", "07", "08",
                           "09", "10", "11", "12", "13", "13E", "14", "15", "15B",
                           "16", "17", "18", "19", "20", "21", "21E", "22", "23",
                           "24", "25", "25E", "26", "27", "28", "28E", "29", "30",
                           "31", "32", "33", "34", "35", "36", "37", "38", "39",
                           "40", "41", "42", "43", "44", "45", "46", "47", "48",
                           "49", "50", "51", "52", "53", "54", "55", "56", "57",
                           "58", "59", "60", "60E", "61", "62", "63", "64", "65",
                           "66", "66E", "67", "68", "69", "70", "71", "72", "73",
                           "74", "75", "76", "77", "78", "79", "80", "81", "82"]
    })
    df['excluded'] = False # All fighters are initially included

    return df.to_dict()

def make_dash_table(df):
    """ Return a dash definition of an HTML table for a Pandas dataframe """
    table = []
    for index, row in df.iterrows():
        html_row = []
        for i in range(len(row)):
            html_row.append(html.Td([row[i]]))
        table.append(html.Tr(html_row))
        
    return table

def get_window_title(page_name):
    page_title =  page_name.replace("pages.", "").replace("_", " ").title()

    if page_title == "Home":
        return "Smash Charts"
    else:
        return page_title + " | Smash Charts"
