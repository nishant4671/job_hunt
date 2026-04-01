import os
import time
from playwright.sync_api import sync_playwright

def fill_form(job_url, user_info, resume_path, cl_path):
    with sync_playwright() as p:
        # Launching with headless=False so the user can see it
        browser = p.chromium.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()
        page.goto(job_url)
        
        print(f"Opening Job URL: {job_url}")
        
        try:
            # 1. Fill Name
            name_sel = 'input[name*="name"], input[id*="first_name"], input[placeholder*="Name"]'
            if page.query_selector(name_sel):
                page.fill(name_sel, user_info['full_name'])

            # 2. Fill Email
            email_sel = 'input[name*="email"], input[id*="email"]'
            if page.query_selector(email_sel):
                page.fill(email_sel, user_info['email'])

            # 3. Fill Phone
            phone_sel = 'input[name*="phone"], input[id*="phone"]'
            if page.query_selector(phone_sel):
                page.fill(phone_sel, user_info['phone'])

            # 4. Upload Resume
            resume_sel = 'input[type="file"][name*="resume"], input[type="file"][id*="resume"]'
            if page.query_selector(resume_sel):
                page.set_input_files(resume_sel, resume_path)

            # 5. Fill Cover Letter (if text box)
            cl_sel = 'textarea[name*="cover_letter"], textarea[id*="cover_letter"]'
            if page.query_selector(cl_sel) and os.path.exists(cl_path):
                with open(cl_path, 'r', encoding='utf-8') as f:
                    page.fill(cl_sel, f.read())

            print("\n[!] Form-Filler has injected the basics.")
            print("[!] Please complete any custom questions and click 'Submit' yourself.")
            print("[!] The browser will stay open for 10 minutes or until you close it manually.")
            
            # Keep browser open for user review
            for _ in range(60): # 10 minutes total
                if page.is_closed():
                    break
                time.sleep(10)
                
        except Exception as e:
            print(f"Error during form filling: {e}")
            # Even on error, keep browser open for user
            time.sleep(300)
        
        browser.close()

if __name__ == "__main__":
    # Test call
    test_user = {'full_name': 'Test User', 'email': 'test@example.com', 'phone': '1234567890'}
    fill_form("https://jobs.lever.co/demo", test_user, "", "")
