"""
MASTER DIAGNOSTIC MASTER (The Complete Diagnostic Report)
Purpose: Runs all tests and gives a Green/Red status for each module.
"""

import subprocess
import os

def run_test(file_name):
    try:
        # Run the specific test file in its own process
        print(f"\n--- RUNNING: {file_name} ---")
        result = subprocess.run(['python', file_name], capture_output=True, text=True)
        print(result.stdout)
        if result.returncode != 0:
            print(f"[ERROR] Test failed with: {result.stderr}")
            return False
        return True
    except Exception as e:
        print(f"[FATAL ERROR] Could not run {file_name}: {e}")
        return False

def main():
    print("="*40)
    print("?? ACA SYSTEM MASTER DIAGNOSTIC")
    print("="*40)
    
    # Run the tests in sequence
    test_files = [
        "tests/test_ai_brain.py",
        "tests/test_browser_scraper.py",
        "tests/test_db_persistence.py"
    ]
    
    overall_status = True
    for test in test_files:
        if not run_test(test):
            overall_status = False
            
    print("\n" + "="*40)
    if overall_status:
        print("?? FINAL STATUS: SYSTEM HEALTHY (100% GREEN)")
        print("Summary: AI, Browser, and DB are all working properly.")
    else:
        print("?? FINAL STATUS: SYSTEM FAULTY (RED DETECTED)")
        print("Summary: One or more modules are failing. Check the logs above.")
    print("="*40)

if __name__ == "__main__":
    main()
