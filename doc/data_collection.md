# Data Collection & Wrangling

<!-- ## Bullet Point Overview
- web scraper is based on playwright
- Tor-proxy 
- structure of webscraper:
    - launches browser
    - visits google maps
        - rejects any cookie banners
    - enters restaurant in search bar
        - selects reviews tab
    - parses html code for number of reviews for each star category
    - parses html code for any defamation notes
    - closes playwright instance
- scraping procedure: `src/web_scraper.py`
    - we run the web scraper three times a day
    1. reads restaurant from restaurant list
    2. prepares dict entry with name and datetime of recording
    3. inits webscraper
    4. visits google maps
    5. searches restaurant 
    6. extracts data from html code
    7. adds data to dict and writes it to csv
- error handling:
    - every action performed by Playwright takes place within a try block to prevent crashes
        - in most cases a blocked ip address by google is the culprit
            - we assign a new ip address to our scraper by assigning the tor instance a new identity via `src/proxy/rotate_tor_ip.py`
            - if this does not suffice we repeat this process 15 times in case of other anomalies. 
            - final solution is skipping the current restaurant for the current run
    - every action is buffered by inserting a random delay to mimic user input
    - we keep the same ip address only for a fixed interval to prevent bot detection as well -->

## Intro
We start of with discussing our data collection procedure. If we search the web, we will find various ways to access review data from [Google Maps](https://www.google.com/maps?hl=en). For example, there are various providers that offer web scraping as a service like [OpenWeb Ninja](https://www.openwebninja.com/api/google-maps-reviews) or [Outscraper](https://outscraper.com/google-maps-reviews-api/). Google itself also offers a solution in the form of the [Google Maps API](https://mapsplatform.google.com/lp/maps-apis/ ).  

However, none of the solutions really meet our requirements. There are two main points to consider. Firstly, the free tiers would exhaust over our scraping duration. Secondly, we want to look at the reviews in a more granular manner, which is often not supported by the available APIs. In most cases, only the total number of reviews and the average rating are displayed. For this reason, and because [Google Maps](https://www.google.com/maps?hl=en) has an easy-to-use interface, we built our own web scraper to collect our data.  

The following section outlines our custom web scraper, which is tailored to our needs, and its data collection process.

## Web Scraper
The web scraper is based on [Playwright](https://playwright.dev/python/docs/api/class-playwright). [Playwright](https://playwright.dev/python/docs/api/class-playwright) is an open-source automation library for automating web browser interactions that provides an API for Python. Additionally we use the [Tor](https://www.torproject.org/?noredirect=1) proxy to hide our IP address.  

## Scraping Procedure
We run the web scraper three times a day to account for fluctuations in the number of stars. The scraper runs in a [Docker](https://www.docker.com/) container and automatically pushes the collected data to the repository, which triggers an update on our website. The following figure provides an overview of our web scraping procedure and instance process:  

1. A new instance of our web scraper is created for each restaurant that is scraped. It starts of with a general initialization of a headless [Firefox](https://www.firefox.com/de/) browser. The `socks5://127.0.0.1:9050` endpoint is configured as the proxy for the [Tor](https://www.torproject.org/?noredirect=1) daemon.

2. In the next step we call https://www.google.com/maps?hl=en. Since our geolocation is constantly changing due to IP rotation by the [Tor](https://www.torproject.org/?noredirect=1) proxy, we have to be prepared to end up in a country with strict cookie policies. Therefore, we implement a handler that rejects any cookie banners that might appear on the page. If no cookie banner appears, the error of not finding the cookie banner is caught and ignored.

3. Next, we reach the [Google Maps](https://www.google.com/maps?hl=en) landing page and enter the name and address of the current restaurant on our list. The address is an important part of our search query. Otherwise, there is a high chance that Google will recommend different restaurants with similar names instead of navigating us directly to the desired place.  
After that the web scraper locates the reviews tab and clicks on it.

4. Finally, the HTML source code contains all the information we need. We continue with parsing each star rating separately and end up with a string of the form 
    ```python
    "5 stars, 1,832 reviews" 
    ```
    In the next step we use regex pattern matching with `r"\d*\,?\d+"` to extract the number of ratings and reviews for each star category and then we select the latter result.
    ```python
    ["5", "1,832"] -> "1,832"
    ```
    [Google Maps](https://www.google.com/maps?hl=en) provides documentation on all possible diffamation notes that can be found in the reviews. We parse the HTML source code for these notes and store them in a list. If no diffamation notes are found, we store an empty list.  

5. After collecting all the data for a restaurant, we write it back to a CSV file and restart our web scraper for the next restaurant.

    | name | date | 5 stars | 4 stars | 3 stars | 2 stars | 1 star | notice |
    | --- | --- | --- | --- | --- | --- | --- | --- |
    | Sukhothai, Bochum Bochumer Str. 15 | 2026-06-27, 13:42 | 1,512 | 175 | 45 | 22 | 26 | |
    | Haus des Döners, Bochum Kortumstraße 45 | 2026-06-27, 13:42 | 282 | 63 | 42 | 4 | 11 | 21 to 50 reviews removed due to defamation complaints |
    | Das Syrische Restaurant, Bochum Kortumstraße 97-99 | 2026-06-27, 13:43 | 1,019 | 220 | 148 | 75 | 288 | |


We insert a random delay into every action to mimic user input. Additionally, we only use the same IP address for a fixed interval of two minutes to prevent bot detection. The IP rotation is implemented by assigning a new identity to the [Tor](https://www.torproject.org/?noredirect=1) instance via the `rotate_tor_ip.py` script.

![Steps performed by the web scraper](/doc/figures/BlockDiagram.svg)

## Error Handling
Every action performed by [Playwright](https://playwright.dev/python/docs/api/class-playwright) takes place within a try block to prevent crashes. In most cases, a blocked IP address by Google is the culprit. Therefore, if we cannot visit Google Maps, we rotate our IP address independently from our fixed interval.  
If this does not suffice we repeat this process 15 times in the event of other anomalies. As a last resort, we skip the current restaurant for the current run and continue with the next restaurant.