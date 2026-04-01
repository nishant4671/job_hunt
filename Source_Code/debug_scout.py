import requests
import xml.etree.ElementTree as ET
import os
import sys

# Add Source_Code to path
sys.path.append(r'C:\Users\HP\OneDrive\Desktop\Job_Hunt\Source_Code')
import database

url = "https://weworkremotely.com/categories/remote-programming-jobs.rss"
print(f"Testing Feed: {url}")
try:
    r = requests.get(url, timeout=10)
    print(f"Status: {r.status_code}")
    root = ET.fromstring(r.content)
    items = root.findall('.//item')
    print(f"Found {len(items)} items in RSS.")
    for i in items[:3]:
        print(f"- {i.find('title').text}")
except Exception as e:
    print(f"Error: {e}")
