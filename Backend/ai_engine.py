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

import os
import json
import traceback
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=api_key)

def generate_dynamic_profile(student_data):
    # USE THE ALIAS THAT WORKED IN YOUR TEST
    model = genai.GenerativeModel('gemini-flash-latest')
    
    target_role = student_data.get('target_role')
    skills = ", ".join(student_data.get('skills', []))

    prompt = f"""
    You are a Career Architect.
    User Goal: {target_role}
    User Skills: {skills}

    Task:
    1. Identify 5 missing technical skills.
    2. Provide 1 industry insight.
    3. Create 1 short coding challenge.
    4. List 3 learning resources.

    Output: JSON ONLY.
    Structure:
    {{
      "skill_gaps": ["skill1", "skill2"],
      "daily_insight": "text",
      "todays_challenge": "text",
      "recommended_learning_path": ["url1", "url2"]
    }}
    """

    try:
        response = model.generate_content(prompt)
        text = response.text.strip()
        # Clean up markdown if AI adds it
        if text.startswith("```json"): text = text[7:]
        if text.endswith("```"): text = text[:-3]
        return json.loads(text)
    except Exception as e:
        traceback.print_exc()
        return {
            "skill_gaps": ["AI Connection Issue"],
            "daily_insight": "Could not retrieve insight.",
            "todays_challenge": "Check terminal logs.",
            "recommended_learning_path": []
        }