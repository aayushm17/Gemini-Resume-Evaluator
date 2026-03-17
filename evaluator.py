import os
import google.generativeai as genai
from dotenv import load_dotenv
import json

# 1. FORCE THE PATH
basedir = os.path.dirname(os.path.abspath(__file__))
env_path = os.path.join(basedir, '.env')

# 2. LOAD
load_dotenv(dotenv_path=env_path, verbose=True)

# 3. RETRIEVE
api_key = os.getenv("GEMINI_API_KEY")

if api_key:
    # FIX: Add transport='rest' to resolve gRPC/timeout/shutdown errors on Windows
    genai.configure(api_key=api_key, transport='rest')
    # Use 1.5-flash as it is currently the most stable model across all tiers
    model = genai.GenerativeModel("gemini-2.5-flash")
    print(f"✅ Key loaded from: {env_path}")
else:
    print(f"❌ ERROR: Key still missing. I searched at: {env_path}")
    model = None

def ask_gemini(prompt):
    if not model:
        return "[Gemini not configured]"
    try:
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        return f"Gemini API error: {str(e)}"

def process_resume_evaluation(resume_text, job_description):
    try:
        prompt = f"""
        Evaluate the following resume against the job description.
        Resume: {resume_text}
        Job Description: {job_description}

        Return ONLY a JSON object with the following fields:
        {{
          "skill_match_score": 0.0,
          "matched_keywords": [],
          "missing_keywords": [],
          "categories": {{
            "Communication Skills": "",
            "Technical Fit": "",
            "Soft Skills": "",
            "Work Experience Relevance": ""
          }},
          "evaluation_summary": ""
        }}
        """

        # Use the configured model
        response = model.generate_content(
            prompt,
            generation_config={"response_mime_type": "application/json"}
        )

        # Clean the response text to ensure it's pure JSON
        clean_json = response.text.strip()
        if clean_json.startswith("```"):
            clean_json = clean_json.split("```")[1]
            if clean_json.startswith("json"):
                clean_json = clean_json[4:]

        evaluation_result = json.loads(response.text)

        skill_score = float(evaluation_result.get("skill_match_score", 0))
        if skill_score < 80:
            keyword = '+'.join(job_description.split()[:3])
            evaluation_result["improvement_resources"] = {
                "certification_courses": [
                    {
                        "title": "Top Udemy Course",
                        "description": "Explore top-rated Udemy courses.",
                        "link": f"https://www.udemy.com/courses/search/?src=ukw&q={keyword}"
                    }
                ],
                "youtube_link": f"https://www.youtube.com/results?search_query=how+to+improve+skills+for+{keyword}",
                "resume_examples": [
                    "https://novoresume.com/resume-templates",
                    "https://enhancv.com/resume-examples/"
                ]
            }

        return evaluation_result

    except Exception as e:
        # Return the error in a way that matches the expected JSON structure
        return {"error": f"Gemini API error: {str(e)}"}