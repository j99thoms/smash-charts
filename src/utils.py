import pandas as pd


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
