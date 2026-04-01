import os
import sys
import json

# Add Source_Code to path
sys.path.append(r'C:\Users\HP\OneDrive\Desktop\Job_Hunt\Source_Code')

try:
    import database
    import scout_agent
    import asset_factory
    print("? Imports successful.")
except ImportError as e:
    print(f"? Import failed: {e}")
    sys.exit(1)

# Test 1: Database
test_job = {"title": "Test Engineer", "url": "https://example.com/test", "status": "pending_review"}
if database.add_job(test_job):
    print("? Database: Successfully added test job.")
else:
    print("?? Database: Test job already exists (OK).")

# Test 2: Preferences Access
try:
    prefs = scout_agent.get_preferences()
    print(f"? Master Assets: Preferences loaded. Roles: {prefs.get('role_types')}")
except Exception as e:
    print(f"? Master Assets: Failed to load preferences: {e}")

# Test 3: Asset Factory Initialization
try:
    factory = asset_factory.AssetFactory()
    context = factory.get_master_context()
    if len(context) > 100:
        print("? Asset Factory: Master context loaded successfully.")
    else:
        print("?? Asset Factory: Master context is very short. Did you fill the files?")
except Exception as e:
    print(f"? Asset Factory: Initialization failed: {e}")

print("\n--- Verification Complete ---")
