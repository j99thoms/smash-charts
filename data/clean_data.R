library(readr)
library(dplyr)

raw_character_data <- read_csv('character_data_v13_0_1.csv', skip = 2)

cleaned_character_data <- raw_character_data |>
  rename(`Character #` = `...1`) |> 
  select(
    `Character #`, Character, Weight, `Maximum Fall Speed`, `Fastfall Speed`,
    `Dash Initial Velocity`, `Run Maximum Velocity`, `Maximum Horizontal Air Speed`,
    `Base Air Acceleration`, `Air Maximum Additional Acceleration`, `Ground Friction`,
    `Base Run Acceleration`, `Run Maximum Additional Accel`, `Jump heights`, `Hop heights`,
    `Air jump heights`, `Horizontal Air Friction`, `Gravity`, `Ledge Jump Height`,
    `Number of Jumps`, `Has Walljump`, `Has Crawl`, `Has Wallcling`, `Has Zair`
  ) |>
  rename(
    `Max Fall Speed` = `Maximum Fall Speed`,
    `Fast Fall Speed` = `Fastfall Speed`,
    `Initial Dash Speed` = `Dash Initial Velocity`,
    `Max Run Speed` = `Run Maximum Velocity`,
    `Max Horizontal Air Speed` = `Maximum Horizontal Air Speed`,
    `Air Acceleration Range` = `Air Maximum Additional Acceleration`,
    `Run Acceleration Range` = `Run Maximum Additional Accel`,
    `Jump Height` = `Jump heights`,
    `Hop Height` = `Hop heights`,
    `Air Jump Height` = `Air jump heights`
  ) |>
  mutate(
    `Number of Jumps` = purrr::map_dbl(
      `Number of Jumps`, ~ as.integer(substring(., 3))
    )
  )

glimpse(cleaned_character_data)

write_csv(cleaned_character_data, 'character_data.csv')
