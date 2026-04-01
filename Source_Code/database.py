"""
DATABASE CONTROLLER: The persistence layer of ACA.
Purpose: Manages the local JSON-based state (database.json) to track found jobs and their application status.
Connections: Used by scout_agent.py to add jobs and dashboard.py to read/update them.
"""

import json
import os

# Define the local storage path relative to this script's location
DB_FILE = os.path.join(os.path.dirname(__file__), 'database.json')

def load_db():
    """
    Reads the JSON database from disk.
    If the file doesn't exist, initializes an empty structure.
    """
    if not os.path.exists(DB_FILE):
        return {"jobs": []} # Default JSON structure
    
    with open(DB_FILE, 'r', encoding='utf-8') as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            # Handle empty or corrupted files by returning the default structure
            return {"jobs": []}

def save_db(data):
    """
    Writes the updated JSON structure back to disk with human-readable indentation.
    """
    with open(DB_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4) # Indent=4 makes the JSON file readable in a text editor

def add_job(job_data):
    """
    Adds a new job to the database if the URL is not already present (duplicate prevention).
    Input: job_data dictionary (title, url, source, status, date_found, job_type)
    Returns: True if job was added, False if it was a duplicate.
    """
    db = load_db()
    
    # --- DUPLICATE CHECK ---
    # We use the URL as a unique identifier because companies often post similar titles.
    if any(job['url'] == job_data['url'] for job in db['jobs']):
        return False # Job already exists, ignore it
    
    # --- PERSISTENCE ---
    # Append the new job data to the global list and save
    db['jobs'].append(job_data)
    save_db(db)
    return True

def get_jobs_by_status(status):
    """
    Filters the database by status (e.g., 'pending_review', 'assets_ready', 'applied').
    Used primarily by the Streamlit Dashboard for selective display.
    """
    db = load_db()
    return [j for j in db['jobs'] if j.get('status') == status]
