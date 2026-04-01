"""
DIAGNOSTIC TEST: AI BRAIN
Purpose: Verifies Gemini API quota and Ollama local availability.
"""

import sys
import os
# Add the Source_Code folder to the path so we can import our modules
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'Source_Code'))
import asset_factory

def test_ai_connection():
    print("[?] Checking AI Brain Status...")
    factory = asset_factory.AssetFactory(persona="Technical")
    
    # 1. Test Model Selection
    model = factory._get_model()
    if model == "ollama":
        print("[!] GEMINI QUOTA HIT (or failed). Switched to Local Ollama.")
    else:
        print(f"[+] GEMINI API SUCCESS: Using {model.model_name}")
    
    # 2. Test Tailoring (Sample Run)
    try:
        print("[?] Testing Sample Tailoring...")
        cl_text, folder = factory.generate_tailored_assets(
            "AI Engineer", 
            "https://jobs.lever.co/demo", 
            "TestCorp"
        )
        if len(cl_text) > 50:
            print("[+] ASSET GENERATION SUCCESS: AI wrote a valid cover letter.")
        else:
            print("[x] ASSET GENERATION FAILED: AI output was too short or empty.")
    except Exception as e:
        print(f"[x] BRAIN FAULTY: {e}")

if __name__ == "__main__":
    test_ai_connection()
