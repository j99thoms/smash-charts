library(readr)
library(dplyr)

DATA_DIR <- here::here('../')

# Download the raw dataset from Google sheets
fighter_params_sheet_url <- paste0(
  'https://docs.google.com/spreadsheets/d/',
  '1N7UdejkLvRQeq4mfwupiu8Kioc7BFBUPjprkuiV0nAM/',
  'export?format=csv&gid=706249581'
)
raw_fighter_params_filename <- file.path(
  DATA_DIR, 'raw/sm4sh_fighter_params.csv'
)
download.file(
  fighter_params_sheet_url, raw_fighter_params_filename, mode = 'wb'
)

# We'll use ultimate's fighter lookup table to assign a number to each fighter:
ultimate_fighter_lookup_table <- read_csv(
  file.path(DATA_DIR, 'clean/ultimate_fighter_lookup_table.csv')
)

# Clean the raw dataset
raw_fighter_params <- read_csv(raw_fighter_params_filename, skip = 2)
cleaned_fighter_params <- raw_fighter_params |>
  janitor::clean_names() |>
  transmute(
    fighter = character,
    weight,
    max_fall_speed = maximum_fall_speed,
    fastfall_speed,
    initial_dash_speed = dash_initial_velocity,
    run_speed = run_maximum_velocity,
    horizontal_air_speed = maximum_horizontal_air_speed,
    base_air_acceleration,
    air_acceleration_range = air_maximum_additional_acceleration,
    jump_frames = as.integer(jump_startup_frames),
    base_run_acceleration,
    run_acceleration_range = run_maximum_additional_accel,
    jump_height = jump_heights,
    hop_height = hop_heights,
    air_jump_height = air_jump_heights,
    horizontal_air_friction,
    gravity,
    ledge_jump_height,
    number_of_jumps = as.integer(number_of_jumps),
    shield_size
  ) |>
  filter(
    !stringr::str_detect(fighter, 'Miienemy|Miis multiplier'),
    !(fighter %in% c('Giga Bowser', 'Giga Mac', 'Mega Lucario', 'Warioman'))
  ) |>
  mutate(
    fighter = case_match(
      fighter,
      'Mr. Game and Watch' ~ 'Mr. Game & Watch',
      'Metaknight' ~ 'Meta Knight',
      'Pikmin and Olimar' ~ 'Olimar',
      'Rosalina and Luma' ~ 'Rosalina',
      'Duckhunt' ~ 'Duck Hunt',
      'Pac-man' ~ 'Pac-Man',
      .default = fighter
    )
  ) |>
  left_join(ultimate_fighter_lookup_table, by = 'fighter') |>
  group_by(fighter_number, fighter) |>
  summarise(across(everything(), ~ mean(.)), .groups = 'drop') |>
  mutate(across(c(number_of_jumps, jump_frames), ~ as.integer(.))) |>
  arrange(fighter_number)

# Write the cleaned data to file
cleaned_fighter_params_filename <- file.path(
  DATA_DIR, 'clean/sm4sh_fighter_params.csv'
)
write_csv(cleaned_fighter_params, cleaned_fighter_params_filename)

# fighter lookup table
fighter_lookup_table <- select(cleaned_fighter_params, fighter_number, fighter)
fighter_lookup_table_filename <- file.path(
  DATA_DIR, 'clean/sm4sh_fighter_lookup_table.csv'
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
  DATA_DIR, 'clean/sm4sh_attribute_lookup_table.csv'
)
write_csv(attribute_lookup_table, attribute_lookup_table_filename)
