# Analysis

The analysis focusses on answering the research question, if there are patterns in the review data that can be detected.

The webscraper collects data three times a day and stores it in a csv file. To analyse this data we created a python script that is automatically run by github actions when there is new data pushed to the main branch of the repository. This means whenever the scraper adds data to the csv file the analysation script is being executed.

The script mainly creates graphs of restaurants, which show the changement of stars over the collected time. Furthermore it only creates the graphs for restaurants that have changes that are of interest to a user. Changes of interest are defined as two cases. For one any deletions of reviews. The second case is when a detected increase of reviews from one data collection to the next (the delta), is higher than the defined threshold of 1.  
For the project a high increase in reviews at a single time is seen as interesting, because it might indicate the use of bots to increase the rating of the restaurant. For an enduser to inspect the  
