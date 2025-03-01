library(dplyr)
library(stringr)
library(glue)

IMG_DIR <- here::here('../../src/assets/img')

clean_fighter_name <- function(name) {
  str_to_lower(name) |>
    str_replace_all(' ', '_') |>
    str_replace_all('&', 'and') |>
    str_remove_all('\\.|\\(|\\)')
}


download_fighter_head_images <- function(img_urls, game) {
  fighters <- readr::read_csv(glue('../clean/{game}_fighter_Lookup_table.csv')) |>
    filter(fighter != 'Giga Bowser') |>
    mutate(fighter = clean_fighter_name(fighter), img_url = img_urls)

  # img_urls must be a sorted character vector (same order as the fighter lookup table)
  bad_rows <- fighters |>
    filter(!str_detect(str_to_lower(img_url), substr(str_remove_all(fighter, '_'), 1, 5)))
  if (nrow(bad_rows) > 0) cli::cli_abort(
    "{.var img_urls} does not align with {game}'s fighter lookup table."
  )

  output_dir <- file.path(IMG_DIR, 'heads', game)
  if (!dir.exists(output_dir)) dir.create(output_dir)

  purrr::pwalk(
    fighters,
    function(fighter_number, fighter, img_url) {
      file_name <- glue('{fighter_number}_{fighter}.png')
      output_file <- file.path(output_dir, file_name)
      download.file(img_url, output_file, mode = 'wb')
    }
  )
}

# ---- Smash Ultimate ----
ultimate_img_urls <- paste0(
  'https://www.ssbwiki.com/images/',
   c(
    '0/0d/MarioHeadSSBU',
    'b/ba/DonkeyKongHeadSSBU',
    'a/aa/LinkHeadSSBU',
    '7/7f/SamusHeadSSBU',
    '9/96/DarkSamusHeadSSBU',
    '0/03/YoshiHeadSSBU',
    '9/91/KirbyHeadSSBU',
    '0/04/FoxHeadSSBU',
    'f/fa/PikachuHeadSSBU',
    'c/c6/LuigiHeadSSBU',
    '0/0f/NessHeadSSBU',
    '3/35/CaptainFalconHeadSSBU',
    '9/95/JigglypuffHeadSSBU',
    'd/d2/PeachHeadSSBU',
    '9/96/DaisyHeadSSBU',
    'b/b5/BowserHeadSSBU',
    '8/8b/IceClimbersHeadSSBU',
    'd/d3/IceClimbersHeadRedSSBU',
    '3/37/SheikHeadSSBU',
    'c/c1/ZeldaHeadSSBU',
    '7/78/DrMarioHeadSSBU',
    'd/d6/PichuHeadSSBU',
    '2/2f/FalcoHeadSSBU',
    'b/bd/MarthHeadSSBU',
    '0/04/LucinaHeadSSBU',
    'c/cd/YoungLinkHeadSSBU',
    '7/78/GanondorfHeadSSBU',
    '9/96/MewtwoHeadSSBU',
    'e/ed/RoyHeadSSBU',
    '2/25/ChromHeadSSBU',
    '6/6b/MrGame%26WatchHeadSSBU',
    'd/de/MetaKnightHeadSSBU',
    'a/aa/PitHeadSSBU',
    'e/ed/DarkPitHeadSSBU',
    '7/71/ZeroSuitSamusHeadSSBU',
    '0/05/WarioHeadSSBU',
    '9/9a/SnakeHeadSSBU',
    'b/b2/IkeHeadSSBU',
    '4/40/SquirtleHeadSSBU',
    'b/b4/IvysaurHeadSSBU',
    'c/c9/CharizardHeadSSBU',
    '3/36/DiddyKongHeadSSBU',
    'f/ff/LucasHeadSSBU',
    '7/76/SonicHeadSSBU',
    'b/bb/KingDededeHeadSSBU',
    '9/91/OlimarHeadSSBU',
    'c/cd/LucarioHeadSSBU',
    'b/b3/ROBHeadSSBU',
    'e/e6/ToonLinkHeadSSBU',
    'e/e8/WolfHeadSSBU',
    'b/b9/VillagerHeadSSBU',
    '5/55/MegaManHeadSSBU',
    '8/87/WiiFitTrainerHeadSSBU',
    'e/e8/RosalinaHeadSSBU',
    '1/10/LittleMacHeadSSBU',
    '6/65/GreninjaHeadSSBU',
    'd/d8/MiiBrawlerHeadSSBU',
    'e/ef/MiiSwordfighterHeadSSBU',
    '3/3d/MiiGunnerHeadSSBU',
    'a/a9/PalutenaHeadSSBU',
    '4/45/Pac-ManHeadSSBU',
    '2/25/RobinHeadSSBU',
    'c/c1/ShulkHeadSSBU',
    '0/07/BowserJrHeadSSBU',
    'a/a1/DuckHuntHeadSSBU',
    'f/fb/RyuHeadSSBU',
    '7/72/KenHeadSSBU',
    '3/3b/CloudHeadSSBU',
    'c/cf/CorrinHeadSSBU',
    '6/6c/BayonettaHeadSSBU',
    'f/f1/InklingHeadSSBU',
    '5/5b/RidleyHeadSSBU',
    'd/df/SimonHeadSSBU',
    '0/07/RichterHeadSSBU',
    'd/de/KingKRoolHeadSSBU',
    '2/2f/IsabelleHeadSSBU',
    '5/50/IncineroarHeadSSBU',
    '3/38/PiranhaPlantHeadSSBU',
    '2/25/JokerHeadSSBU',
    '3/3d/HeroHeadSSBU',
    '6/60/Banjo%26KazooieHeadSSBU',
    'f/f9/TerryHeadSSBU',
    'a/a2/BylethHeadSSBU',
    'd/de/MinMinHeadSSBU',
    '1/11/SteveHeadSSBU',
    '5/5e/SephirothHeadSSBU',
    '7/79/PyraHeadSSBU',
    '3/32/MythraHeadSSBU',
    '6/67/KazuyaHeadSSBU',
    '0/0e/SoraHeadSSBU'
  ),
  '.png'
)

download_fighter_head_images(ultimate_img_urls, game = 'ultimate')

# ---- Smash Melee ----
melee_img_urls <- paste0(
  'https://www.ssbwiki.com/images/',
  c(
    'e/ec/MarioHeadSSBM',
    '9/9b/DonkeyKongHeadSSBM',
    '1/17/LinkHeadSSBM',
    'f/f6/SamusHeadSSBM',
    '6/6d/YoshiHeadSSBM',
    '7/7a/KirbyHeadSSBM',
    'd/db/FoxHeadSSBM',
    '8/88/PikachuHeadSSBM',
    'd/d1/LuigiHeadSSBM',
    '4/47/NessHeadSSBM',
    '5/5f/CaptainFalconHeadSSBM',
    '5/5a/JigglypuffHeadSSBM',
    '3/3f/PeachHeadSSBM',
    '3/3b/BowserHeadSSBM',
    'd/d1/IceClimbersHeadSSBM',
    'c/c3/IceClimbersHeadRedSSBM',
    '7/76/SheikHeadSSBM',
    '2/29/ZeldaHeadSSBM',
    '6/61/DrMarioHeadSSBM',
    '3/30/PichuHeadSSBM',
    'd/d6/FalcoHeadSSBM',
    '9/9b/MarthHeadSSBM',
    'a/ac/YoungLinkHeadSSBM',
    '7/77/GanondorfHeadSSBM',
    '5/5b/MewtwoHeadSSBM',
    'f/f2/RoyHeadSSBM',
    'b/ba/MrGame%26WatchHeadSSBM'
  ),
  '.png'
)

download_fighter_head_images(melee_img_urls, game = 'melee')
