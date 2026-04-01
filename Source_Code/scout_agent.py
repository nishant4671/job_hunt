"""
SCOUT AGENT: The discovery engine of ACA.
Purpose: Hunts for job opportunities via RSS feeds and targeted URL guessing on platforms like Greenhouse and Lever.
"""

import json
import os
import requests
from datetime import datetime
import database # Import the local database controller
import xml.etree.ElementTree as ET # Used for parsing XML RSS feeds
from playwright.sync_api import sync_playwright # For deep-scanning via browser

def search_jobs(role="Internship", domain="Software", location="Remote", job_type="Internship", deep_scan=False):
    """
    Core search function to find new job leads.
    """
    found_count = 0 # Counter for new, unique jobs found
    today = datetime.now().strftime("%Y-%m-%d") # Format date for record-keeping
    
    # --- TIER 1: RSS FEEDS (High Reliability & Minimal Cost) ---
    # We use RSS feeds from known job boards to get structured data instantly.
    feeds = [
        "https://weworkremotely.com/categories/remote-programming-jobs.rss",
        "https://remotive.com/api/remote-jobs/feed"
    ]

    for feed_url in feeds:
        try:
            # Request the XML content from the feed provider
            response = requests.get(feed_url, timeout=10)
            if response.status_code == 200:
                # Parse the XML structure
                root = ET.fromstring(response.content)
                for item in root.findall('.//item'):
                    title = item.find('title').text
                    # Check if the job matches our role OR domain OR job_type
                    search_matches = [role.lower(), domain.lower(), job_type.lower()]
                    if any(term in title.lower() for term in search_matches):
                        # Construct a standardized job dictionary
                        job = {
                            "title": title,
                            "url": item.find('link').text,
                            "source": "RSS_Feed",
                            "status": "pending_review", 
                            "date_found": today,
                            "job_type": job_type # Store metadata for UI coloring
                        }
                        # database.add_job returns True if it's a new, unique URL
                        if database.add_job(job):
                            found_count += 1
        except Exception as e:
            print(f"RSS Feed Error ({feed_url}): {e}")
            continue

    # --- TIER 2: URL GUESSING (Direct-to-Source) ---
    # Many companies use Greenhouse/Lever. We "guess" their board URL to find jobs before they hit job boards.
    companies = ["stripe", "airbnb", "uber", "datadog", "dropbox", "asana", "figma", "github", "zoom", "spotify", "slack", "discord"]
    for company in companies:
        for platform in ["boards.greenhouse.io", "jobs.lever.co"]:
            url = f"https://{platform}/{company}"
            # Construct job object for the whole board
            job = {
                "title": f"{company.capitalize()} Board", 
                "url": url, 
                "source": "Guesser", 
                "status": "pending_review", 
                "date_found": today,
                "job_type": job_type # Tag with current search intent
            }
            if database.add_job(job):
                found_count += 1

    # --- TIER 3: DEEP SCAN (Google Dorking via Browser) ---
    # If deep_scan is enabled, we use a real browser to search Google for direct career links.
    if deep_scan:
        try:
            with sync_playwright() as p:
                # Launch a hidden browser
                browser = p.chromium.launch(headless=True)
                page = browser.new_page()
                # Construct a Google "Dork" query to find application pages specifically
                query = f"{role} {domain} {job_type} {location} site:greenhouse.io OR site:lever.co"
                page.goto(f"https://www.google.com/search?q={query}")
                
                # Extract all anchor tags (links) from the search results
                links = page.query_selector_all('a')
                for link in links:
                    href = link.get_attribute('href')
                    # If the link points to a known career platform, we log it
                    if href and ("greenhouse.io" in href or "lever.co" in href):
                        job = {
                            "title": f"{domain} {job_type} Role", 
                            "url": href, 
                            "source": "DeepScan", 
                            "status": "pending_review", 
                            "date_found": today,
                            "job_type": job_type
                        }
                        if database.add_job(job): 
                            found_count += 1
                browser.close()
        except Exception as e:
            print(f"DeepScan Error: {e}")

    return found_count # Return total new leads discovered

if __name__ == "__main__":
    # Test execution when run directly
    print(f"Found {search_jobs()} new jobs.")
