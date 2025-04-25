import math
import re
from itertools import product

import pandas as pd
from dash import dcc, html
from dash_iconify import DashIconify

IMG_DIR = 'assets/img'
TXT_DIR = 'assets/txt'
DATA_DIR = '../data/clean'


def get_icon(icon, height=16):
    return DashIconify(icon=icon, height=height)


def get_logo():
    return html.A(
        className='logo',
        children=[html.Img(src=f'{IMG_DIR}/logo-small.png')],
        href='/',
        target='_self',
    )


def create_text_block(children):
    return html.Div(
        className='text-block',
        children=[
            html.Div(
                children=[
                    html.Div(
                        children=children,
                        style={
                            'width': '98%',
                            'float': 'right',
                        },
                    ),
                ],
                style={
                    'width': '98%',
                    'float': 'left',
                    'margin-top': '10px',
                },
            ),
        ],
    )


def get_attribute_info_block():
    attribute_info_header = html.H4(
        children=[html.U('Attribute Info')],
        style={'text-align': 'center'},
    )
    attribute_info_paragraphs = get_attribute_info_paragraphs()
    smash_wiki_credits = get_smash_wiki_credits()

    return create_text_block(
        children=[
            attribute_info_header,
            *attribute_info_paragraphs,
            smash_wiki_credits,
        ],
    )


def get_introduction_block():
    introduction_paragraphs = get_introduction_paragraphs()

    return create_text_block(children=introduction_paragraphs)


def get_attribute_info_paragraphs():
    with open(f'{TXT_DIR}/attribute_info.txt') as text:
        attribute_info_txt = text.readlines()

    return parse_paragraphs(
        lines=attribute_info_txt,
        paragraph_class_name='attribute-info-paragraph',
    )


def get_introduction_paragraphs():
    with open(f'{TXT_DIR}/introduction.txt') as text:
        introduction_txt = text.readlines()

    return parse_paragraphs(
        lines=introduction_txt,
        paragraph_class_name='introduction-paragraph',
    )


def get_smash_wiki_credits():
    smash_wiki_hyperlink = html.A(
        children='SmashWiki',
        href='https://www.ssbwiki.com/',
        target='_blank',
    )

    return html.Div(
        children=[
            'These attribute descriptions are based on ',
            'the descriptions which can be found on ',
            smash_wiki_hyperlink,
            '.',
        ],
        style={
            'margin-top': '30px',
            'font-size': '85%',
        },
    )


def get_attribute_selector_dropdown(
    div_id,
    default_value,
    data_type='all',
    game='ultimate',
):
    dropdown_options = get_dropdown_options(data_type=data_type, game=game)

    return dcc.Dropdown(
        id=div_id,
        options=dropdown_options,
        value=default_value,
    )


def get_vertical_spacer(height):
    return html.Div(style={'height': f'{height}px'})


def parse_paragraphs(lines, paragraph_class_name):
    paragraphs = []
    p_children = []

    for line in lines:
        if line != '\n':
            line_segments = parse_bolds(line.removesuffix('\n'))
            p_children.extend(line_segments)
        else:
            # Current line is "\n", so end the paragraph and start a new one
            paragraphs.append(
                html.P(
                    className=paragraph_class_name,
                    children=p_children,
                ),
            )
            p_children = []

    if len(p_children) > 0:
        # This only happens if there is no newline at the end of the txt file
        paragraphs.append(
            html.P(
                className=paragraph_class_name,
                children=p_children,
            ),
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
        first_delim = line.find('**')
        second_delim = line[first_delim + 2 :].find('**') + first_delim + 2

        if first_delim > 0:
            line_segments.append(line[:first_delim])

        line_segments.append(html.B(line[first_delim + 2 : second_delim]))

        for segment in parse_bolds(line[second_delim + 2 :]):
            line_segments.append(segment)

    return line_segments


def get_page_title(page_url):
    title_text = page_url.strip('/').replace('-', ' ').title()

    return html.H1(title_text, id='page_title')


def get_app_title(screen_width):
    if screen_width is None or screen_width > 1400:
        # App title is all on one line
        title_text = 'Explore Super Smash Bros Fighters with Interactive Visualizations!'
        app_title = html.H1(
            title_text,
            id='page-title',
            style={'font-size': '1.7vw', 'padding-top': '10px'},
        )
    else:
        # App title is split across two lines
        title_text_upper = 'Explore Super Smash Bros. Fighters'
        title_text_lower = 'with Interactive Visualizations!'
        if screen_width > 750:
            font_size = 24
        elif screen_width > 650:
            font_size = 22
        else:
            font_size = 19

        app_title = [
            html.H1(
                title_text_upper,
                id='page-title-upper',
                style={'font-size': f'{font_size}px'},
            ),
            html.H1(
                title_text_lower,
                id='page-title-lower',
                style={'font-size': f'{font_size}px', 'margin-top': '-10px'},
            ),
        ]

    return app_title


def get_screen_width(display_size_str):
    # display_size_str looks like "Breakpoint name: <=1500px, width: 1440px"
    try:
        screen_width = display_size_str.split(' ')[4]  # Looks like "1440px"
        screen_width = int(screen_width.strip('px'))
    except (IndexError, ValueError):
        return None

    return screen_width


def get_fighter_attributes_df(game='ultimate', excluded_fighter_ids=None, **kwargs):
    fighter_attributes_df = pd.read_csv(
        f'{DATA_DIR}/{game}_fighter_params.csv', dtype={'fighter_number': str}, **kwargs
    )

    if excluded_fighter_ids is not None:
        fighter_attributes_df = fighter_attributes_df.loc[
            ~fighter_attributes_df.index.isin(excluded_fighter_ids)
        ]

    return append_img_urls(fighter_attributes_df, game=game)


def append_row_col_for_fighter_selector(fighters_df):
    fighters_df = fighters_df.sort_values(by='fighter_number', ignore_index=True)

    # Calculate number of rows and columns needed for a square grid
    n_fighters = len(fighters_df)
    n_rows = math.ceil(math.sqrt(n_fighters))
    n_cols = math.ceil(n_fighters / n_rows)

    # Generate row-column pairs and add them as new columns
    row_cols = [*product(range(n_rows), range(n_cols))][:n_fighters]
    fighters_df['row_number'], fighters_df['col_number'] = zip(*row_cols, strict=True)

    return fighters_df


def append_img_urls(fighters_df, game='ultimate'):
    clean_fighter_names = (
        fighters_df['fighter']
        .str.lower()
        .str.replace(' ', '_', regex=False)
        .str.replace('&', 'and', regex=False)
        .str.replace(r'\.|\(|\)', '', regex=True)
    )

    fighters_df['img_url'] = (
        IMG_DIR
        + f'/heads/{game}/'
        + fighters_df['fighter_number']
        + '_'
        + clean_fighter_names
        + '.png'
    )

    return fighters_df


def get_correlations_df():
    fighter_attributes_df = get_fighter_attributes_df().drop(
        columns=['row_number', 'col_number', 'number_of_jumps', 'jump_frames'],
        errors='ignore',
    )

    column_names = fighter_attributes_df.columns.tolist()
    formatted_names = [format_attribute_name(column_name) for column_name in column_names]
    fighter_attributes_df = fighter_attributes_df.rename(
        columns=dict(zip(column_names, formatted_names, strict=True)),
    )

    corr_df = fighter_attributes_df.corr(numeric_only=True, method='pearson')
    corr_df = (
        corr_df.reset_index()
        .melt(id_vars='index')
        .rename(
            columns={
                'index': 'Attribute 1',
                'variable': 'Attribute 2',
                'value': 'Correlation',
            },
        )
    )

    corr_df['Correlation'] = corr_df['Correlation'].round(4)
    corr_df['corr_2dec'] = corr_df['Correlation'].round(2)
    corr_df['corr_1dec'] = corr_df['Correlation'].round(1)
    corr_df['abs_corr'] = corr_df['Correlation'].abs()

    return corr_df


def get_dropdown_options(data_type, game):
    attribute_columns = get_valid_attributes(data_type, game)
    attribute_names = [
        format_attribute_name(column_name) for column_name in attribute_columns
    ]

    return [
        {'value': column, 'label': name}
        for column, name in zip(attribute_columns, attribute_names, strict=True)
    ]


def get_valid_attributes(data_type, game):
    attributes_df = pd.read_csv(f'{DATA_DIR}/{game}_attribute_lookup_table.csv')

    if data_type == 'continuous':
        attributes_df = attributes_df[attributes_df['type'] == 'C']
    elif data_type == 'all':
        pass
    else:
        raise ValueError("data_type should be either 'continuous' or 'all'.")

    return attributes_df['attribute'].tolist()


def format_attribute_name(column_name):
    return column_name.replace('_', ' ').title()


def get_excluded_fighter_ids(excluded_fighter_ids_mem):
    if excluded_fighter_ids_mem is None:
        return []

    ids = excluded_fighter_ids_mem['ids']
    return [] if ids is None else ids


def get_fighter_lookup_table(game='ultimate'):
    return pd.read_csv(
        f'{DATA_DIR}/{game}_fighter_lookup_table.csv', dtype={'fighter_number': str}
    )


def convert_excluded_fighter_ids(excluded_fighter_numbers, selected_game):
    excluded_fighter_numbers_df = pd.DataFrame(excluded_fighter_numbers)
    fighter_df = get_fighter_lookup_table(game=selected_game)[['fighter_number']]

    excluded_mask = excluded_fighter_numbers_df['excluded']
    excluded_numbers = excluded_fighter_numbers_df.loc[excluded_mask, 'fighter_number']

    fighter_df['excluded'] = fighter_df['fighter_number'].isin(excluded_numbers)

    return fighter_df[fighter_df['excluded']].index.tolist()


def update_excluded_fighter_numbers(
    cur_excluded_fighter_numbers,
    excluded_fighter_ids,
    selected_game,
):
    cur_excluded_fighters_df = pd.DataFrame(cur_excluded_fighter_numbers)
    fighter_df = get_fighter_lookup_table(game=selected_game)[['fighter_number']]

    fighter_df['excluded_in_selected'] = fighter_df.index.isin(excluded_fighter_ids)

    excluded_fighters_df = pd.merge(
        cur_excluded_fighters_df,
        fighter_df,
        how='left',
        on='fighter_number',
    )
    excluded_fighters_df['excluded'] = excluded_fighters_df[
        'excluded_in_selected'
    ].fillna(excluded_fighters_df['excluded'])

    return excluded_fighters_df[['fighter_number', 'excluded']].to_dict()


def initialize_excluded_fighters(excluded=None):
    df = pd.DataFrame(
        {
            'fighter_number': [
                '01',
                '02',
                '03',
                '04',
                '04E',
                '05',
                '06',
                '07',
                '08',
                '09',
                '10',
                '11',
                '12',
                '13',
                '13E',
                '14',
                '15',
                '15B',
                '16',
                '17',
                '18',
                '19',
                '20',
                '21',
                '21E',
                '22',
                '23',
                '24',
                '25',
                '25E',
                '26',
                '27',
                '28',
                '28E',
                '29',
                '30',
                '31',
                '32',
                '33',
                '34',
                '35',
                '36',
                '37',
                '38',
                '39',
                '40',
                '41',
                '42',
                '43',
                '44',
                '45',
                '46',
                '47',
                '48',
                '49',
                '50',
                '51',
                '52',
                '53',
                '54',
                '55',
                '56',
                '57',
                '58',
                '59',
                '60',
                '60E',
                '61',
                '62',
                '63',
                '64',
                '65',
                '66',
                '66E',
                '67',
                '68',
                '69',
                '70',
                '71',
                '72',
                '73',
                '74',
                '75',
                '76',
                '77',
                '78',
                '79',
                '80',
                '81',
                '82',
            ],
        },
    )
    if excluded is None or excluded == '':
        df['excluded'] = False
    elif excluded == 'all':
        df['excluded'] = True
    else:
        raise ValueError

    return df.to_dict()


def parse_vega_fighter_selection(selector_signal):
    selector_dict = selector_signal['fighter_selector']
    if '_vgsid_' in selector_dict:
        selected_fighter_ids_string = selector_dict['_vgsid_'].strip('Set()')
    else:
        selected_fighter_ids_string = ''

    # Get fighter ids currently selected in the chart's selection_point:
    if not selected_fighter_ids_string:
        selected_fighter_ids = []
    else:
        fighter_ids = selected_fighter_ids_string.split(',')
        selected_fighter_ids = [
            int(fighter_id) - 1  # Altair off-by-one
            for fighter_id in fighter_ids
            if int(fighter_id) < 100 and int(fighter_id) >= 1
        ]

    return selected_fighter_ids


def determine_clicked_id(selected_fighter_ids=None, selector_mem=None):
    if selected_fighter_ids is None:
        selected_fighter_ids = []

    if selector_mem is None or 'selected' not in selector_mem:
        prev_selected_fighter_ids = []
    else:
        prev_selected_fighter_ids = selector_mem['selected']

    # All changes between new/old selections:
    diff = list(set(selected_fighter_ids) ^ set(prev_selected_fighter_ids))

    if len(diff) != 1:
        return None  # Should not have > 1 difference unless the chart was reset
    return diff[0]


def make_dash_table(df):
    """Return a dash definition of an HTML table for a Pandas dataframe"""
    table = []
    for _index, row in df.iterrows():
        html_row = []
        html_row = [html.Td([row[i]]) for i in range(len(row))]
        table.append(html.Tr(html_row))

    return table


def get_window_title(page_name):
    page_title = page_name.replace('pages.', '').replace('_', ' ').title()

    if page_title == 'Home':
        return 'Smash Charts'
    return page_title + ' | Smash Charts'
