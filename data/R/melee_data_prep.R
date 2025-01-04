library(readr)
library(dplyr)

DATA_DIR <- here::here('../')

# Download the raw dataset from Google sheets
fighter_params_sheet_url <- paste0(
  'https://docs.google.com/spreadsheets/d/',
  '16jPsSs7IXyKNwaGnQpK2aijwX2U9Z6G03Mi7zgtpHBM/',
  'export?format=csv&gid=1426416407'
)
raw_fighter_params_filename <- file.path(
  DATA_DIR, 'raw/melee_fighter_params.csv'
)
download.file(
  fighter_params_sheet_url, raw_fighter_params_filename, mode = 'wb'
)

# Convert fighter codenames from the raw dataset to English names
fighter_lookup_table <- tibble::tribble(
  ~codename,  ~fighter,                  ~number,
  'Ma',       'Mario',                   '01',
  'DK',       'Donkey Kong',             '02',
  'Lk',       'Link',                    '03',
  'Sm',       'Samus',                   '04',
  'Ys',       'Yoshi',                   '05',
  'Kb',       'Kirby',                   '06',
  'Fx',       'Fox',                     '07',
  'Pk',       'Pikachu',                 '08',
  'Lg',       'Luigi',                   '09',
  'Ns',       'Ness',                    '10',
  'CF',       'Captain Falcon',          '11',
  'Jp',       'Jigglypuff',              '12',
  'Pc',       'Peach',                   '13',
  'Bw',       'Bowser',                  '14',
  'Po',       'Ice Climbers (leader)',   '15',
  'Na',       'Ice Climbers (partner)',  '15B',
  'Sh',       'Sheik',                   '16',
  'Zd',       'Zelda',                   '17',
  'DM',       'Dr. Mario',               '18',
  'Pi',       'Pichu',                   '19',
  'Fc',       'Falco',                   '20',
  'Mh',       'Marth',                   '21',
  'YL',       'Young Link',              '22',
  'Gn',       'Ganondorf',               '23',
  'Mw',       'Mewtwo',                  '24',
  'Ry',       'Roy',                     '25',
  'GW',       'Mr. Game & Watch',        '26',
  'GB',       'Giga Bowser',             NA
)

# Clean the raw dataset
raw_fighter_params <- read_csv(
  raw_fighter_params_filename, col_select = -1
)
cleaned_fighter_params <- raw_fighter_params |>
  select(!matches('\\.\\.\\.')) |>
  janitor::clean_names() |>
  select(
    codename = char, # lets us join to the lookup table of English names
    weight,
    max_fall_speed = term_vel,
    fastfall_speed = ff_term_vel,
    initial_dash_speed = dash_init,
    run_speed,
    air_speed = airspeed,
    air_acceleration = air_accel,
    jump_frames,
    run_acceleration = run_accel,
    jump_height = jump_v,
    hop_height = hop_v,
    air_friction = air_fric,
    gravity,
    ledge_jump_height = edge_jump_v,
    number_of_jumps = jumps,
    shield_size
  ) |>
  inner_join(fighter_lookup_table, by = 'codename') |>
  select(-codename) |>
  select(fighter_number = number, fighter, everything()) |>
  arrange(fighter_number)

# Write the cleaned data to file
cleaned_fighter_params_filename <- file.path(
  DATA_DIR, 'clean/melee_fighter_params.csv'
)
write_csv(cleaned_fighter_params, cleaned_fighter_params_filename)
