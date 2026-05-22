import re
from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeoutError
import time



def setup_playwright(pw):
    # configuration
    config = {
        "accept_downloads": False, # do not download stuff
        "locale": "en-US", # emulate us english language settings
        "screen": {"width": 1920, "height": 1080}, # emulate full hd screen
        "viewport": {"width": 1920, "height": 1080}, # emulate full hd viewport
        "headless": False, # set true to not show browser window (invisible); set false to show browser window (visible)
        # TODO: set navigator.webdriver to false to bypass bot detection
        "args":  [
            # "--disable-blink-features=AutomationControlled", # navigator.webdriver = false
            "--proxy-server"
        ],
        "proxy" : {"server": "socks5://127.0.0.1:9050"}
    }
    # browser and context
    browser = pw.firefox
    context = browser.launch_persistent_context("", **config)
    # create page
    page = context.new_page()
    return context, page

if __name__ == "__main__":
    with sync_playwright() as pw:
        context, page = setup_playwright(pw)
        page.goto(r"https://check.torproject.org/")
        print(f"Playwright:{page.title()}")
        time.sleep(10)
        page.close()
        context.close()