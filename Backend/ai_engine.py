# import os
# import json
# import google.generativeai as genai
# from dotenv import load_dotenv

# # Load environment variables
# load_dotenv()

# # Configure the API key
# # You will need to get a free key from: https://aistudio.google.com/app/apikey
# GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
# genai.configure(api_key=GOOGLE_API_KEY)

# def generate_dynamic_profile(student_data):
#     """
#     Uses a Large Language Model to analyze the student profile 
#     and generate a custom, world-class industry roadmap.
#     """
    
#     student_name = student_data.get('name')
#     target_role = student_data.get('target_role')
#     current_skills = ", ".join(student_data.get('skills', []))

#     # This is the "Prompt Engineering" part - the brain of the operation.
#     prompt = f"""
#     Act as an elite Career Mentor and Industry Expert for a global tech firm.
#     Analyze the following student profile:
#     - Name: {student_name}
#     - Target Role: {target_role}
#     - Current Skills: {current_skills}

#     Your goal is to prepare this student for a top-tier industry job.
#     Perform a Gap Analysis and return a JSON object with the following fields:
#     1. "skill_gaps": A list of critical skills they are missing for {target_role}.
#     2. "daily_insight": A sophisticated, real-time industry trend or fact related to {target_role}.
#     3. "todays_challenge": A concrete, technical micro-challenge to build a missing skill.
#     4. "recommended_learning_path": A list of 3 specific, high-quality resources (courses, documentation, or project ideas).

#     Return ONLY raw JSON. No markdown formatting.
#     """

#     try:
#         model = genai.GenerativeModel('gemini-pro')
#         response = model.generate_content(prompt)
        
#         # Clean up the response to ensure it's valid JSON
#         json_str = response.text.replace('```json', '').replace('```', '')
#         return json.loads(json_str)
        
#     except Exception as e:
#         print(f"AI Generation Error: {e}")
#         # Fallback mechanism if AI fails (Robust Engineering)
#         return {
#             "skill_gaps": ["Critical Thinking", "Advanced System Design"],
#             "daily_insight": "AI is reshaping this role. Focus on adaptability.",
#             "todays_challenge": "Research the top 3 companies hiring for this role.",
#             "recommended_learning_path": ["Official Documentation", "GitHub Open Source"]
#         }

# import os
# import json
# import traceback
# import google.generativeai as genai
# from dotenv import load_dotenv
# import requests

# def validate_links(roadmap_json):
#     """
#     Iterates through the roadmap steps.
#     If a link returns 404, replace it with a generic search link.
#     """
#     for step in roadmap_json.get('roadmap', []):
#         url = step.get('link')
#         if url:
#             try:
#                 # Set a timeout so your app doesn't freeze
#                 response = requests.head(url, timeout=3)
#                 if response.status_code >= 400:
#                     # Link is dead, replace with a Google Search link
#                     query = f"{step['title']} tutorial"
#                     step['link'] = f"https://www.google.com/search?q={query.replace(' ', '+')}"
#             except:
#                 # If request fails (DNS error, etc.), fallback to Google
#                 query = f"{step['title']} tutorial"
#                 step['link'] = f"https://www.google.com/search?q={query.replace(' ', '+')}"
#     return roadmap_json

# load_dotenv()
# api_key = os.getenv("GOOGLE_API_KEY")
# genai.configure(api_key=api_key)

# def generate_dynamic_profile(student_data):
#     # USE THE ALIAS THAT WORKED IN YOUR TEST
#     model = genai.GenerativeModel('gemini-flash-latest')
    
#     target_role = student_data.get('target_role')
#     skills = ", ".join(student_data.get('skills', []))

#     # prompt = f"""
#     # You are a Career Architect.
#     # User Goal: {target_role}
#     # User Skills: {skills}

#     # Task:
#     # 1. Identify 5 missing technical skills.
#     # 2. Provide 1 industry insight.
#     # 3. Create 1 short coding challenge.
#     # 4. List 3 learning resources.

#     # Output: JSON ONLY.
#     # Structure:
#     # {{
#     #   "skill_gaps": ["skill1", "skill2"],
#     #   "daily_insight": "text",
#     #   "todays_challenge": "text",
#     #   "recommended_learning_path": ["url1", "url2"]
#     # }}
#     # """

#     # UPDATED PROMPT: Request 'roadmap' with title and link objects
#     prompt = f"""
#     You are a Career Architect.
#     User Goal: {target_role}
#     User Skills: {skills}

#     Task:
#     1. Identify 5 missing technical skills.
#     2. Provide 1 industry insight.
#     3. Create 1 short coding challenge.
#     4. List 3 learning resources.

#     Output: JSON ONLY.
#     Structure:
#     {{
#       "skill_gaps": ["skill1", "skill2"],
#       "daily_insight": "text",
#       "todays_challenge": "text",
#       "roadmap": [
#         {{"title": "Resource Title", "link": "url"}}
#       ]
#     }}
#     """

#     try:
#         # response = model.generate_content(prompt)
#         # text = response.text.strip()
#         # # Clean up markdown if AI adds it
#         # if text.startswith("```json"): text = text[7:]
#         # if text.endswith("```"): text = text[:-3]
#         # return json.loads(text)
#         response = model.generate_content(prompt)
#         text = response.text.strip()
        
#         # Clean up markdown if AI adds it
#         if text.startswith("```json"): text = text[7:]
#         if text.endswith("```"): text = text[:-3]
        
#         # --- ADD THESE LINES ---
#         data = json.loads(text)       # 1. Convert text to JSON
#         data = validate_links(data)   # 2. Fix broken links
#         return data                   # 3. Return validated data
#         # -----------------------
#     # except Exception as e:
#     #     traceback.print_exc()
#     #     return {
#     #         "skill_gaps": ["AI Connection Issue"],
#     #         "daily_insight": "Could not retrieve insight.",
#     #         "todays_challenge": "Check terminal logs.",
#     #         "recommended_learning_path": []
#     #     }
#     except Exception as e:
#         traceback.print_exc()
#         return {
#             "skill_gaps": ["AI Connection Issue"],
#             "daily_insight": "Could not retrieve insight.",
#             "todays_challenge": "Check terminal logs.",
#             # CHANGE THIS KEY from "recommended_learning_path" to "roadmap"
#             "roadmap": [] 
#         }

import os
import json
import traceback
import google.generativeai as genai
from dotenv import load_dotenv
import requests

# Load environment variables
load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=api_key)

def validate_links(roadmap_json):
    """
    Iterates through the roadmap steps.
    If a link returns 404, replace it with a generic search link.
    """
    # Check if 'roadmap' exists, if not, try to find 'recommended_learning_path'
    steps = roadmap_json.get('roadmap', [])
    
    for step in steps:
        url = step.get('link')
        if url:
            try:
                # Set a timeout (3 seconds) so the app doesn't freeze
                response = requests.head(url, timeout=3)
                
                # If 404 (Not Found) or 403 (Forbidden), fix the link
                if response.status_code >= 400:
                    query = f"{step.get('title', 'Tutorial')} {step.get('tech', '')} tutorial"
                    step['link'] = f"https://www.google.com/search?q={query.replace(' ', '+')}"
            except:
                # If request fails (DNS error, etc.), fallback to Google Search
                query = f"{step.get('title', 'Tutorial')} tutorial"
                step['link'] = f"https://www.google.com/search?q={query.replace(' ', '+')}"
    
    return roadmap_json

def generate_dynamic_profile(student_data):
    # Use the model alias
    model = genai.GenerativeModel('gemini-flash-latest')
    
    target_role = student_data.get('target_role')
    skills = ", ".join(student_data.get('skills', []))

    # Prompt asks for "roadmap" to enable structure validation
    prompt = f"""
    You are a Career Architect.
    User Goal: {target_role}
    User Skills: {skills}

    Task:
    1. Identify 5 missing technical skills (Critical Missing Links).
    2. Provide 1 industry insight (Market Pulse).
    3. Create 1 short coding challenge (Active Protocol).
    4. List 3 learning resources (Upload Sequence).

    Output: JSON ONLY.
    Structure:
    {{
      "skill_gaps": ["skill1", "skill2"],
      "daily_insight": "text",
      "todays_challenge": "text",
      "roadmap": [
        {{"title": "Resource Title", "link": "url"}}
      ]
    }}
    """

    try:
        response = model.generate_content(prompt)
        text = response.text.strip()
        
        # Clean up markdown if AI adds it
        if text.startswith("```json"): text = text[7:]
        if text.endswith("```"): text = text[:-3]
        
        # 1. Parse JSON
        data = json.loads(text)
        
        # 2. Fix broken links
        data = validate_links(data)
        
        # --- CRITICAL FIX: MAP DATA TO THE KEY YOUR FRONTEND EXPECTS ---
        # Your React frontend looks for "recommended_learning_path", 
        # so we copy "roadmap" to that key.
        data['recommended_learning_path'] = data.get('roadmap', [])
        # ---------------------------------------------------------------

        return data

    except Exception as e:
        traceback.print_exc()
        # Return empty structure with BOTH keys to prevent frontend crashes
        return {
            "skill_gaps": ["AI Connection Issue"],
            "daily_insight": "Could not retrieve insight.",
            "todays_challenge": "Check terminal logs.",
            "roadmap": [],
            "recommended_learning_path": [] 
        }