# Data Collection

## Bullet Point Overview
- web scraper is based on playwright
- Tor-proxy 
- structure of webscraper:
    - launches browser
    - visits google maps
        - rejects any cookie banners
    - enters restaurant in search bar
        - selects reviews tab
    - parses html code for number of reviews for each star category
    - parses html code for any diffamation notes
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
            - final solution is skipping the current restaurent for the current run
    - every action is buffered by inserting a random delay to mimic user input
    - we keep the same ip address only for a fixed interval to prevent bot detection aswell

## Intro
We start of with discussing the optimal data collection procedure. If we search the web, we will find various ways to access review data from [Google Maps](https://www.google.com/maps?hl=en). For example, there are various providers that offer web scraping as a service like [OpenWeb Ninja](https://www.openwebninja.com/api/google-maps-reviews) or [Outscraper](https://outscraper.com/google-maps-reviews-api/). Google itself also offers a solution in the form of the [Google Maps API](https://outscraper.com/google-maps-reviews-api/).  

However, none of the solutions really meet our requirements. There are two main points to consider. Firstly, the free tiers would exhaust over our scraping duration. Secondly, we want to look at the reviews in a more granular manner, which is often not supported by the available APIs. In most cases, only the total number of reviews and the average rating are displayed. For this reason, and because [Google Maps](https://www.google.com/maps?hl=en) has an easy-to-use interface, we built our own web scraper to collect our data.  

The following section outlines our custom web scraper, which is tailored to our needs, and its data collection process.

## Web Scraper
The web scraper is based on [Playwright](https://playwright.dev/python/docs/api/class-playwright). [Playwright](https://playwright.dev/python/docs/api/class-playwright) is an open-source automation library for automating web browser interactions that provides an API for Python. Additionally we use the [Tor](https://www.torproject.org/?noredirect=1) proxy to hide our IP address.  

![](/doc/figures/BlockDiagram.png)




## Scraping Procedure

## Error Handling