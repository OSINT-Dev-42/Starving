from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeoutError
import time
import re
import random
import pathlib as path
from datetime import datetime
import pandas as pd

PATH = path.Path(__file__).parents[1]

RAW_PATH = PATH / "data" / "raw"

LIST_PATH = PATH / "data" / "list"

class WebCrawler:
    # ----------------constants ----------------
    __BASE_URL = r"https://www.google.com/maps?hl=en"
    # --------------------------------------------

    def __init__(self):
        """
        Creates chromium ``browser`` with ``context`` and ``page`` tab.
        Note that browsers do not allow launching multiple instances with the same User Data Directory.\n
            - !simultaneous WebCrawler instances are not supported
        """
        # setup browser
        self.pw = sync_playwright().start()
        self.browser = self.pw.firefox
        self.context = self.browser.launch(headless=False, proxy={"server": "socks5://127.0.0.1:9050"})
        self.page = self.context.new_page()

    def visit_maps(self): 
        """
        Visit https://www.google.com/maps?hl=en and reject any cookie banners.
        """
        self.page.goto(self.__BASE_URL) # visit english website
        time.sleep(random.randrange(10, 20, 5)*0.1)
        try:
            button = self.page.get_by_role("button", name="Reject all") # search for reject all button
            button.click(timeout=3000)
        except PlaywrightTimeoutError:
            print("Timeout while trying to skip cookie banner. No cookie banner found.")
        time.sleep(random.randrange(20, 50, 5)*0.1) # insert random delay

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
        
        time.sleep(random.randrange(20, 50, 5)*0.1) # insert random delay
        
        try:
            search = self.page.get_by_role("tab", name=re.compile(r"Reviews")) # select reviews tab
            search.click(timeout=10000)
        except PlaywrightTimeoutError:
            print("Timeout while trying to navigate to reviews tab.")
        time.sleep(random.randrange(20, 50, 5)*0.1) # insert random delay

    def get_star_metadata(self) -> dict:
        """
        parse hmtl content for:\n
        - star count
        - defamation removal notice\n
        ``returns`` metada
        """
        # collect stars count
        stars = ['5 stars', '4 stars', '3 stars', '2 stars', '1 stars']
        metadata = {'5 stars': None,
                      '4 stars': None,
                      '3 stars': None,
                      '2 stars': None,
                      '1 stars': None,
                      'notice': None}
        for rating in stars:
            raw_rating = self.page.get_by_role("img", name=rating).first.get_attribute("aria-label")  # regex match rating count
            # print(f"raw_rating: {raw_rating}")
            metadata[rating] = [re.findall(r'\d*\,?\d+', raw_rating)[1]] # skip star num an extract only the review count
        
        # collect diffamation removal count
        notices = ["One review removed due to a defamation complaint.",
                   "Two to five reviews removed due to defamation complaints.",
                   "Six to ten reviews removed due to defamation complaints.",
                   "11 to 20 reviews removed due to defamation complaints.",
                   "21 to 50 reviews removed due to defamation complaints.",
                   "51 to 100 reviews removed due to defamation complaints.",
                   "101 to 150 reviews removed due to defamation complaints.",
                   "151 to 200 reviews removed due to defamation complaints.",
                   "201 to 250 reviews removed due to defamation complaints.",
                   "Over 250 reviews removed due to defamation complaints.",]

        for notice in notices:
            try:
                metadata["notice"] = [self.page.get_by_text(notice).first.text_content(timeout=200)]
            except PlaywrightTimeoutError:
                continue
        return metadata

    def close(self):
        """
        Ends playwright session.
        """
        self.page.close()
        self.context.close()
        self.pw.stop()


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
    restaurants = pd.read_csv(LIST_PATH / "restaurants.csv")
    
    for rows in restaurants.itertuples():
        result = {}
        query = f"{rows.name}, {rows.address}"
        print(f"Query: {query}")
        result['name'] = query
        result["date"] = datetime.today().strftime(r'%Y-%m-%d')

        crawl = WebCrawler() # init playwright

        crawl.visit_maps() # visit google maps
        crawl.search(query)

        metadata = crawl.get_star_metadata()
        result.update(metadata)
        print(f"Result: {result}")
        crawl.close()
        write_to_csv(result, "firstcrawl.csv", RAW_PATH)
        time.sleep(random.randrange(20, 50, 5)*0.1) # insert random delay
  


    
