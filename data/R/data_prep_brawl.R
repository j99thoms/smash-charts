library(readxl)
library(readr)
library(dplyr)
library(tidyr)
library(stringr)

DATA_DIR <- here::here('../')

# Download the raw dataset from Google sheets.
# Note that we need it in xlsx format because each fighter's data is in a separate sheet.
fighter_params_sheet_url <- paste0(
  'https://docs.google.com/spreadsheets/d/',
  '1_5NFTe3dvxxC6MMlsI49mnC5m7D3_y5UoGZ7mxPje1I/',
  'export?format=xlsx'
)
raw_fighter_params_filename_excel <- file.path(DATA_DIR, 'raw/brawl_fighter_params.xlsx')
download.file(
  fighter_params_sheet_url, raw_fighter_params_filename_excel, mode = 'wb'
)

brawl_fighters <- tibble::tribble(
  ~fighter,                 ~number,
  'Mario',                  '01',
  'Donkey Kong',            '02',
  'Link',                   '03',
  'Samus',                  '04',
  'Yoshi',                  '05',
  'Kirby',                  '06',
  'Fox',                    '07',
  'Pikachu',                '08',
  'Luigi',                  '09',
  'Ness',                   '10',
  'Captain Falcon',         '11',
  'Jigglypuff',             '12',
  'Peach',                  '13',
  'Bowser',                 '14',
  'Ice Climbers (leader)',  '15',
  'Sheik',                  '16',
  'Zelda',                  '17',
  'Falco',                  '20',
  'Marth',                  '21',
  'Ganondorf',              '23',
  'Mr. Game & Watch',       '26',
  'Meta Knight',            '27',
  'Pit',                    '28',
  'Zero Suit Samus',        '29',
  'Wario',                  '30',
  'Snake',                  '31',
  'Ike',                    '32',
  'Squirtle',               '33',
  'Ivysaur',                '34',
  'Charizard',              '35',
  'Diddy Kong',             '36',
  'Lucas',                  '37',
  'Sonic',                  '38',
  'King Dedede',            '39',
  'Olimar',                 '40',
  'Lucario',                '41',
  'R.O.B.',                 '42',
  'Toon Link',              '43',
  'Wolf',                   '44',
)

read_brawl_sheet <- function(sheet) {
  data_range <- 'B1:G3' # The cells containing the fighter's physical attributes
  read_xlsx(
    raw_fighter_params_filename_excel,
    sheet = sheet, range = data_range, col_names = FALSE
  )
}

# Load the sheets one at a time, and combine them all together
raw_fighter_params <- purrr::map_dfr(
  brawl_fighters$fighter, function(fighter) {
    suppressMessages({
      sheet <- try(read_brawl_sheet(fighter), silent = TRUE)
      if (inherits(sheet, 'try-error')) {
        # Deal with edge cases
        sheet <- switch(
          fighter,
          'Fox' = read_brawl_sheet('Fox '),
          'Ice Climbers (leader)' = read_brawl_sheet('Ice Climbers'),
          'Meta Knight' = read_brawl_sheet('Meta Knight ')
        )
      }
    })

  sheet |>
    mutate(fighter = fighter)
  }
)

# Write 'raw' data to csv and delete xlsx file
# (we don't push the full xlsx file to GitHub because it has images and is too bulky)
raw_fighter_params_filename <- file.path(DATA_DIR, 'raw/brawl_fighter_params.csv')
write_csv(raw_fighter_params, raw_fighter_params_filename, na = '', col_names = FALSE)
file.remove(raw_fighter_params_filename_excel)

# Clean the raw dataset
cleaned_fighter_params <- raw_fighter_params |>
  janitor::clean_names() |>
  filter(!(x1 == 'Character Attributes' & is.na(x2))) |>
  pivot_longer(-fighter) |>
  transmute(
    fighter,
    attribute = str_remove(value, '\\n.*$'),
    value = str_remove(value, '^.*\\n')
  ) |>
  pivot_wider(names_from = 'attribute', values_from = 'value') |>
  janitor::clean_names() |>
  mutate(across(
    -fighter,
    ~ if_else(
      str_detect(., 'frames'),
      trimws(str_remove(., 'frames')) |> as.integer(),
      trimws(.) |> as.numeric()
    )
  )) |>
  left_join(brawl_fighters, by = 'fighter') |>
  transmute(
    fighter_number = number,
    fighter,
    weight,
    max_fall_speed = fall_speed,
    fastfall_speed = fast_fall,
    walk_speed = walk,
    initial_dash_speed = initial_dash,
    run_speed = dash,
    horizontal_air_speed = air_speed,
    horizontal_air_acceleration = air_accel,
    gravity,
    traction,
    jumpsquat_frames = as.integer(jumpsquat),
    meteor_cancel_frames = as.integer(meteor_cancel)
  ) |>
  arrange(fighter_number)

# Write the cleaned data to file
cleaned_fighter_params_filename <- file.path(DATA_DIR, 'clean/brawl_fighter_params.csv')
write_csv(cleaned_fighter_params, cleaned_fighter_params_filename)

# fighter lookup table
fighter_lookup_table <- select(cleaned_fighter_params, fighter_number, fighter)
fighter_lookup_table_filename <- file.path(DATA_DIR, 'clean/brawl_fighter_lookup_table.csv')
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
attribute_lookup_table_filename <- file.path(DATA_DIR, 'clean/brawl_attribute_lookup_table.csv')
write_csv(attribute_lookup_table, attribute_lookup_table_filename)
