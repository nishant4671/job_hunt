"""
ACA-CLI: The High-Speed "Factory" version of your Job-Hunt app.
Enhanced Version: Now supports interactive review and custom search filters.
"""

import argparse # Library to handle terminal commands
import scout_agent # Our job hunter
import asset_factory # Our AI brain
import database # Our local memory
import form_filler # Our browser automation
import os

def main():
    # 1. Setup the "Command Menu"
    parser = argparse.ArgumentParser(description="ACA High-Speed Terminal Agent")
    parser.add_argument("--scout", action="store_true", help="Find new jobs")
    parser.add_argument("--review", action="store_true", help="Interactively review found jobs")
    parser.add_argument("--tailor", action="store_true", help="AI-read JDs and write letters")
    parser.add_argument("--apply", action="store_true", help="Launch semi-auto browser")
    
    # 2. Add Search Preference Arguments (Can be passed via terminal)
    parser.add_argument("--role", type=str, default="Internship", help="Target role (e.g. Intern, Engineer)")
    parser.add_argument("--domain", type=str, default="AI", help="Tech stack (e.g. AI, Backend)")
    parser.add_argument("--type", type=str, default="Internship", help="Full-Time, Part-Time, Internship")
    parser.add_argument("--loc", type=str, default="Remote", help="Job location")
    parser.add_argument("--limit", type=int, default=10, help="Batch limit")
    
    args = parser.parse_args()

    # --- PHASE 1: THE SCOUT (Hunting with your Preferences) ---
    if args.scout:
        print(f"\n[?] Scouting for: {args.role} | {args.domain} | {args.type} | {args.loc}")
        # Now uses the variables you passed in the command!
        count = scout_agent.search_jobs(
            role=args.role, 
            domain=args.domain, 
            location=args.loc, 
            job_type=args.type
        )
        print(f"[!] Success: Found {count} new leads! Run --review to see them.")

    # --- PHASE 1.5: THE REVIEW (Look at what the Robot found) ---
    if args.review:
        db = database.load_db()
        pending = [j for j in db['jobs'] if j.get('status') == 'pending_review']
        
        if not pending:
            print("[!] No new jobs to review. Run --scout first!")
            return

        print(f"\n--- INTERACTIVE REVIEW ({len(pending)} jobs) ---")
        for job in pending:
            print(f"\n[JOB]: {job['title']} @ {job.get('source', 'Unknown')}")
            print(f"[URL]: {job['url']}")
            
            # Ask the human what to do
            choice = input("Action -> [A]pprove, [I]gnore, [S]kip, [Q]uit: ").lower()
            
            if choice == 'a':
                database.update_job_status(job['url'], 'approved')
                print(" [+] Approved for tailoring!")
            elif choice == 'i':
                database.update_job_status(job['url'], 'ignored')
                print(" [-] Ignored.")
            elif choice == 'q':
                break
            else:
                print(" [ ] Skipped for now.")

    # --- PHASE 2: THE FACTORY (Tailoring Only Approved Jobs) ---
    if args.tailor:
        db = database.load_db()
        # Only work on jobs YOU approved in the --review phase
        approved = [j for j in db['jobs'] if j.get('status') == 'approved'][:args.limit]
        
        if not approved:
            print("[!] No approved jobs ready. Run --review first!")
            return

        print(f"\n[?] Tailoring {len(approved)} jobs...")
        factory = asset_factory.AssetFactory(persona="Technical")
        for job in approved:
            print(f" -> Processing: {job['title']}")
            factory.generate_tailored_assets(job['title'], job['url'], job.get('source', 'Company'))
            database.update_job_status(job['url'], 'form_ready')
        print("[!] All assets ready!")

    # --- PHASE 3: THE EXECUTOR (Applying) ---
    if args.apply:
        db = database.load_db()
        ready = [j for j in db['jobs'] if j.get('status') == 'form_ready'][:args.limit]
        
        user_info = {'full_name': 'Nishant', 'email': 'NISHANTHKR4671@gmail.com', 'phone': '+91 8468002278'}
        resume_path = r"C:\Users\HP\OneDrive\Desktop\Job_Hunt\Master_Assets\resume.pdf"

        for job in ready:
            print(f"\n[!] APPLYING: {job['title']}")
            folder = f"{job.get('source', 'Company')}_{job['title']}".replace(' ', '_').replace('/', '_')
            cl_path = os.path.join(r"C:\Users\HP\OneDrive\Desktop\Job_Hunt\Applications", folder, "Cover_Letter.txt")
            
            form_filler.fill_form(job['url'], user_info, resume_path, cl_path)
            database.update_job_status(job['url'], 'applied')
            print(f"[+] Done with {job['title']}.")

if __name__ == "__main__":
    main()
