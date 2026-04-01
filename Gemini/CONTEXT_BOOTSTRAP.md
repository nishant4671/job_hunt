# ?? AI CONTEXT BOOTSTRAP: READ THIS FIRST
**MANDATE:** Any AI assistant entering this workspace MUST read this file before performing any task.

## ?? PROJECT OVERVIEW
- **Name:** Autonomous Career Agent (ACA)
- **User:** Nishant (https://github.com/nishant4671)
- **Status:** Active Development (Version 1.0)
- **Goal:** Automate Internship/Job hunt (Scout -> Tailor -> Apply -> Track).

## ??? LAST KNOWN STATE (March 30, 2026)
1. **Scout Agent:** Successfully implemented with RSS + URL Guessing. 58+ jobs in queue.
2. **Asset Factory:** Integrated with Gemini API and Playwright JD Scraper. Generates custom PDFs.
3. **Dashboard:** Streamlit UI is live with:
   - Resume Upload
   - AI Persona Switching (Professional/Startup/Technical)
   - Desktop Notifications (win10toast)
   - Power Search & Filtering
4. **Tracking:** Local CSV Logging (Applications_Log.csv) is active.

## ??? DIRECTORY MAP
- /Source_Code: Python logic (scout, factory, dashboard, database).
- /Master_Assets: User's raw data (Resume, GitHub summaries, Personal info).
- /Applications: Generated custom folders per job.
- /Gemini: Professional documentation and this bootstrap.

## ?? NEXT STEPS FOR THE NEXT SESSION
- Enhance the 'Form-Filler' to handle more complex multi-page applications.
- Add a "Job Scraper" to pull full text from LinkedIn/Indeed.
- Integrate the Google Sheets API for cloud tracking.
