# Project: Autonomous Career Agent (ACA)
# Agent Identity: Gemini-CLI

## 1. Project Objective
Build a lightweight, zero-cost AI agent that automates the internship/job application lifecycle (Discovery -> Asset Generation -> Form Filling -> Tracking).

## 2. Technical Architecture
- **AI Brain:** Google Gemini API (Free Tier).
- **Automation:** Python + Playwright (Browser Control).
- **UI/Dashboard:** Streamlit (Local Web App).
- **Storage:** Local Filesystem (Folders) + Google Sheets API (Tracking).
- **Database:** Source_Code/database.json for local state tracking.

## 3. Key Components
- **Scout Agent:** Google Dorking for job leads.
- **Asset Factory:** Generates tailored PDF resumes/cover letters.
- **Form-Filler:** Auto-fills Greenhouse/Lever/LinkedIn forms.
- **Vault:** Organizes applications in Applications/YYYY-MM-DD_Company_Role/.

## 4. Current Status (LAST ENDPOINT)
- **Phase 0: Environment Setup** (COMPLETED)
- **Phase 1: Knowledge Acquisition** (IN PROGRESS)
  - NEXT STEP: User to place Resume.pdf and Master Context files in Master_Assets/.
  - NEXT STEP: Run Source_Code/parser.py to initialize the "Brain".

## 5. Security & Stealth
- No direct LinkedIn scraping (Prevents bans).
- Human-in-the-Loop for final submission.
