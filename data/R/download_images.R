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

# ---- Smash 4 ----
sm4sh_img_urls <- paste0(
  'https://www.ssbwiki.com/images/',
  c(
    '2/2b/MarioHeadSSB4-U',
    'b/b2/DonkeyKongHeadSSB4-U',
    'e/ea/LinkHeadSSB4-U',
    'b/b9/SamusHeadSSB4-U',
    'c/c2/YoshiHeadSSB4-U',
    'b/bd/KirbyHeadSSB4-U',
    '4/40/FoxHeadSSB4-U',
    'd/d6/PikachuHeadSSB4-U',
    'd/d4/LuigiHeadSSB4-U',
    'c/c6/NessHeadSSB4-U',
    '4/4d/CaptainFalconHeadSSB4-U',
    '5/53/JigglypuffHeadSSB4-U',
    '5/50/PeachHeadSSB4-U',
    '4/44/BowserHeadSSB4-U',
    '6/6f/SheikHeadSSB4-U',
    '5/50/ZeldaHeadSSB4-U',
    '5/5d/DrMarioHeadSSB4-U',
    'e/ee/FalcoHeadSSB4-U',
    '4/47/MarthHeadSSB4-U',
    'e/e2/LucinaHeadSSB4-U',
    'f/fd/GanondorfHeadSSB4-U',
    '1/12/MewtwoHeadSSB4-U',
    '5/58/RoyHeadSSB4-U',
    'e/ea/MrGame%26WatchHeadSSB4-U',
    '6/65/MetaKnightHeadSSB4-U',
    '7/7a/PitHeadSSB4-U',
    '9/9b/DarkPitHeadSSB4-U',
    'c/c1/ZeroSuitSamusHeadSSB4-U',
    'e/e6/WarioHeadSSB4-U',
    'd/dd/IkeHeadSSB4-U',
    '7/7d/CharizardHeadSSB4-U',
    'a/a3/DiddyKongHeadSSB4-U',
    'c/cf/LucasHeadSSB4-U',
    'd/de/SonicHeadSSB4-U',
    'b/bf/KingDededeHeadSSB4-U',
    '7/74/OlimarHeadSSB4-U',
    '4/49/LucarioHeadSSB4-U',
    'c/c6/ROBHeadGreySSB4-U',
    'a/a0/ToonLinkHeadSSB4-U',
    '5/5d/VillagerHeadSSB4-U',
    '0/0d/MegaManHeadSSB4-U',
    '8/85/WiiFitTrainerHeadSSB4-U',
    '2/2d/Rosalina%26LumaHeadSSB4-U',
    '0/06/LittleMacHeadSSB4-U',
    'b/b0/GreninjaHeadSSB4-U',
    'b/bd/MiiBrawlerHeadSSB4-U',
    '5/56/MiiSwordfighterHeadSSB4-U',
    'b/b2/MiiGunnerHeadSSB4-U',
    'a/ad/PalutenaHeadSSB4-U',
    'b/bb/Pac-ManHeadSSB4-U',
    'e/ef/RobinHeadSSB4-U',
    '9/9d/ShulkHeadSSB4-U',
    'f/fa/BowserJrHeadSSB4-U',
    '1/15/DuckHuntHeadSSB4-U',
    'f/f1/RyuHeadSSB4-U',
    '2/2a/CloudHeadSSB4-U',
    '8/89/CorrinHeadSSB4-U',
    'b/b4/BayonettaHeadSSB4-U'
  ),
  '.png'
)

download_fighter_head_images(sm4sh_img_urls, game = 'sm4sh')

# ---- Smash Brawl ----
brawl_img_urls <- paste0(
  'https://www.ssbwiki.com/images/',
  c(
    '0/07/MarioHeadSSBB',
    '0/0b/DonkeyKongHeadSSBB',
    '2/28/LinkHeadSSBB',
    'e/ee/SamusHeadSSBB',
    'a/ab/YoshiHeadSSBB',
    'c/ca/KirbyHeadSSBB',
    '1/15/FoxHeadSSBB',
    'c/ca/PikachuHeadSSBB',
    'a/af/LuigiHeadSSBB',
    '5/51/NessHeadSSBB',
    '6/61/CaptainFalconHeadSSBB',
    '4/4a/JigglypuffHeadSSBB',
    '0/0c/PeachHeadSSBB',
    '0/05/BowserHeadSSBB',
    'e/e4/IceClimbersHeadSSBB',
    '2/2e/SheikHeadSSBB',
    '5/59/ZeldaHeadSSBB',
    '4/4b/FalcoHeadSSBB',
    '5/52/MarthHeadSSBB',
    '8/82/GanondorfHeadSSBB',
    '4/48/MrGame%26WatchHeadSSBB',
    'f/f1/MetaKnightHeadSSBB',
    'c/c8/PitHeadSSBB',
    '8/8e/ZeroSuitSamusHeadSSBB',
    'e/e1/WarioHeadSSBB',
    '6/6b/SnakeHeadSSBB',
    '3/32/IkeHeadSSBB',
    'd/d6/SquirtleHeadSSBB',
    'c/c7/IvysaurHeadSSBB',
    '3/3f/CharizardHeadSSBB',
    '1/1c/DiddyKongHeadSSBB',
    'e/e6/LucasHeadSSBB',
    '4/4a/SonicHeadSSBB',
    '6/6b/KingDededeHeadSSBB',
    'f/fd/OlimarHeadSSBB',
    'e/e3/LucarioHeadSSBB',
    'c/cb/ROBHeadSSBB',
    '6/66/ToonLinkHeadSSBB',
    '6/63/WolfHeadSSBB'
  ),
  '.png'
)

download_fighter_head_images(brawl_img_urls, game = 'brawl')

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

# ---- Smash 64 ----
ssb_img_urls <- paste0(
  'https://www.ssbwiki.com/images/',
  c(
    'a/aa/MarioHeadSSB',
    'a/af/DonkeyKongHeadSSB',
    '3/3b/LinkHeadSSB',
    '1/14/SamusHeadSSB',
    '4/44/YoshiHeadSSB',
    'e/e0/KirbyHeadSSB',
    '8/80/FoxHeadSSB',
    '8/80/PikachuHeadSSB',
    '6/69/LuigiHeadSSB',
    'c/cd/NessHeadSSB',
    '7/75/CaptainFalconHeadSSB',
    '8/84/JigglypuffHeadSSB'
  ),
  '.png'
)

download_fighter_head_images(ssb_img_urls, game = '64')
