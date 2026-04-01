"""
SCOUT AGENT (ELITE): The Multi-Niche Discovery Engine.
Now specifically tuned for AI, Healthcare, FinTech, and Cybersecurity.
"""

import json
import os
import requests
from datetime import datetime
import database
import xml.etree.ElementTree as ET
from playwright.sync_api import sync_playwright

def search_jobs(role="Internship", domain="AI", location="Remote", job_type="Internship"):
    found_count = 0
    today = datetime.now().strftime("%Y-%m-%d")
    
    # --- 1. THE NICHE KEYWORD ENGINE ---
    # We now pull from your specific strengths
    niches = ["AI", "Healthcare", "FinTech", "Cybersecurity", "Full Stack"]
    search_queries = [f"{role} {n}" for n in niches]
    
    # --- 2. EXPANDED RSS FEED LIST ---
    feeds = [
        "https://weworkremotely.com/categories/remote-programming-jobs.rss",
        "https://hnrss.org/jobs",
        "https://remoteok.com/remote-jobs.rss",
        "https://www.workingnomads.com/jobs/feed"
    ]

    for feed_url in feeds:
        try:
            response = requests.get(feed_url, timeout=10)
            if response.status_code == 200:
                root = ET.fromstring(response.content)
                for item in root.findall('.//item'):
                    title = item.find('title').text
                    # Match any of your niches or the search role
                    if any(term.lower() in title.lower() for term in (search_queries + [domain])):
                        job = {
                            "title": title,
                            "url": item.find('link').text,
                            "source": f"RSS_{feed_url.split('/')[2]}",
                            "status": "pending_review", 
                            "date_found": today,
                            "job_type": job_type
                        }
                        if database.add_job(job): found_count += 1
        except: continue

    # --- 3. THE "ELITE 100" COMPANY BOARD CHECK ---
    # Adding heavy hitters in FinTech and Healthcare
    companies = [
        # FINTECH
        "plaid", "brex", "ramp", "stripe", "robinhood", "coinbase", "affirm", "chime", "revolut", "wise", "klarna", "marqeta",
        # HEALTHCARE
        "oscar", "cloverhealth", "flatiron", "zocdoc", "headspace", "ro", "hims", "omada", "tempus", "teladoc", "modernhealth",
        # AI & CORE TECH
        "openai", "anthropic", "tesla", "spacex", "palantir", "figma", "github", "vercel", "notion", "databricks", "snowflake"
    ]
    
    for company in companies:
        for platform in ["boards.greenhouse.io", "jobs.lever.co"]:
            url = f"https://{platform}/{company}"
            job = {"title": f"{company.capitalize()} Board", "url": url, "source": "Elite_Guesser", "status": "pending_review", "date_found": today, "job_type": job_type}
            if database.add_job(job): found_count += 1

    # --- 4. ADVANCED DEEP SCAN (The "Nishant" Special) ---
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            for q in search_queries:
                page.goto(f"https://www.google.com/search?q={q} site:greenhouse.io OR site:lever.co after:2026-03-01")
                links = page.query_selector_all('a')
                for link in links:
                    href = link.get_attribute('href')
                    if href and ("greenhouse.io" in href or "lever.co" in href):
                        job = {"title": f"{q} Role", "url": href, "source": "Niche_DeepScan", "status": "pending_review", "date_found": today, "job_type": job_type}
                        if database.add_job(job): found_count += 1
            browser.close()
    except: pass

    return found_count
