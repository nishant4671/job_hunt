# ?? ARCHITECTURAL GUIDE: WORK OF EACH FILE

## 1. CORE SYSTEM OVERVIEW
The **Autonomous Career Agent (ACA)** is a modular Python suite designed to automate the job application lifecycle. It connects four main layers: **Discovery**, **Synthesis**, **Automation**, and **Persistence**.

---

## 2. FILE-BY-FILE BREAKDOWN

### ?? `scout_agent.py` (The Hunter)
- **Role**: Discovers new job opportunities.
- **How it works**:
    - **RSS Scraper**: Reads structured XML from remote job boards (Remotive, WeWorkRemotely).
    - **URL Guesser**: Directly checks common career board formats (Greenhouse/Lever) for top tech companies.
    - **Deep Scan**: Uses Playwright to perform Google "Dorking" (advanced search) for direct application links.
- **Connection**: Sends discovered URLs to `database.py` for unique storage.

### ?? `asset_factory.py` (The Brain)
- **Role**: AI-driven document generation.
- **How it works**:
    - **Smart Scraper**: Uses `BeautifulSoup` to read the real Job Description (JD) text from the URL.
    - **Gemini Orchestrator**: Sends your projects (from `projects_summary.txt`) and the JD to Google Gemini.
    - **Mapping Logic**: Tells the AI to specifically match your skills to the keywords in the JD.
    - **Fallback**: Automatically switches to **Ollama (Llama3)** if Gemini's quota is hit.
- **Connection**: Creates specific folders in `Applications/` and generates the tailored `Cover_Letter.pdf`.

### ?? `dashboard.py` (The Control Center)
- **Role**: The Streamlit-based User Interface.
- **How it works**:
    - **State Management**: Uses `st.session_state` to track your current "Live Edits".
    - **Human-in-the-Loop**: Allows you to review and fix the AI's "first draft" before it becomes a PDF.
    - **Filtering**: Shows jobs based on "Job Type" (Internship vs Full-Time) and status.
- **Connection**: This is the "Main" file. It calls all other scripts based on your button clicks.

### ?? `form_filler.py` (The Executor)
- **Role**: Semi-automated browser control via Playwright.
- **How it works**:
    - **DOM Injection**: Finds common HTML fields (name, email, phone) and auto-types your data.
    - **Human-Augmented**: Opens a **visible** browser window (non-headless) and waits for you to click the final "Submit" button.
- **Connection**: Triggered by the Dashboard once assets are finalized.

### ?? `database.py` (The Memory)
- **Role**: Local JSON state management.
- **How it works**:
    - **JSON Storage**: Reads and writes to `database.json`.
    - **Duplicate Guard**: Ensures you never apply to the same URL twice by checking every new link against existing records.

### ?? `sheets_sync.py` & `notifier.py` (The Ledger & Alerts)
- **Role**: Tracking and communication.
- **How it works**:
    - **CSV Logging**: Appends every final application to `Applications_Log.csv` for your records.
    - **Toast/Telegram**: Sends real-time alerts so you don't miss a hot new role.

---

## 3. DATA FLOW ARCHITECTURE
1.  **Discovery**: `scout_agent` -> `database.json`.
2.  **Selection**: User selects job in `dashboard.py`.
3.  **Synthesis**: `dashboard.py` -> `asset_factory` -> `Gemini` -> `Applications/` (PDF).
4.  **Automation**: `dashboard.py` -> `form_filler` -> `Browser` (User Submits).
5.  **Audit**: `dashboard.py` -> `sheets_sync` -> `Applications_Log.csv`.
