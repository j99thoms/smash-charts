library(readr)
library(dplyr)

DATA_DIR <- here::here('../')

# Download the raw dataset from Google sheets
fighter_params_sheet_url <- paste0(
  'https://docs.google.com/spreadsheets/d/',
  '1Zf56QjlGCZ0aLIaDv0tujqfx2XU09DOKvqjUWLV16LA/',
  'export?format=csv&gid=963542361'
)
raw_fighter_params_filename <- file.path(
  DATA_DIR, 'raw/ultimate_fighter_params.csv'
)
download.file(
  fighter_params_sheet_url, raw_fighter_params_filename, mode = 'wb'
)

# Convert fighter codenames from the raw dataset to English names
fighter_ids_and_codenames <- read_csv(
  raw_fighter_params_filename, skip = 3,
  col_select = 1:2, col_names = c('id', 'codename')
)
fighter_lookup_table <- tibble::tribble(
  ~codename,      ~fighter,                 ~number,
  'mario',        'Mario',                  '01',
  'donkey',       'Donkey Kong',            '02',
  'link',         'Link',                   '03',
  'samus',        'Samus',                  '04',
  'yoshi',        'Yoshi',                  '05',
  'kirby',        'Kirby',                  '06',
  'fox',          'Fox',                    '07',
  'pikachu',      'Pikachu',                '08',
  'luigi',        'Luigi',                  '09',
  'ness',         'Ness',                   '10',
  'captain',      'Captain Falcon',         '11',
  'purin',        'Jigglypuff',             '12',
  'peach',        'Peach',                  '13',
  'koopa',        'Bowser',                 '14',
  'popo',         'Ice Climbers (leader)',  '15',
  'nana',         'Ice Climbers (partner)', '15B',
  'sheik',        'Sheik',                  '16',
  'zelda',        'Zelda',                  '17',
  'mariod',       'Dr. Mario',              '18',
  'pichu',        'Pichu',                  '19',
  'falco',        'Falco',                  '20',
  'marth',        'Marth',                  '21',
  'younglink',    'Young Link',             '22',
  'ganon',        'Ganondorf',              '23',
  'mewtwo',       'Mewtwo',                 '24',
  'roy',          'Roy',                    '25',
  'gamewatch',    'Mr. Game & Watch',       '26',
  'metaknight',   'Meta Knight',            '27',
  'pit',          'Pit',                    '28',
  'szerosuit',    'Zero Suit Samus',        '29',
  'wario',        'Wario',                  '30',
  'snake',        'Snake',                  '31',
  'ike',          'Ike',                    '32',
  'pzenigame',    'Squirtle',               '33',
  'pfushigisou',  'Ivysaur',                '34',
  'plizardon',    'Charizard',              '35',
  'diddy',        'Diddy Kong',             '36',
  'lucas',        'Lucas',                  '37',
  'sonic',        'Sonic',                  '38',
  'dedede',       'King Dedede',            '39',
  'pikmin',       'Olimar',                 '40',
  'lucario',      'Lucario',                '41',
  'robot',        'R.O.B.',                 '42',
  'toonlink',     'Toon Link',              '43',
  'wolf',         'Wolf',                   '44',
  'murabito',     'Villager',               '45',
  'rockman',      'Mega Man',               '46',
  'wiifit',       'Wii Fit Trainer',        '47',
  'rosetta',      'Rosalina',               '48',
  'littlemac',    'Little Mac',             '49',
  'gekkouga',     'Greninja',               '50',
  'miifighter',   'Mii Brawler',            '51',
  'miiswordsman', 'Mii Swordfighter',       '52',
  'miigunner',    'Mii Gunner',             '53',
  'palutena',     'Palutena',               '54',
  'pacman',       'Pac-Man',                '55',
  'reflet',       'Robin',                  '56',
  'shulk',        'Shulk',                  '57',
  'koopajr',      'Bowser Jr.',             '58',
  'duckhunt',     'Duck Hunt',              '59',
  'ryu',          'Ryu',                    '60',
  'cloud',        'Cloud',                  '61',
  'kamui',        'Corrin',                 '62',
  'bayonetta',    'Bayonetta',              '63',
  'inkling',      'Inkling',                '64',
  'ridley',       'Ridley',                 '65',
  'simon',        'Simon',                  '66',
  'krool',        'King K. Rool',           '67',
  'shizue',       'Isabelle',               '68',
  'gaogaen',      'Incineroar',             '69',
  'packun',       'Piranha Plant',          '70',
  'jack',         'Joker',                  '71',
  'brave',        'Hero',                   '72',
  'buddy',        'Banjo & Kazooie',        '73',
  'dolly',        'Terry',                  '74',
  'master',       'Byleth',                 '75',
  'tantan',       'Min Min',                '76',
  'pickel',       'Steve',                  '77',
  'demon',        'Sephiroth',              '78',
  'trail',        'Pyra',                   '79',
  'eflame',       'Mythra',                 '80',
  'elight',       'Kazuya',                 '81',
  'edge',         'Sora',                   '82',
  'samusd',       'Dark Samus',             '04E',
  'daisy',        'Daisy',                  '13E',
  'lucina',       'Lucina',                 '21E',
  'chrom',        'Chrom',                  '25E',
  'pitb',         'Dark Pit',               '28E',
  'ken',          'Ken',                    '60E',
  'richter',      'Richter',                '66E',
  'koopag',       'Giga Bowser',            NA
)
map_fighter_id_to_name_and_number <- fighter_ids_and_codenames |>
  inner_join(fighter_lookup_table, by = 'codename') |>
  select(id, number, fighter)

# Clean the raw dataset
raw_fighter_params <- read_csv(
  raw_fighter_params_filename, skip = 2, col_select = -2
)
cleaned_fighter_params <- raw_fighter_params |>
  janitor::clean_names() |>
  select(
    id = x1, # lets us join to the tibble of English names created above
    weight,
    max_fall_speed = maximum_fall_speed,
    fastfall_speed,
    initial_dash_speed = dash_initial_velocity,
    run_speed = run_maximum_velocity,
    horizontal_air_speed = maximum_horizontal_air_speed,
    base_air_acceleration,
    air_acceleration_range = air_maximum_additional_acceleration,
    base_run_acceleration,
    run_acceleration_range = run_maximum_additional_accel,
    jump_height = jump_heights,
    hop_height = hop_heights,
    air_jump_height = air_jump_heights,
    horizontal_air_friction,
    gravity,
    ledge_jump_height,
    number_of_jumps
  ) |>
  mutate(
    number_of_jumps = purrr::map_int(
      number_of_jumps, ~ as.integer(stringr::str_remove(., '0x'))
    )
  ) |>
  inner_join(map_fighter_id_to_name_and_number, by = 'id') |>
  select(-id) |>
  select(fighter_number = number, fighter, everything()) |>
  arrange(fighter_number)

# Write the cleaned data to file
cleaned_fighter_params_filename <- file.path(
  DATA_DIR, 'clean/ultimate_fighter_params.csv'
)
write_csv(cleaned_fighter_params, cleaned_fighter_params_filename)

# fighter lookup table
fighter_lookup_table <- select(cleaned_fighter_params, fighter_number, fighter)
fighter_lookup_table_filename <- file.path(
  DATA_DIR, 'clean/ultimate_fighter_lookup_table.csv'
)
write_csv(fighter_lookup_table, fighter_lookup_table_filename)

# attribute lookup table
attribute_lookup_table <- tibble(
  attribute = names(select(cleaned_fighter_params, -c(fighter_number, fighter)))
) |>
  mutate(
    type = purrr::map_chr(attribute, ~ class(pull(cleaned_fighter_params, .))),
    type = case_match(
      type, 'integer' ~ 'O', 'numeric' ~ 'C'  # O --> ordinal; C --> continuous
    )
)
attribute_lookup_table_filename <- file.path(
  DATA_DIR, 'clean/ultimate_attribute_lookup_table.csv'
)
write_csv(attribute_lookup_table, attribute_lookup_table_filename)
