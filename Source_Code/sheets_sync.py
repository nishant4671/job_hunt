"""
SHEETS SYNC: The ledger of ACA.
Purpose: Logs every finalized application into a CSV file for long-term tracking.
Connections: Called by dashboard.py after a user clicks 'Finalize PDF'.
"""

import pandas as pd # Used for efficient data logging and CSV manipulation
import os
from datetime import datetime

# Define the central application ledger path
CSV_FILE = r'C:\Users\HP\OneDrive\Desktop\Job_Hunt\Applications_Log.csv'

def log_application(company, title, url):
    """
    Appends a new application record to the local CSV database.
    Inputs: Company Name, Job Title, and Application URL.
    """
    # 1. Create a standardized dictionary for the record
    new_entry = {
        "Date": datetime.now().strftime("%Y-%m-%d"),
        "Company": company,
        "Role": title,
        "URL": url,
        "Status": "Applied/Assets Generated"
    }
    
    # 2. Convert dictionary to a single-row DataFrame
    df = pd.DataFrame([new_entry])
    
    # 3. Handle File Creation or Appending
    if not os.path.exists(CSV_FILE):
        # Create a new file with headers if it doesn't exist
        df.to_csv(CSV_FILE, index=False)
    else:
        # Append to existing file without repeating headers
        df.to_csv(CSV_FILE, mode='a', header=False, index=False)
    
    # Visual confirmation in terminal for the developer
    print(f"Logged application to: {CSV_FILE}")
