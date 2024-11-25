library(here)
library(dplyr)
library(stringr)

IMG_DIR <- here('../src/assets/img')

img_files <- c(
  "0/0d/MarioHeadSSBU",
  "b/ba/DonkeyKongHeadSSBU",
  "a/aa/LinkHeadSSBU",
  "7/7f/SamusHeadSSBU",
  "0/03/YoshiHeadSSBU",
  "9/91/KirbyHeadSSBU",
  "0/04/FoxHeadSSBU",
  "f/fa/PikachuHeadSSBU",
  "c/c6/LuigiHeadSSBU",
  "0/0f/NessHeadSSBU",
  "3/35/CaptainFalconHeadSSBU",
  "9/95/JigglypuffHeadSSBU",
  "d/d2/PeachHeadSSBU",
  "b/b5/BowserHeadSSBU",
  "8/8b/IceClimbersHeadSSBU",
  "d/d3/IceClimbersHeadRedSSBU",
  "3/37/SheikHeadSSBU",
  "c/c1/ZeldaHeadSSBU",
  "7/78/DrMarioHeadSSBU",
  "d/d6/PichuHeadSSBU",
  "2/2f/FalcoHeadSSBU",
  "b/bd/MarthHeadSSBU",
  "c/cd/YoungLinkHeadSSBU",
  "7/78/GanondorfHeadSSBU",
  "9/96/MewtwoHeadSSBU",
  "e/ed/RoyHeadSSBU",
  "6/6b/MrGame%26WatchHeadSSBU",
  "d/de/MetaKnightHeadSSBU",
  "a/aa/PitHeadSSBU",
  "7/71/ZeroSuitSamusHeadSSBU",
  "0/05/WarioHeadSSBU",
  "9/9a/SnakeHeadSSBU",
  "b/b2/IkeHeadSSBU",
  "4/40/SquirtleHeadSSBU",
  "b/b4/IvysaurHeadSSBU",
  "c/c9/CharizardHeadSSBU",
  "3/36/DiddyKongHeadSSBU",
  "f/ff/LucasHeadSSBU",
  "7/76/SonicHeadSSBU",
  "b/bb/KingDededeHeadSSBU",
  "9/91/OlimarHeadSSBU",
  "c/cd/LucarioHeadSSBU",
  "b/b3/ROBHeadSSBU",
  "e/e6/ToonLinkHeadSSBU",
  "e/e8/WolfHeadSSBU",
  "b/b9/VillagerHeadSSBU",
  "5/55/MegaManHeadSSBU",
  "8/87/WiiFitTrainerHeadSSBU",
  "e/e8/RosalinaHeadSSBU",
  "1/10/LittleMacHeadSSBU",
  "6/65/GreninjaHeadSSBU",
  "d/d8/MiiBrawlerHeadSSBU",
  "e/ef/MiiSwordfighterHeadSSBU",
  "3/3d/MiiGunnerHeadSSBU",
  "a/a9/PalutenaHeadSSBU",
  "4/45/Pac-ManHeadSSBU",
  "2/25/RobinHeadSSBU",
  "c/c1/ShulkHeadSSBU",
  "0/07/BowserJrHeadSSBU",
  "a/a1/DuckHuntHeadSSBU",
  "f/fb/RyuHeadSSBU",
  "3/3b/CloudHeadSSBU",
  "c/cf/CorrinHeadSSBU",
  "6/6c/BayonettaHeadSSBU",
  "f/f1/InklingHeadSSBU",
  "5/5b/RidleyHeadSSBU",
  "d/df/SimonHeadSSBU",
  "d/de/KingKRoolHeadSSBU",
  "2/2f/IsabelleHeadSSBU",
  "5/50/IncineroarHeadSSBU",
  "3/38/PiranhaPlantHeadSSBU",
  "2/25/JokerHeadSSBU",
  "3/3d/HeroHeadSSBU",
  "6/60/Banjo%26KazooieHeadSSBU",
  "f/f9/TerryHeadSSBU",
  "a/a2/BylethHeadSSBU",
  "d/de/MinMinHeadSSBU",
  "1/11/SteveHeadSSBU",
  "5/5e/SephirothHeadSSBU",
  "7/79/PyraHeadSSBU",
  "3/32/MythraHeadSSBU",
  "6/67/KazuyaHeadSSBU",
  "0/0e/SoraHeadSSBU",
  "9/96/DarkSamusHeadSSBU",
  "9/96/DaisyHeadSSBU",
  "0/04/LucinaHeadSSBU",
  "2/25/ChromHeadSSBU",
  "e/ed/DarkPitHeadSSBU",
  "7/72/KenHeadSSBU",
  "0/07/RichterHeadSSBU"
)

character_data <- readr::read_csv('character_data.csv', col_select = 1:2) |>
  janitor::clean_names() |>
  filter(character != "Giga Bowser") |>
  mutate(
    character = str_to_lower(character) |>
      str_replace_all(" ", "_") |>
      str_replace_all("&", "and") |>
      str_remove_all("\\.|\\(|\\)"),
    img_url = paste0("https://www.ssbwiki.com/images/", img_files, ".png")
  )

output_dir <- file.path(IMG_DIR, 'heads')
if (!dir.exists(output_dir)) dir.create(output_dir)

purrr::pwalk(
  character_data,
  function(character_number, character, img_url) {
    file_name <- glue::glue("{character_number}_{character}.png")
    output_file <- file.path(output_dir, file_name)
    download.file(img_url, output_file, mode = "wb")
  }
)
