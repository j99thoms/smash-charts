import pandas as pd
from bs4 import BeautifulSoup
import requests
import os
import sys


def get_html(url, verify=True):
    response = requests.get(
        url, 
        verify=verify, 
        headers={
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36"
        } 
    )

    html_text = response.text
    return html_text


def get_character_attribute_table(page_text):
    # Get the rough location of the table (which always has a "CHARACTER" column)
    character_index = page_text.find(">CHARACTER</th>")    

    table_start_index = page_text[:character_index].rfind("<table") 

    table_end_index = page_text[character_index:].find("</table>")
    table_end_index = table_end_index + character_index + len("</table>")

    table_text = page_text[table_start_index:table_end_index]
    return table_text


def html_table_to_df(html_text):
    parser = BeautifulSoup(html_text, 'html.parser')
    table = parser.find_all('table')[0]

    headers = []
    for th in table.find_all('th'):
        headers.append(th.text.strip())

    rows = []
    for tr in table.find_all('tr')[1:]: # Skip row 0 because it contains header data
        row = []
        for td in tr.find_all('td'):
            row.append(td.text.strip())
        rows.append(row)

    df = pd.DataFrame(rows, columns=headers)
    return df


def get_character_attributes_data(attribute_type, clean=True):
    attribute_types = [
        "AirAcceleration", "AirSpeed", 
        "FallSpeed", "DashSpeed", 
        "RunSpeed", "WalkSpeed", 
        "Weight"
    ]
    if attribute_type not in attribute_types:
        print(f"attribute_type should be one of {attribute_types}")
        return None
    
    website = "http://kuroganehammer.com/Ultimate/"
    url = website + attribute_type
    page_text = get_html(url, verify=False) # SSL certificate of the website has expired...

    attributes_data_table_text = get_character_attribute_table(page_text)
    attributes_df = html_table_to_df(attributes_data_table_text)
    attributes_df = attributes_df.drop(columns='RANK').set_index('CHARACTER')

    if clean==False:
        return attributes_df

    # ----
    # Clean dataframes for consistency when joining multiple dataframes together:

    if attribute_type == "AirAcceleration":
        attributes_df.loc['Dr. Mario'] = attributes_df.loc['Dr Mario']  
        attributes_df = attributes_df.drop(index='Dr Mario')

        attributes_df.loc['Ice Climbers (partner)'] = attributes_df.loc['Nana']  
        attributes_df = attributes_df.drop(index='Nana')

        attributes_df.loc['Ice Climbers (leader)'] = attributes_df.loc['Popo']  
        attributes_df = attributes_df.drop(index='Popo')

        attributes_df.loc['King Dedede'] = attributes_df.loc['Dedede']  
        attributes_df = attributes_df.drop(index='Dedede')

    if attribute_type == "AirSpeed":
        attributes_df.loc['Ice Climbers (partner)'] = attributes_df.loc['Nana']  
        attributes_df = attributes_df.drop(index='Nana')
        
        attributes_df.loc['Ice Climbers (leader)'] = attributes_df.loc['Popo']  
        attributes_df = attributes_df.drop(index='Popo')

    if attribute_type == "RunSpeed":
        attributes_df.loc['Ice Climbers (partner)'] = attributes_df.loc['Ice Climbers (Nana)']  
        attributes_df = attributes_df.drop(index='Ice Climbers (Nana)')

        attributes_df.loc['Ice Climbers (leader)'] = attributes_df.loc['Ice Climbers (Popo)']  
        attributes_df = attributes_df.drop(index='Ice Climbers (Popo)')

        attributes_df.loc['Dark Samus'] = attributes_df.loc['Dank Samus']  
        attributes_df = attributes_df.drop(index='Dank Samus')

    if attribute_type == "WalkSpeed":
        attributes_df.loc['Ice Climbers (partner)'] = attributes_df.loc['Ice Climbers (Nana)']  
        attributes_df = attributes_df.drop(index='Ice Climbers (Nana)')

        attributes_df.loc['Ice Climbers (leader)'] = attributes_df.loc['Ice Climbers (Popo)']  
        attributes_df = attributes_df.drop(index='Ice Climbers (Popo)')          

        attributes_df.loc['Mii Swordfighter'] = attributes_df.loc['Mii Swordspider']  
        attributes_df = attributes_df.drop(index='Mii Swordspider') 

    if attribute_type == "Weight":
        attributes_df.loc['Mr. Game & Watch'] = attributes_df.loc['M. Game & Watch']
        attributes_df = attributes_df.drop(index='M. Game & Watch')

        attributes_df.loc['Dr. Mario'] = attributes_df.loc['Educated Mario']  
        attributes_df = attributes_df.drop(index='Educated Mario')  # ???

        attributes_df.loc['Dark Pit'] = attributes_df.loc['Pit, but edgy']
        attributes_df = attributes_df.drop(index='Pit, but edgy')   # ???

    return attributes_df



# ===Main=== 

attribute_types = [
        "AirAcceleration", "AirSpeed", 
        "FallSpeed", "DashSpeed", 
        "RunSpeed", "WalkSpeed", 
        "Weight"
    ]

# Scrape the data tables from the website
datasets = []
for attribute_type in attribute_types:
   datasets.append(get_character_attributes_data(attribute_type))

# Join all the datasets together
attributes_df = None
for dataset in datasets:
    if attributes_df is None:
        attributes_df = dataset
    else:
        attributes_df = attributes_df.join(dataset, how="outer")

# Drop DLC characters
attributes_df = attributes_df.drop(index=[
        'Banjo Á Kazooie', 'Byleth', 'Hero', 'Joker', 'Min Min',
        'Mythra', 'Pyra', 'Sephiroth', 'Steve', 'Terry', ''
])


# Clean column names
attributes_df = attributes_df.reset_index()
attributes_df = attributes_df.rename(columns = {
    'CHARACTER': 'character',
    'MAX ADDITIONAL': 'delta_air_acc',
    'BASE VALUE': 'base_air_acc', 
    'TOTAL': 'max_air_acc', 
    'MAX AIR SPEED VALUE': 'max_air_speed',
    'MAX FALL SPEED': 'max_normal-fall_speed', 
    'FAST FALL SPEED': 'fast-fall_speed', 
    'SPEED INCREASE': 'percent_incr_fall_speed',
    'INITIAL DASH VALUE': 'initial_dash_speed', 
    'MAX RUN SPEED VALUE': 'max_run_speed',
    'MAX WALK SPEED VALUE': 'max_walk_speed',
    'WEIGHT VALUE': 'weight'
})

# Drop duplicates
attributes_df = attributes_df.drop_duplicates(subset=['character'])
attributes_df = attributes_df.set_index('character')

# Rearrange columns
cols = attributes_df.columns.tolist()
cols = [cols[-1]] + cols[-4:-1] + cols[3:-4] + cols[:3]
attributes_df = attributes_df[cols]

# Determine which characters have special formes
special_characters_boolean_mask = attributes_df.apply(
    lambda x: x.str.contains('[A-Za-z]:').any(),
    axis = 1
)
special_characters = attributes_df[special_characters_boolean_mask].index

# Deal with characters who have special formes
for special_character in special_characters:

    # Determine which attributes are affected by the character's special formes
    special_cols_boolean_mask = attributes_df.loc[special_character].str.contains('[A-Za-z]:')
    special_cols = attributes_df.columns[special_cols_boolean_mask]
    
    # List of names for the character's special formes
    special_forme_names = attributes_df.loc[
        special_character, [special_cols[0]]
    ].str.findall('[0-9 ][A-Za-z][A-Za-z ]*:').iloc[0]
    special_forme_names = [f"{special_character} ({str.lower(forme[1:-1])})" for forme in special_forme_names]

    # Row names for indexing the dataframe
    character_names = [special_character] + special_forme_names

    # Strip the numeric values.
    # - this is a Series in which each entry is a list of numbers
    special_character_data = attributes_df.loc[special_character].str.replace('[^0-9.:]', "", regex=True).str.split(':')

    # Update the dataframe
    for i, character_name in enumerate(character_names):
        if i == 0:
            character_row = special_character_data.apply(lambda x: x[0])
            attributes_df.loc[character_name] = character_row
        else:
            character_row = special_character_data.loc[special_cols].apply(lambda x: x[i])
            attributes_df.loc[character_name] = character_row


# Convert datatype to numeric
attributes_df.loc[:, 'percent_incr_fall_speed'] = attributes_df.loc[:, 'percent_incr_fall_speed'].str.strip('%')
attributes_df = attributes_df.astype('float64')

# Save to csv
script_dir = os.path.abspath(os.path.dirname(sys.argv[0]) or '.')
file_path = os.path.join(script_dir, '../data/attributes.csv')
attributes_df.to_csv(file_path)
