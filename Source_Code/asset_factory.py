"""
ASSET FACTORY: The AI engine of ACA.
Purpose: Uses Google Gemini (or local Ollama) to scrape job descriptions and generate tailored PDF assets.
Connections: Called by dashboard.py to synthesize custom application documents.
"""

import os
import json
import requests
from bs4 import BeautifulSoup # Used for scraping the Job Description (JD)
import google.generativeai as genai # Brain of the system (Gemini)
from fpdf import FPDF # Used to generate PDFs from AI-generated text
from dotenv import load_dotenv # Loads GOOGLE_API_KEY from .env file

# Load environment variables
load_dotenv()

class AssetFactory:
    def __init__(self, persona="Professional"):
        # Base path for our Master Assets
        self.assets_path = os.path.join(os.path.dirname(__file__), '..', 'Master_Assets')
        self.persona = persona
        self.api_key = os.getenv('GOOGLE_API_KEY')
        genai.configure(api_key=self.api_key)
        
        # Stability fallback list for Gemini Free Tier
        self.model_names = ['gemini-1.5-flash', 'gemini-1.5-pro']
        self.current_model = None

    def _get_model(self):
        """
        Dynamically selects a working AI model based on quota/availability.
        If all Gemini models fail, it returns "ollama" for local processing.
        """
        for name in self.model_names:
            try:
                model = genai.GenerativeModel(name)
                # Test call to ensure we're not being throttled by quota (429)
                model.generate_content("ping", request_options={"timeout": 5}) 
                self.current_model = model
                return model
            except Exception:
                continue
        
        # FINAL FALLBACK: Local Ollama (Assumes Ollama is running on localhost)
        return "ollama"

    def fetch_jd(self, url):
        """
        Scrapes the raw text from the Job URL.
        Optimized for Greenhouse and Lever board layouts.
        """
        try:
            headers = {'User-Agent': 'Mozilla/5.0'}
            # Fetch HTML content with timeout to prevent hanging
            response = requests.get(url, headers=headers, timeout=10)
            if response.status_code != 200:
                return "HTTP Error: Could not fetch JD text from site."
            
            # Parse HTML into searchable soup
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Platform-Specific Scraping Logic
            if "greenhouse.io" in url:
                # Greenhouse usually puts JD in the #content div
                content = soup.find('div', id='content')
                return content.get_text(separator='\n') if content else "JD div not found on Greenhouse page."
            elif "lever.co" in url:
                # Lever uses section page-centered for its job content
                content = soup.find('div', class_='section page-centered')
                return content.get_text(separator='\n') if content else "JD section not found on Lever page."
            
            # Fallback: Just return the text snippet if it's an unsupported platform
            return soup.get_text()[:1000]
        except Exception as e:
            return f"Scrape Error: {e}"

    def generate_tailored_assets(self, job_title, url, company_name, selected_projects=None):
        """
        Core logic: Mapping your projects to the JD requirements using LLMs.
        """
        # 1. Scrape the target JD text
        jd_text = self.fetch_jd(url)
        
        # 2. Gather User Context (PersonalInfo + Selected Projects)
        context = ""
        personal_info_path = os.path.join(self.assets_path, 'personal_info.txt')
        if os.path.exists(personal_info_path):
            with open(personal_info_path, 'r', encoding='utf-8') as f:
                context += f.read() + "\n\n"
        
        # 3. Dynamic Project Mapping
        projects_path = os.path.join(self.assets_path, 'projects_summary.txt')
        if os.path.exists(projects_path):
            with open(projects_path, 'r', encoding='utf-8') as f:
                all_projects = f.read()
                if selected_projects:
                    # Filter the summary to only include projects chosen in the Sidebar
                    filtered_projects = ""
                    for p_name in selected_projects:
                        if p_name in all_projects:
                            start_marker = f"--- {p_name} ---"
                            parts = all_projects.split(start_marker)
                            if len(parts) > 1:
                                filtered_projects += start_marker + parts[1].split('---')[0]
                    context += filtered_projects
                else:
                    context += all_projects

        # Style guides for AI tone
        persona_guide = {
            "Professional": "Use formal, corporate language. Focus on ROI, efficiency, and measurable impact.",
            "Startup": "Be enthusiastic, bold, and agile. Emphasize fast learning and 'scrappiness'.",
            "Technical": "Be concise and tech-heavy. Focus on specific architecture and technical 'how'."
        }

        # 4. Construct the AI Prompt (This is where the magic happens)
        prompt = f"""
        Persona Style: {persona_guide.get(self.persona)}
        
        CANDIDATE PROFILE & PROJECTS:
        {context}
        
        TARGET ROLE: {job_title} at {company_name}
        TARGET JOB DESCRIPTION:
        {jd_text[:2000]} # Truncate for token efficiency
        
        TASK: Write an ATS-optimized cover letter (max 300 words).
        Strategically map my projects to their requirements. Use specific keywords from the JD text.
        """

        # 5. Execute AI Generation
        model = self._get_model()
        if model == "ollama":
            # API call to local Ollama instance
            try:
                import requests as ollama_req
                res = ollama_req.post("http://localhost:11434/api/generate", 
                                      json={"model": "llama3", "prompt": prompt, "stream": False})
                cl_text = res.json().get('response', 'Ollama failed to respond.')
            except Exception:
                cl_text = "ERROR: Gemini quota hit and Ollama is not running. Please check local server."
        else:
            # Call Google Gemini API
            response = model.generate_content(prompt)
            cl_text = response.text

        # 6. Folder Management
        # Create a specific folder for this application to keep files organized
        safe_name = f"{company_name}_{job_title}".replace(' ', '_').replace('/', '_')
        app_folder = os.path.join(os.path.dirname(__file__), '..', 'Applications', safe_name)
        os.makedirs(app_folder, exist_ok=True)
        
        # Save the raw text for the Dashboard Live Editor
        with open(os.path.join(app_folder, 'Cover_Letter.txt'), 'w', encoding='utf-8') as f:
            f.write(cl_text)

        return cl_text, app_folder

    def save_pdf(self, cl_text, app_folder):
        """
        Converts edited cover letter text into a finalized PDF.
        """
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=11)
        # Handle non-Latin-1 characters common in AI text
        safe_text = cl_text.encode('latin-1', 'replace').decode('latin-1')
        pdf.multi_cell(0, 7, safe_text)
        pdf_path = os.path.join(app_folder, 'Cover_Letter_Final.pdf')
        pdf.output(pdf_path)
        return pdf_path
