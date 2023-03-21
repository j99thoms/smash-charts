# The Super Smash Dashboard!

#### Try it out at [the-super-smash-dashboard.onrender.com](https://the-super-smash-dashboard.onrender.com)!

Welcome to The Super Smash Dashboard! This is a resource for Super Smash Bros. players who are interested in exploring the various quantitative attributes that control a character's in-game physics, such a character's weight, a character's maximum movement speed (in various forms, e.g. walking, running, and airborne), and a character's airborne acceleration.


## Proposal

I ([@J99thoms](https://github.com/J99thoms)) am a graduate student at the University of British Columbia who is enrolled in the Master of Data Science program ([UBC-MDS](https://github.com/UBC-MDS)). I am also a huge fan of Super Smash Bros. As a result, The Super Smash Dashboard was created as both a personal project as well as to satisfiy part of the requirements of the UBC MDS program. The project proposal can be found [here](proposal.md).

## Usage

With this dashboard, users are able to choose which attributes to visualize as well as how to visualize those attributes. Users can quickly see which characters have the highest/lowest value in any given attribute by using a bar chart, and can also see how any given attribute relates to any other attribute by using a scatter plot. The visualizations include tooltips so that one is able to determine the exact values of a character's attributes by simply hovering their mouse over the relevant section of the visualization.

## Credits and References

Character attribute data is not directly accessible within the game itself, and I was unable to find a nice data file (e.g. `.csv` or `.json`) with the dataset. The best I could find were websites with the data in tabular format (i.e. `HTML` tables).
As a result, I had to create the dataset myself by scraping data from one of these websites. I used [kuroganehammer.com](http://kuroganehammer.com/Ultimate/) for this since the tables on this site are in a fairly consistent format, which makes scraping data easier. The resulting dataset can be found [here](data/attributes.csv), and the script used for scraping the data can be found [here](src/scrape_data.py).
Please note that it appears that the website's SSL certificate has expired.

The dataset includes various quantitative attributes that control a character's in-game physics.
A more in-depth description for each of these attributes can be found on the main page of the dashboard.
The attribute descriptions provided on the dashboard are based on the descriptions which can be found on [SmashWiki](https://www.ssbwiki.com/).

## Contributing

Interested in contributing? Check out the [contributing guidelines](CONTRIBUTING.md). Please note that this project is released with a [Code of Conduct](CODE_OF_CONDUCT.md). By contributing to this project, you agree to abide by its terms.

## License

The Super Smash Dashboard was created by Jakob Thoms. It is licensed under the terms of the MIT license.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)  
