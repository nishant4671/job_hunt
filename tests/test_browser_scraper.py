"""
DIAGNOSTIC TEST: BROWSER & SCRAPER
Purpose: Verifies if Playwright can open a browser and if BeautifulSoup can read the web.
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'Source_Code'))
import asset_factory
from playwright.sync_api import sync_playwright

def test_browser_core():
    print("[?] Checking Playwright (Browser Engine)...")
    try:
        with sync_playwright() as p:
            # We use a very light browser check
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            page.goto("https://www.google.com")
            print(f"[+] PLAYWRIGHT SUCCESS: Browser reached Google. Title: {page.title()}")
            browser.close()
    except Exception as e:
        print(f"[x] PLAYWRIGHT FAULTY: {e}")

def test_jd_scraper():
    print("[?] Checking JD Scraper (The Eyes)...")
    factory = asset_factory.AssetFactory()
    # Test on a known public Lever board
    test_url = "https://jobs.lever.co/demo" 
    jd_text = factory.fetch_jd(test_url)
    if "lever" in jd_text.lower() or "demo" in jd_text.lower():
        print("[+] SCRAPER SUCCESS: Successfully read the Job Description from the URL.")
    else:
        print("[x] SCRAPER FAULTY: Could not extract clean text from the test URL.")

if __name__ == "__main__":
    test_browser_core()
    test_jd_scraper()
