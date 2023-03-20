# The Super Smash Dashboard - Proposal

## Motivation and Purpose

The target audience of this dashboard are Super Smash Bros. players who are interested in exploring the various attributes that control a character's in-game physics. This dashboard will be a useful resource for quickly and easily visualizing differences among the many characters in the Super Smash Bros. cast. The visualizations presented will make it easy to spot outlier characters who are particularly strong or weak in a given attrribute. Further, competive Super Smash Bros. players will likely find this dashboard useful for the purpose of studying character data. 

Although this dashboard has a fairly niche target audience, it is a much-needed addition to existing Super Smash Bros. resources. Character attribute data is not directly accessible within the game itself, and although there are some websites which provide tables of the data (e.g. [ultimateframedata.com](https://ultimateframedata.com/stats)), I could not find a service that allowed the user to visualize the data.

## Description of Data

The dataset includes various quantitative attributes that control a character's in-game physics, such a character's weight, a character's maximum movement speed (in various forms, e.g. walking, running, and airborne), and a character's airborne acceleration. A more in-depth description for each of these attributes can be found on the main page of the dashboard.

The data is not directly accessible within the game itself, and I was unable to find a nice data file (e.g. `.csv` or `.json`) with the dataset. The best I could find were websites with the data in tabular format (i.e. `HTML` tables). As a result, I had to create the dataset myself by scraping data from one of these websites. I used [kuroganehammer.com](http://kuroganehammer.com/Ultimate/) for this since the tables on this site are in a fairly consistent format, which makes scraping data easier. The resulting dataset can be found [here](data/attributes.csv), and the script used for scraping the data can be found [here](src/scrape_data.py).

## Usage Scenarios

Jakob is an avid Super Smash Bros player who wants to visualize the differences and similarities between the physical attributes of various characters available in the game. Jakob has been unable to do so previously due to a lack of existing resources for this purpose. 

Jakob wants to be able to [choose which attributes to visualize], and he wants to be able to [choose how to visualize those attributes]. He wants to be able to [quickly see which characters have the highest/lowest value in any given attribute], and also to be able to [see how any given attribute relates to any other attribute]. He also wants the visualizations to include tooltips so that he is able to [determine the exact values of a character's attributes] by simply hovering his mouse over the relevant section of the visualization. 

Jakob will use this dashboard to make interesting insights about the effect of a character's attributes on that character's playstyle. For example, he will notice that on a scatter plot of `Base Air Acceleration` vs. `Max Air Acceleration` his two favourite characters to play happen to form a 2-point cluster, and he will conclude that those two character's unique combination of those two attributes may contribute to his preference for playing as them.

