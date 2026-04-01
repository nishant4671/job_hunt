"""
CLI USAGE GUIDE: How to use the ACA Terminal "Factory"
Purpose: Explains the 3-step terminal flow for high-volume job hunting.
"""

# ?? STEP 1: FIND NEW JOBS (THE SCOUT)
Run this command to find new leads:
```bash
python Source_Code/aca_cli.py --scout
```
*   **What happens?** The robot checks RSS feeds and Google to find 10-20 new job links and adds them to `database.json`.

# ?? STEP 2: WRITE 50 LETTERS AT ONCE (THE FACTORY)
Run this command to have the AI "read" and "write" for your jobs:
```bash
python Source_Code/aca_cli.py --tailor --limit 50
```
*   **What happens?** The robot opens every link, reads the job ad, and writes a perfect cover letter matching your projects. **This is the huge time saver.**
*   **Drawback?** You don't see the letters until they are finished. You can check them in the `Applications/` folder later.

# ?? STEP 3: APPLY SEMI-AUTO (THE EXECUTOR)
Run this command to actually fill the forms:
```bash
python Source_Code/aca_cli.py --apply --limit 10
```
*   **What happens?** 
    1.  The robot opens a **visible** browser window.
    2.  It types your **Name, Email, and Phone**.
    3.  It **uploads your Resume**.
    4.  It **STOPs**.
    5.  **YOU** solve any "Captcha" or "Click the buses" puzzles.
    6.  **YOU** read the "Why us?" box (AI usually fills it, but you should check).
    7.  **YOU** click "Submit."
    8.  When you close the browser, the robot **automatically opens the next job**.

---

### **SUMMARY: Why use this?**
-   **Dashboard:** Good for 1-5 very special, high-priority jobs.
-   **CLI:** Good for 50+ "bulk" applications where you want to move as fast as possible.
