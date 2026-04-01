"""
DASHBOARD: The Human-in-the-Loop Control Center of ACA.
Purpose: Provides a Streamlit UI to manage the job queue, tailor AI-generated assets, and launch browser automation.
Connections: Orchestrates scout_agent, asset_factory, database, and form_filler.
"""

import streamlit as st # UI Framework
import os
import json
import database # Local database controller (database.py)
import scout_agent # Job search logic (scout_agent.py)
import asset_factory # AI asset generation (asset_factory.py)
import sheets_sync # Application logging (sheets_sync.py)
import form_filler # Browser automation (form_filler.py)
import notifier # Notifications (notifier.py)
from datetime import datetime

# --- SYSTEM PATHS ---
# Master Assets are our "Source of Truth" for personal branding.
MASTER_ASSETS = r'C:\Users\HP\OneDrive\Desktop\Job_Hunt\Master_Assets'
RESUME_PATH = os.path.join(MASTER_ASSETS, 'Resume.pdf')
PROJECTS_SUMMARY = os.path.join(MASTER_ASSETS, 'projects_summary.txt')

def update_job_status(url, new_status):
    """
    Helper function to update a job's status directly in database.json.
    Inputs: Job URL (unique ID) and the new status string.
    """
    db = database.load_db()
    for job in db['jobs']:
        if job['url'] == url:
            job['status'] = new_status
    database.save_db(db)

def get_project_list():
    """
    Helper function to parse project names from projects_summary.txt.
    Parses lines starting with '--- ' to populate the Sidebar Multi-Select.
    """
    if not os.path.exists(PROJECTS_SUMMARY):
        return []
    with open(PROJECTS_SUMMARY, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        # Clean up the markers to get raw project names
        return [l.replace('--- ', '').replace(' ---', '').strip() for l in lines if l.startswith('--- ')]

# --- STREAMLIT PAGE CONFIGURATION ---
st.set_page_config(page_title="ACA Power Dashboard", page_icon="??", layout="wide")
st.title("?? Autonomous Career Agent (ACA)")

# --- SESSION STATE INITIALIZATION ---
# cl_buffer stores the cover letter text temporarily so it doesn't disappear on UI refresh.
if 'cl_buffer' not in st.session_state:
    st.session_state.cl_buffer = {}

# --- SIDEBAR: SETTINGS & TOOLS ---
st.sidebar.header("??? Global Settings")
# Select the "Persona" or tone the AI should use for writing.
u_persona = st.sidebar.selectbox("AI Writing Style", ["Professional", "Startup", "Technical"])
u_notify = st.sidebar.checkbox("Enable Notifications", value=True)

st.sidebar.divider()
st.sidebar.header("?? Persona: Featured Projects")
# Allow the user to pick which projects match the current application "vibe".
all_available_projects = get_project_list()
selected_projects = st.sidebar.multiselect(
    "Select projects to showcase in AI documents", 
    all_available_projects, 
    default=all_available_projects[:2] if all_available_projects else []
)

st.sidebar.divider()
st.sidebar.header("?? Master Resume")
# Check for a resume and allow a quick update/upload.
if os.path.exists(RESUME_PATH):
    st.sidebar.success("? Master Resume Found")
else:
    st.sidebar.warning("? No Resume Found")
uploaded_file = st.sidebar.file_uploader("Replace Master PDF", type=["pdf"])
if uploaded_file:
    with open(RESUME_PATH, "wb") as f:
        f.write(uploaded_file.getbuffer())
    st.sidebar.success("Updated!")

st.sidebar.divider()
st.sidebar.header("?? Power Scout Search")
# Inputs for the Scout Agent (scout_agent.py).
u_role = st.sidebar.text_input("Role (Title)", "Internship")
u_domain = st.sidebar.text_input("Domain (Tech Stack)", "AI")
# Added: Job Type selection for filtering results.
u_job_type = st.sidebar.selectbox("Job Type", ["Internship", "Full-Time", "Part-Time", "Contract"])
u_loc = st.sidebar.text_input("Location", "Remote")
u_deep = st.sidebar.checkbox("Deep Scan (Google Search)")

if st.sidebar.button("?? Run Power Scout"):
    with st.spinner(f"Scouting for {u_job_type} leads..."):
        # Launch the Scout and notify the user of results.
        count = scout_agent.search_jobs(u_role, u_domain, u_loc, u_job_type, u_deep)
        if u_notify and count > 0:
            notifier.send_notification(f"Found {count} new {u_job_type} positions!")
        st.success(f"Found {count} new jobs added to queue!")
        st.rerun() # Refresh the UI to show new jobs

st.sidebar.divider()
search_query = st.sidebar.text_input("?? Filter Local Queue", "")

# --- MAIN CONTENT: THE JOB QUEUE ---
db = database.load_db()
# Only show jobs that are pending action (Review, Assets, Form).
all_pending = [j for j in db['jobs'] if j.get('status') in ['pending_review', 'assets_ready', 'form_ready', 'applied']]
# Filter by the search query in the sidebar.
jobs = [j for j in all_pending if search_query.lower() in j['title'].lower()]

st.subheader(f"Active Job Queue ({len(jobs)} leads)")

# Iterate through each job and build a visual card (Expander).
for job in jobs:
    # Color-coded badge for Job Type (Internship vs Full-Time).
    j_type = job.get('job_type', 'Unknown')
    badge_color = ":green" if "Intern" in j_type else ":blue" if "Full" in j_type else ":orange"
    
    with st.expander(f"[{badge_color}[{j_type}]] {job['title']} | Status: {job.get('status', 'Pending')}", expanded=False):
        col1, col2, col3, col4 = st.columns([2, 1, 1, 1])
        
        with col1:
            st.write(f"Source: {job.get('source', 'Web')}")
            st.caption(f"URL: {job['url']}")
        
        # --- ACTION: ASSET GENERATION ---
        with col2:
            if st.button("? Tailor Assets", key=f"t_{job['url']}"):
                factory = asset_factory.AssetFactory(persona=u_persona)
                with st.spinner("Scraping JD & Mapping Projects..."):
                    # Launch AI pipeline: Scrape JD -> Prompt Gemini -> Generate Text.
                    cl_text, folder = factory.generate_tailored_assets(job['title'], job['url'], job.get('source', 'Company'), selected_projects)
                    st.session_state.cl_buffer[job['url']] = cl_text
                    update_job_status(job['url'], 'assets_ready')
                    st.rerun()

        # --- ACTION: VAULT EDITOR ---
        if job.get('status') in ['assets_ready', 'form_ready'] or job['url'] in st.session_state.cl_buffer:
            st.divider()
            st.subheader("?? The Vault: Live Edit & Finalize")
            current_cl = st.session_state.cl_buffer.get(job['url'], "")
            
            # Fallback: If buffer lost on refresh, try loading from saved .txt file.
            if not current_cl:
                app_folder = os.path.join(os.path.dirname(__file__), '..', 'Applications', f"{job.get('source', 'Company')}_{job['title']}".replace(' ', '_'))
                cl_path = os.path.join(app_folder, 'Cover_Letter.txt')
                if os.path.exists(cl_path):
                    with open(cl_path, 'r', encoding='utf-8') as f:
                        current_cl = f.read()
                        st.session_state.cl_buffer[job['url']] = current_cl

            # Allow the human (Nishant) to review and edit the AI's "first draft".
            edited_cl = st.text_area("Interactive AI Cover Letter", value=current_cl, height=300, key=f"edit_{job['url']}")
            
            sc1, sc2 = st.columns(2)
            with sc1:
                if st.button("?? Save & Finalize PDF", key=f"f_{job['url']}"):
                    factory = asset_factory.AssetFactory(persona=u_persona)
                    # Convert the text into a clean PDF.
                    app_folder = os.path.join(os.path.dirname(__file__), '..', 'Applications', f"{job.get('source', 'Company')}_{job['title']}".replace(' ', '_'))
                    pdf_path = factory.save_pdf(edited_cl, app_folder)
                    
                    # Log the finalized application into the CSV ledger.
                    sheets_sync.log_application(job.get('source', 'Company'), job['title'], job['url'])
                    update_job_status(job['url'], 'form_ready')
                    st.success(f"PDF Saved! Ready for Submission.")
                    st.rerun()
            
            # --- ACTION: BROWSER AUTOMATION ---
            with sc2:
                if job.get('status') == 'form_ready':
                    if st.button("?? Launch Form-Filler", key=f"fill_{job['url']}"):
                        st.info("Launching browser... Watch your screen for the automation!")
                        
                        # Load user info from personal_info.txt (Simplified parsing).
                        info_path = os.path.join(MASTER_ASSETS, 'personal_info.txt')
                        user_info = {'full_name': 'Nishant', 'email': 'NISHANTHKR4671@gmail.com', 'phone': '+91 8468002278'}
                        
                        app_folder = os.path.join(os.path.dirname(__file__), '..', 'Applications', f"{job.get('source', 'Company')}_{job['title']}".replace(' ', '_'))
                        cl_path = os.path.join(app_folder, 'Cover_Letter.txt')
                        
                        # Trigger Playwright (form_filler.py) in non-headless mode.
                        form_filler.fill_form(job['url'], user_info, RESUME_PATH, cl_path)
                        update_job_status(job['url'], 'applied')
                        st.success("Form pre-filled. Review and click 'Submit' manually!")
                        st.rerun()

        with col3:
            if st.button("??? Ignore", key=f"ign_{job['url']}"):
                update_job_status(job['url'], 'ignored')
                st.rerun()
        
        with col4:
            st.link_button("?? Open Site", job['url'])
