import re
from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeoutError
import time
import subprocess


def setup_playwright(pw):
    # configuration
    browser = pw.firefox
    context = browser.launch(
        headless=False, proxy={"server": "socks5://127.0.0.1:9050"}
    )
    page = context.new_page()
    return context, page

if __name__ == "__main__":
    for i in range(5):
        with sync_playwright() as pw:
            context, page = setup_playwright(pw)
            page.goto(r"https://check.torproject.org/")
            print(f"Playwright:{page.title()}")
            time.sleep(2)
            page.close()
            context.close()
            pw.stop()
        subprocess.run(["sudo", "service", "tor", "restart"])