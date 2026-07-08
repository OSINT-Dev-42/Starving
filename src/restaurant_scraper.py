from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeoutError
import time
import re
import random
import pathlib as path
from datetime import datetime
import pandas as pd

PATH = path.Path()

LIST_PATH = PATH / "data" / "list"

class WebCrawler:
    # ----------------constants ----------------
    __BASE_URL = r"https://www.google.com/maps?hl=en"
    # --------------------------------------------

    def __init__(self):
        """
        Creates chromium ``browser`` with *persistent* ``context`` and ``page`` tab.
        Note that browsers do not allow launching multiple instances with the same User Data Directory.\n
            - !simultaneous WebCrawler instances are not supported
        """
        # context configuration
        config = {
            "accept_downloads": False, # do not download stuff
            "locale": "en-US", # emulate us english language settings
            "screen": {"width": 1920, "height": 1080}, # emulate full hd screen
            "viewport": {"width": 1920, "height": 1080}, # emulate full hd viewport
            "headless": False, # set true to not show browser window (invisible); set false to show browser window (visible)
            "args":  [
                # "--disable-blink-features=AutomationControlled" # navigator.webdriver = false
                "--proxy-server"
            ],
        "proxy" : {"server": "socks5://127.0.0.1:9050"}
        }
        # setup browser
        self.pw = sync_playwright().start()
        self.browser = self.pw.firefox
        self.context = self.browser.launch_persistent_context("",**config)
        self.page = self.context.new_page()

    def visit_maps(self): 
        """
        Visit https://www.google.com/maps?hl=en and consent to any cookie banners.
        """
        self.page.goto(self.__BASE_URL) # visit english website
        time.sleep(random.randrange(25, 50, 5)*0.1)
        try:
            button = self.page.get_by_role("button", name="Reject all") # search for accept all button
            button.click(timeout=5000)
        except PlaywrightTimeoutError:
            print("Timeout while trying to skip cookie banner.")
        # time.sleep(10)
        time.sleep(random.randrange(70, 100, 1)*0.1) # insert random delay

    def search(self, query: str):
        """
        Enter search ``query`` and navigate to review tab.
        """
        try:
            search = self.page.locator('input[name="q"]')
            search.fill(query) # input search query
            search.press("Enter")

        except PlaywrightTimeoutError:
            print("Timeout while trying to find input field.")
        # time.sleep(8)
        time.sleep(random.randrange(60, 100, 1)*0.1) # insert random delay
        
        
    def _parse_restaurant_data(self, text_content: str) -> dict:
        """
        Parse restaurant information from article text.
        Extracts: name, rating, review count, price range, cuisine, address
        """        
        # Split by common delimiters
        parts = text_content.split('·')
        
        if not parts:
            return None
        # Extract restaurant name (first element, before rating)
        name = parts[0].split('  ')[0]
        address = "Bochum"
        if parts[3].find("PM") == -1 and parts[3].find("AM") == -1 and (parts[3].find("Open") != -1 or parts[3].find("Close") != -1):
            address += parts[3]
        elif parts[2].find("PM") == -1 and parts[2].find("AM") == -1 and (parts[2].find("Open") != -1 or parts[2].find("Close") != -1):
            address += parts[2]
        else:
            print(parts)
        # delete Open or Closed from my string and only use the part before
        if "Open" in address:
            address = address.split("Open")[0]
        elif "Close" in address:
            address = address.split("Close")[0]
        # sometimes there are more informations directly after the number, this is to delete that
        address = re.split(r'(?<=\d)(?=[A-Z])', address)[0]
        # print(f"address: {address}")

        data = {
            'name': name,
            'address': address
            }
        return data
    
    
    def get_restaurant_results(self, limit: int=50):
        """
        First scroll until we see either limit-amount of entries or until the end of the list is reached.
        Then we save all entries into the results array and return it.
        """
        results = []
        
        try:
            self.page.wait_for_load_state("networkidle")
            self.page.wait_for_timeout(5000)
            
            feed_locator = self.page.locator('//div[@role="feed"]')
            # Scroll the feed to load more results
            article_count = 0
            while article_count < limit:
                articles = self.page.locator('//div[@role="article"]')
                article_count = articles.count()
                
                print(f"Currently found {article_count} articles, extracted {len(results)} results")
                # Check if we've reached the end of the list
                end_of_list = self.page.get_by_text("You've reached the end of the")
                if end_of_list.is_visible():
                    print("Reached end of list")
                    break
                    
                # Scroll the feed to load more results
                try:
                    feed_locator.scroll_into_view_if_needed()
                    # Scroll down within the feed
                    self.page.evaluate("""
                        () => {
                            const feed = document.querySelector('[role="feed"]');
                            if (feed) {
                                feed.scrollTop = feed.scrollHeight;
                            }
                        }
                    """)
                    time.sleep(4)  # Wait for new results to load

                except Exception as e:
                    print(f"Error scrolling: {e}")
                    break
                    
            # Extract data from each article
            for i in range(article_count):
                if len(results) >= limit:
                    break
                article = articles.nth(i)
                try:
                    # Extract text content
                    text_content = article.text_content()
                    # Parse the restaurant data
                    restaurant_data = self._parse_restaurant_data(text_content)
                    if restaurant_data and restaurant_data not in results:
                        results.append(restaurant_data)
            
                except Exception as e:
                    print(f"Error extracting article {i}: {e}")
            
            print(f"\nTotal results extracted: {len(results)}")
            return results
        except Exception as e:
            print(f"Error getting results: {e}")
            return results
            

    def close(self):
        """
        Ends playwright session.
        """
        self.page.close()
        self.context.close()


def write_to_csv(data, name, path):
    """
    Write ``data`` to csv with a given path ``path / name``.
    """
    output = path / name
    df = pd.DataFrame(data)
    # check if file exists
    if output.is_file():
        df.to_csv(output , mode="a", index=False, header=False)
    else:
        df.to_csv(output, mode="w", index=False)
        
        

if __name__ == "__main__":

    query = r"Restaurant Bochum"

    crawl1 = WebCrawler() # init playwright

    crawl1.visit_maps() # visit google maps
    crawl1.search(query)
    # crawl1.print_roles_with_details()
    results = crawl1.get_restaurant_results(limit=200)
    for restaurant_data in results:
        print(f"restaurant_data:\n{restaurant_data.get('name')}{restaurant_data.get('address')}")

    
    #time.sleep(10)
    crawl1.close()
    write_to_csv(results, "restaurants.csv", LIST_PATH)
  


    
