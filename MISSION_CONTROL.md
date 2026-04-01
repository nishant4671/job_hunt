# ?? MISSION CONTROL: Autonomous Career Agent (ACA)

## ?? MOTIVATION
Job hunting is a repetitive, high-volume task. This project aims to reclaim time by automating the 'Discovery -> Application' loop while maintaining 100% personalization to ensure high success rates.

## ?? CORE GOAL
An autonomous system that finds internships, tailors resumes/cover letters based on GitHub projects, fills forms, and tracks everything in a Google Sheet—all for ** cost**.

## ??? TECH STACK
- **Orchestrator:** Python 3.11+
- **Brain (LLM):** Google Gemini API (Free Tier)
- **Browser Automation:** Playwright (Stealth Mode)
- **UI Dashboard:** Streamlit
- **Document Engine:** PyPDF & FPDF
- **Persistence:** Local JSON (database.json) + Google Sheets API

## ??? SYSTEM ARCHITECTURE (MODULAR AGENTS)
1. **Scout Agent:** Performs Google Dorking for Job URLs.
2. **Asset Factory:** Synthesizes custom PDFs using Gemini + Master Assets.
3. **Form-Filler:** Navigates sites and auto-types user info.
4. **Tracker:** Updates the Google Sheet with application status.

## ?? DATA ENDPOINTS & FLOW
- **Input:** Master_Assets/ (Resume, GitHub Summaries, Personal Info).
- **Processing:** Source_Code/ (Python Logic).
- **Output:** Applications/ (Custom PDF sub-folders).
- **Finality:** database.json (Local State) -> Google Sheets (Global View).

## ?? CURRENT STATUS & ROADMAP
- [x] Phase 0: Project Structure & Documentation.
- [x] Phase 1: Knowledge Acquisition (GitHub Crawl, Assets Setup).
- [ ] Phase 2: The Scout Agent (Job Search Logic). **<-- CURRENT FOCUS**
- [x] Phase 3: The Asset Factory (PDF Generation Logic).
- [x] Phase 4: The Streamlit Dashboard (UI).
- [x] Phase 5: The Form-Filler (Playwright Integration).

## ?? HOW TO RESUME
1. Load MISSION_CONTROL.md to understand the goal.
2. Check Source_Code/database.json for applied jobs.
3. Verify .env has the GOOGLE_API_KEY.

