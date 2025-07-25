library(readr)
library(dplyr)

DATA_DIR <- here::here('../')

# Normalize a column using min-max scaling (0-1)
normalize_minmax <- function(x) {
  (x - min(x, na.rm = TRUE)) / (max(x, na.rm = TRUE) - min(x, na.rm = TRUE))
}

# Normalize a column using z-score
normalize_zscore <- function(x) {
  (x - mean(x, na.rm = TRUE)) / sd(x, na.rm = TRUE)
}

# Apply normalization to all numeric columns in a dataset of fighter attributes
apply_normalization <- function(df, method) {
  if (method == 'minmax') normalize_fnc <- normalize_minmax
  else if (method == 'zscore') normalize_fnc <- normalize_zscore
  else stop("method must be 'minmax' or 'zscore'.")

  df |>
    mutate(
      fighter_number = as.character(fighter_number),
      across(where(is.numeric), ~ normalize_fnc(.))
    )
}

# Run normalization for all games using all methods
games <- c('64', 'melee', 'brawl', 'sm4sh', 'ultimate')
methods <- c('minmax', 'zscore')

for (game in games) {
  input_file <- file.path(DATA_DIR, glue::glue('clean/{game_name}_fighter_params.csv'))

  if (!file.exists(input_file)) {
    warning(glue::glue('{input_file} not found.'))
    next
  }

  fighter_data <- read_csv(input_file, show_col_types = FALSE)

  for (method in methods) {
    normalized_data <- apply_normalization(fighter_data, method)

    # Write normalized data to file
    output_file <- file.path(
      DATA_DIR, glue::glue('clean/normalized/{game}_fighter_params_{method}.csv')
    )
    write_csv(normalized_data, output_file)
  }
}
