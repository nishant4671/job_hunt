"""
DIAGNOSTIC TEST: DATABASE & PERSISTENCE
Purpose: Verifies JSON storage and CSV logging.
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'Source_Code'))
import database
import sheets_sync

def test_json_db():
    print("[?] Checking JSON Database...")
    db = database.load_db()
    if isinstance(db, dict) and "jobs" in db:
        print(f"[+] DATABASE LOAD SUCCESS: Current database has {len(db['jobs'])} jobs stored.")
    else:
        print("[x] DATABASE FAULTY: Could not load valid JSON from database.json.")

def test_csv_log():
    print("[?] Checking CSV Ledger (The Audit Trail)...")
    try:
        sheets_sync.log_application("TEST_COMPANY", "TEST_ROLE", "http://test.com")
        print("[+] CSV LOG SUCCESS: Successfully added a record to Applications_Log.csv.")
    except Exception as e:
        print(f"[x] CSV LOG FAULTY: {e}")

if __name__ == "__main__":
    test_json_db()
    test_csv_log()
