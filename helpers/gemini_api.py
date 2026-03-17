import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

model = genai.GenerativeModel('gemini-2.0-flash')

def query_gemini(prompt: str) -> dict:
    try:
        response = model.generate_content(prompt)
        return eval(response.text)  # Use safer parsing in production
    except Exception as e:
        print(f"Gemini API error: {e}")
        return {
            "evaluation_summary": "Gemini API failed.",
            "categories": {
                "Communication Skills": "Not available.",
                "Technical Fit": "Not available.",
                "Soft Skills": "Not available.",
                "Work Experience Relevance": "Not available."
            }
        }
