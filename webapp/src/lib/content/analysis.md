# Analysis

The analysis focusses on answering the research question, if there are patterns in the review data that can be detected.  
The webscraper collects data three times a day and stores it in a csv file. To analyse this data we created a python script that is automatically run by github actions when there is new data pushed to the main branch of the repository. This means whenever the scraper adds data to the csv file, the analyzation script is being executed.

This project focussed on restaurants in the city Bochum, which appear in the google maps search for the query "Restaurant Bochum". We collected data for 119 restaurants and focus on the maximum change of reviews in a single measurement. As the following sankey plot shows, 111 restaurants have new reviews and 8 restaurants did not get new reviews during the time of the experiment.  
TODO input the plot Starving/data/graphs/general/restaurants_with_new_reviews.html

The plot shows that 57 restaurants had a maximum of one new review from one measurement to the next. It is also not uncommon for restaurants to have 2-4 new reviews with 45 restaurants, but it is less common for restaurants to get more than 5 on a single measurement. Only 5 restaurants got 5-9 new reviews and 4 restaurants got 10-14 new reviews maximum in a single measurement.

When we consider the deletions, we can look at two cases. For one, google maps now provides a notice, when a restaurant deleted reviews because of defamation. The second case is the deletions that were measured in this experiment. With measured deletions we focus on the total amount of deleted reviews in the time of our experiment.  
A caveat with the measured deletions and new reviews is, that it can not be detected if inbetween measurements the same amount of reviews was deleted and added, thus only the total change at the time of the measurement can be tracked and visualized.  
The following two plots show the distribution of restaurants that have a deletion notice by google maps and the distribution of restaurants with measured deletions. 
TODO input the plot Starving/data/graphs/general/gridplot-notice-deletions.html
TODO input the plot Starving/data/graphs/general/gridplot-tracked-deletions.html

The plot with the distribution of restaurants with a deletion notice visualizes, that most restaurants do not have a notice. The note from google maps differentiates between amounts of deletions, for example it classifies from 2-5, 6-10 and so on. The class with the most deletions we observed in our dataset is 101-150 deletions. In later parts of this chapter we will specifically analyze this particular case.  
The plot with the measured deletions also takes into account ther reviews that were deleted by users. Furthermore we could also track if only one review was deleted. Thus the plot shows, that only 52 out of the 119 restaurants did not have any deleted reviews. There were 31 restaurants with one deleted review and 29 restaurants with two to five deleted reviews. The second class is noticably more common than the notice shows, which suggests that users activvely deleted their reviews. 

The script, apart from the graphs shown before, mainly creates graphs of restaurants, which show the changement of stars over the collected time. Furthermore it only creates the graphs for restaurants that have changes that are of interest to a user.  
Changes of interest are defined as two cases. For one any deletions of reviews. The second case is, when a detected increase of reviews from one data collection to the next (the delta), is higher than the defined threshold of 4. Thus, only restaurants with a maximum delta of 5 or higher are selected as interesting.  
This threshold is chosen, because experiments with the restaurants in Bochum show, that of the 119 restaurants there are 58 that have a maximum delta of 1, and a further 44 restaurants with a maximum delta of 2-4. Only 9 restaurants have a delta of 5 and higher. These are seen as interesting, because it might indicate the use of bots to increase the rating of the restaurant if these increases to not fit into the ongoing increase of reviews.

The restaurant with the highest increase of restaurants from one point of measurement to the next is the "Taste-Trip Restaurant Bochum Innenstadt". The plot of the total amount of reviews is shown in the followng plot:
TODO input the plot Starving/data/graphs/interesting_total_count/Taste-Trip Restaurant Bochum Innenstadt, Bochum .html

As seen in the graphs the high delta is in the timespan of May 28th to May 31st. This is a long time between measurements, because it was in the beginning of the project, where the scraper was optimized. Nevertheless, this example is interesting, because it seems to be a new restaurant with only 16 reviews at the start of our experiment. As of the 15th of July, the restaurant has a total of 58 reviews. A search on the restaurants website shows, that it was opened May 18th (https://taste-trip.de/ueber-uns.html), which confirms, that this restaurant was opened shortly before the start of the restaurant.  
The high increase of new reviews seems plausible, since the restaurant is new and the increase is consistent and it does not show an increase that would suggest the use of bots.

The following graph shows another restaurant with a high delta of 11 for the 5-star reviews of the "L'Osteria Bochum". The graph shows the changement of reviews, the delta, from one measurement to the next.

TODO input the plot Starving/data/graphs/interesting_differences/L'Osteria Bochum Husemann Karree, Bochum Viktoriastraße 14 a.html

It can be seen, that there are multiple spikes for the  5-star reviews of 5 up to 11 new reviews. Furthermore it can be seen, that there was a deletion of 5 star reviews on the 14th and 15th of July. In these two days there was a deletion of 3 5-star reviews. Restaurants with deletions due to defamation receive a notice on google maps. In this case no notice appearde, thus it can be claimed, that the reviews were deleted by the users.  
These high fluctuations alone might seem significant, but if they are put into perspective, it can be seen that they only constitute a change of up to 1.2%. The following plot shows the total number of reviews for the given restaurant.
TODO input the plot Starving/data/graphs/interesting_total_count/L'Osteria Bochum Husemann Karree, Bochum Viktoriastraße 14 a.html

When the 5-star graph is selected, it can be clearly seen, that the revies increased from for example 854 to 865 in the 2nd of June. This means, that the restaurant has many reviews and a changement of 11 new reviews is plausible and does not indicate any manipulation.

Another case of interesting increase of reviews is the restaurant "YUMINI" for their 5-star reviews. The following plot of the delta shows a big spike of 10 new reviews for the 5-star reviews. 

TODO input the plot Starving/data/graphs/interesting_differences/YUMINI, Bochum Viktoriastraße 43-45.html

The restaurant has 1422 5-star reviews on the 20th June 2026. With this in mind the change of 10 reviews is less than 1%. Between the 28th of May and the 15th of July the restaurant received 18 new 5 star reviews, 3 new 4-star reviews and 3 new 1-star reviews. In this context an increase of 10 reviews in one day might be indicating towards foul-play, but this short timespan of measurements is not enough to make any conclusions. With the presumption of innocence we would not indicate this as usage of bots. A potential user on the search for a place to eat can make their own conlcusions and decide if this increase seems legitimate or not.

In Germany it is possible for restaurant owners to delete reviews due to defamation. shortly after the start of this project, google maps introduced a notice which indicates if a restaurant has deleted reviews due to defamation.  
Only 15 of the 119 restaurants have this notice. In our detection system any deletion is detected, this includes user deletions. Again th focus lies on the maximum delta for deletions from one measurement to the next.  
Two restaurants clearly stand out, one having 20 deletions in one measurement step and the other having 75 deletions.


We first consider the restaurant with 20 deletions, "Trattoria Momo". The plot of the deltas for this restaurant shows normal activity for the restaurant with a spike for 1-star and 2-star reviews.

TODO input the plot Starving/data/graphs/interesting_differences/Trattoria Momo, Bochum .html

The graphs show that overall 39 reviews were deleted, after which the restaurant received the notice "21 to 50 reviews removed due to defamation complaints". This deletion increased the average stars from 4.64 to 4.69 stars, which would have raised it by 0.1 shown on google maps.  
This alone is not sufficient to claim that the reason was not defamation, thus no claim of foul-play can be made in this case.

The restaurant with most deletions is the "Fiege's Stammhaus" which deleted 119 3-star reviews within two days. This can be seen in the two plots for this restaurant showing the delta and the total amount of reviews.
TODO input the plot Starving/data/graphs/interesting_total_count/Fiege's Stammhaus, Bochum Bongardstraße 23.html
TODO input the plot Starving/data/graphs/interesting_differences/Fiege's Stammhaus, Bochum Bongardstraße 23.html

This deletion of reviews has changed the average from 4.49 to 4.64 stars by deleting 9% of its reviews. Between the 28th of May and the 15th of July the restaurant no new reviews for 1 and 2 stars, 1 new 3-star review, 2 new 4-star reviews and 9 new 5-star reviews. At the end of our measureements the restaurant has 774 5-star reviews, 415 4-star reviews, 6 3-star reviews and no 2-star and 1-star reviews.  
Since it is not known what the content of the deleted reviews was, it is not possible to ethically judge if the deletions were justified. Thus the presumption of innocence still holds and it is up to an enduser to make their own conclusion.

To conclude the analysis, we showed different restaurants that show anomalies for the increase and deletion of reviews. It is not possible to clearly label any of the cases as foul-play, thus it is up to an end-user to draw their own conclusions and this project provides a tool to help in the endeavour of finding a suitible restaurant to eat.  
We also raise the point that with a longer time it might be possible to recognize patterns that are not apparent within a timespan of about 2 months.







