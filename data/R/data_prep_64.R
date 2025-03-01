library(readr)
library(dplyr)
library(tidyr)

DATA_DIR <- here::here('../')

# Download the raw dataset from Google sheets
fighter_params_sheet_url <- paste0(
  'https://docs.google.com/spreadsheets/d/',
  '1UfGuZnztuUM4ldjgkSnOV_G5KLa2DGwrYo_eRxhVWvg/',
  'export?format=csv&gid=667304140'
)
raw_fighter_params_filename <- file.path(
  DATA_DIR, 'raw/64_fighter_params.csv'
)
download.file(
  fighter_params_sheet_url, raw_fighter_params_filename, mode = 'wb'
)

# Clean the raw dataset
raw_fighter_params <- read_csv(raw_fighter_params_filename)
cleaned_fighter_params <- raw_fighter_params |>
  rename(attribute = `...1`) |>
  filter(attribute != 'Body Material') |>
  mutate(across(Mario:Jigglypuff, as.numeric)) |>
  pivot_longer(Mario:Jigglypuff, names_to = 'fighter') |>
  pivot_wider(names_from = 'attribute', values_from = 'value') |>
  janitor::clean_names() |>
  transmute(
    fighter_number = sprintf('%02.f', row_number()),
    fighter,
    weight,
    max_fall_speed = maximum_fall_speed,
    fastfall_speed = maximum_fastfall_speed,
    walk_speed_factor,
    initial_dash_speed,
    run_speed,
    horizontal_air_speed = maximum_aerial_x_axis_speed,
    horizontal_air_friction = aerial_x_axis_deceleration,
    gravity = falling_acceleration,
    traction,
    jumpsquat_frames = as.integer(jumpsquat_length),
    number_of_jumps = as.integer(maximum_jumps),
    shield_size = shield_radius
  )

# Write the cleaned data to file
cleaned_fighter_params_filename <- file.path(
  DATA_DIR, 'clean/64_fighter_params.csv'
)
write_csv(cleaned_fighter_params, cleaned_fighter_params_filename)

# fighter lookup table
fighter_lookup_table <- select(cleaned_fighter_params, fighter_number, fighter)
fighter_lookup_table_filename <- file.path(
  DATA_DIR, 'clean/64_fighter_lookup_table.csv'
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
  DATA_DIR, 'clean/64_attribute_lookup_table.csv'
)
write_csv(attribute_lookup_table, attribute_lookup_table_filename)
