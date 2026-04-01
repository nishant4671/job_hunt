# ?? ACA WORKFLOW LOGIC

1. **TRIGGER:** User clicks 'Scout' in the Dashboard.
2. **SCOUT:** scout_agent.py fetches RSS feeds and probes company boards. Hits are added to database.json.
3. **NOTIFICATION:** 
otifier.py sends a Windows Toast alert.
4. **REVIEW:** User filters the Dashboard and finds a role.
5. **TAILOR:** User clicks 'Tailor Assets'. 
   - sset_factory.py scrapes the JD using Playwright.
   - Gemini API generates a custom Cover Letter.
   - sheets_sync.py logs the intent to apply.
6. **APPLY:** User clicks 'Open' to visit the site; orm_filler.py is ready for pre-filling standard data.
