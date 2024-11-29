library(readr)
library(dplyr)

raw_character_data <- read_csv('character_data_v13_0_1.csv', skip = 2)

cleaned_character_data <- raw_character_data |>
  rename(character_number = `...1`) |>
  janitor::clean_names() |>
  select(
    character_number, character, weight, maximum_fall_speed, fastfall_speed,
    dash_initial_velocity, run_maximum_velocity, maximum_horizontal_air_speed,
    base_air_acceleration, air_maximum_additional_acceleration, ground_friction,
    base_run_acceleration, run_maximum_additional_accel, jump_heights, hop_heights,
    air_jump_heights, horizontal_air_friction, gravity, ledge_jump_height,
    number_of_jumps, has_walljump, has_crawl, has_wallcling, has_zair
  ) |>
  rename(
    max_fall_speed = maximum_fall_speed,
    initial_dash_speed = dash_initial_velocity,
    max_run_speed = run_maximum_velocity,
    max_horizontal_air_speed = maximum_horizontal_air_speed,
    air_acceleration_range = air_maximum_additional_acceleration,
    run_acceleration_range = run_maximum_additional_accel,
    jump_height = jump_heights,
    hop_height = hop_heights,
    air_jump_height = air_jump_heights
  ) |>
  mutate(
    number_of_jumps = purrr::map_dbl(
      number_of_jumps, ~ as.integer(substring(., 3))
    )
  )

glimpse(cleaned_character_data)

write_csv(cleaned_character_data, 'character_data.csv')
