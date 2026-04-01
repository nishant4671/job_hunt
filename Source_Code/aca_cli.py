"""
ACA-CLI: The High-Speed "Factory" version of your Job-Hunt app.
Purpose: Handles massive batches of jobs from the terminal for maximum speed.
"""

import argparse # Library to handle terminal commands (like --scout)
import scout_agent # Our job hunter
import asset_factory # Our AI brain
import database # Our local memory
import form_filler # Our browser automation
import os

def main():
    # 1. Setup the "Command Menu" for the terminal
    parser = argparse.ArgumentParser(description="ACA High-Speed Terminal Agent")
    parser.add_argument("--scout", action="store_true", help="Find new jobs")
    parser.add_argument("--tailor", action="store_true", help="AI-read JDs and write letters for all pending jobs")
    parser.add_argument("--apply", action="store_true", help="Launch the semi-auto browser for ready jobs")
    parser.add_argument("--limit", type=int, default=10, help="How many jobs to handle at once")
    
    args = parser.parse_args() # This reads what you typed in the terminal

    # --- PHASE 1: THE SCOUT ---
    if args.scout:
        print(f"[?] Scouting for new leads...")
        # Calls our hunter script to find fresh links
        count = scout_agent.search_jobs(role="Internship", domain="AI", job_type="Internship")
        print(f"[!] Success: Found {count} new jobs and added them to database.json")

    # --- PHASE 2: THE FACTORY (The Boring Part) ---
    if args.tailor:
        print(f"[?] Starting Batch Tailoring...")
        db = database.load_db()
        # Find jobs that haven't been worked on yet
        pending = [j for j in db['jobs'] if j.get('status') == 'pending_review'][:args.limit]
        
        factory = asset_factory.AssetFactory(persona="Technical")
        for job in pending:
            print(f" -> Reading JD and Writing for: {job['title']}")
            # The AI reads the site, maps your projects, and writes the .txt and .pdf
            factory.generate_tailored_assets(job['title'], job['url'], job.get('source', 'Company'))
            # Update status so we don't do it twice
            database.update_job_status(job['url'], 'form_ready')
        print(f"[!] Done: {len(pending)} sets of assets are ready in your Applications folder.")

    # --- PHASE 3: THE EXECUTOR (The Semi-Auto Part) ---
    if args.apply:
        print(f"[?] Starting Semi-Auto Application Loop...")
        db = database.load_db()
        # Find jobs where the AI has finished its work
        ready = [j for j in db['jobs'] if j.get('status') == 'form_ready'][:args.limit]
        
        # User info for the forms
        user_info = {'full_name': 'Nishant', 'email': 'NISHANTHKR4671@gmail.com', 'phone': '+91 8468002278'}
        resume_path = r"C:\Users\HP\OneDrive\Desktop\Job_Hunt\Master_Assets\resume.pdf"

        for job in ready:
            print(f"\n[!] OPENING BROWSER FOR: {job['title']}")
            print(f"[!] Link: {job['url']}")
            # Path to the AI-written letter
            folder = f"{job.get('source', 'Company')}_{job['title']}".replace(' ', '_').replace('/', '_')
            cl_path = os.path.join(r"C:\Users\HP\OneDrive\Desktop\Job_Hunt\Applications", folder, "Cover_Letter.txt")
            
            # This opens the browser, types your info, and WAITS for you.
            form_filler.fill_form(job['url'], user_info, resume_path, cl_path)
            # Once you close the browser, we mark it as applied
            database.update_job_status(job['url'], 'applied')
            print(f"[+] Finished with {job['title']}. Moving to next...")

if __name__ == "__main__":
    main()
