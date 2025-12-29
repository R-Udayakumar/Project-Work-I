# from flask import Flask, request, jsonify
# from flask_cors import CORS
# from faker import Faker
# import random
# from ai_engine import generate_dynamic_profile # <-- Import the new brain

# app = Flask(__name__)
# CORS(app) # Enable CORS for frontend-backend communication
# fake = Faker()

# # In-memory storage for demo purposes. In a real app, use a database.
# student_profiles = {}

# # Mock Data for "RAG" System - Simulating a Knowledge Base
# MOCK_INDUSTRY_DATA = {
#     "Software Engineer": {
#         "skills": ["Python", "Java", "React", "AWS", "System Design", "SQL"],
#         "insights": [
#             "Demand for cloud-native skills (AWS/Azure) is at an all-time high.",
#             "Companies are prioritizing engineers with experience in microservices architecture.",
#             "AI-assisted coding tools are becoming standard in dev workflows."
#         ],
#         "challenges": [
#             "Build a REST API for a simple to-do list app using Flask or Django.",
#             "Deploy a simple static website using AWS S3 and CloudFront.",
#             "Write a script to parse a large CSV file and store the data in a SQL database."
#         ],
#         "courses": ["Full Stack Open", "AWS Certified Developer - Associate", "System Design Primer on GitHub"]
#     },
#     "Data Scientist": {
#         "skills": ["Python", "R", "Machine Learning", "SQL", "TensorFlow/PyTorch", "Data Visualization"],
#         "insights": [
#             "Generative AI is the hottest topic; knowing LLMs is a huge plus.",
#             "Data Engineering skills (ETL pipelines) are increasingly valued for Data Scientists.",
#             "Ethical AI and model interpretability are becoming critical business requirements."
#         ],
#         "challenges": [
#             "Clean a messy dataset and perform Exploratory Data Analysis (EDA).",
#             "Build a simple linear regression model to predict housing prices.",
#             "Fine-tune a pre-trained transformer model on a small text dataset."
#         ],
#         "courses": ["Andrew Ng's Machine Learning Specialization", "Fast.ai Deep Learning for Coders", "Data Engineering Zoomcamp"]
#     },
#     # Add more roles as needed
# }

# @app.route('/api/profile', methods=['POST'])
# def create_profile():
#     """Creates a new student profile (Digital Twin init)."""
#     data = request.json
#     student_id = fake.uuid4()
#     student_profiles[student_id] = {
#         "id": student_id,
#         "name": data.get("name"),
#         "target_role": data.get("target_role"),
#         "skills": data.get("skills", []),
#         "skill_gaps": [] # Will be calculated
#     }
#     return jsonify({"student_id": student_id, "message": "Profile created successfully!"})

# @app.route('/api/dashboard/<student_id>', methods=['GET'])
# def get_dashboard(student_id):
#     """Generates the personalized dashboard data (Simulates AI Core & RAG)."""
#     profile = student_profiles.get(student_id)
#     if not profile:
#         return jsonify({"error": "Student not found"}), 404

#     # role = profile["target_role"]
#     # role_data = MOCK_INDUSTRY_DATA.get(role, MOCK_INDUSTRY_DATA["Software Engineer"]) # Default to SE

#     # # 1. Simulate Skill Gap Analysis (Simple set difference)
#     # required_skills = set(role_data["skills"])
#     # student_skills = set(profile["skills"])
#     # skill_gaps = list(required_skills - student_skills)
#     # profile["skill_gaps"] = skill_gaps

#     # # 2. Simulate RAG-based Recommendations
#     # # In a real system, an LLM would generate this based on retrieved data.
#     # # Here, we just pick random items from our mock data.
#     # daily_insight = random.choice(role_data["insights"])
#     # micro_challenge = random.choice(role_data["challenges"])
#     # recommended_courses = random.sample(role_data["courses"], min(2, len(role_data["courses"])))

#     # dashboard_data = {
#     #     "student_name": profile["name"],
#     #     "target_role": role,
#     #     "skill_gaps": skill_gaps,
#     #     "daily_insight": daily_insight,
#     #     "todays_challenge": micro_challenge,
#     #     "recommended_learning_path": recommended_courses
#     # }

#     # return jsonify(dashboard_data)

#     # CALL THE REAL AI ENGINE
#     # We pass the real student data to the LLM
#     ai_insights = generate_dynamic_profile(profile)

#     # Combine profile info with AI insights
#     dashboard_data = {
#         "student_name": profile["name"],
#         "target_role": profile["target_role"],
#         "skill_gaps": ai_insights.get("skill_gaps", []),
#         "daily_insight": ai_insights.get("daily_insight", "Keep learning!"),
#         "todays_challenge": ai_insights.get("todays_challenge", "Check back tomorrow."),
#         "recommended_learning_path": ai_insights.get("recommended_learning_path", [])
#     }

#     return jsonify(dashboard_data)

# if __name__ == '__main__':
#     app.run(debug=True, port=5000)

import os
import json
import google.generativeai as genai  # <-- ADD THIS
from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from ai_engine import generate_dynamic_profile

# from ai_engine import generate_dynamic_profile

# --- ADD THIS CONFIGURATION BLOCK ---
import os
from dotenv import load_dotenv
load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
# ------------------------------------

app = Flask(__name__)
CORS(app)

# --- DATABASE CONFIGURATION ---
# This creates a file named 'nexus.db' in a folder called 'instance'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///nexus.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# --- DATABASE MODEL (The Schema) ---
class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    target_role = db.Column(db.String(100), nullable=False)
    skills = db.Column(db.String(500), nullable=False)
    # We store the AI response as text so we don't have to regenerate it every time
    ai_analysis = db.Column(db.Text, nullable=True)

# Create the database tables automatically
with app.app_context():
    db.create_all()

# --- ROUTES ---

@app.route('/api/init_twin', methods=['POST'])
def init_twin():
    data = request.json
    
    # 1. Generate AI Insights immediately
    print(f"🧠 Generating AI Profile for {data['name']}...")
    ai_result = generate_dynamic_profile(data)
    
    # --- THE FIX IS HERE ---
    # Convert the list of skills back to a string for the database
    # If data['skills'] is ["Java", "Python"], this becomes "Java, Python"
    skills_as_string = ", ".join(data['skills']) 
    
    # 2. Save User + AI Data to Database
    new_student = Student(
        name=data['name'],
        target_role=data['target_role'],
        skills=skills_as_string,  # <--- Save the STRING, not the list
        ai_analysis=json.dumps(ai_result)
    )
    
    db.session.add(new_student)
    db.session.commit()
    
    print(f"✅ Student {new_student.id} saved to Database!")

    return jsonify({
        "message": "Digital Twin Initialized & Saved", 
        "student_id": new_student.id
    })

@app.route('/api/dashboard/<int:student_id>', methods=['GET'])
def get_dashboard(student_id):
    # 1. Find student in Database
    student = Student.query.get_or_404(student_id)
    
    # 2. Retrieve the saved AI analysis
    # This is "High Performance" - we read from disk, not API
    ai_data = json.loads(student.ai_analysis)

    response_data = {
        "student_id": student.id,
        "student_name": student.name,
        "target_role": student.target_role,
        "skill_gaps": ai_data.get("skill_gaps", []),
        "daily_insight": ai_data.get("daily_insight", "Keep pushing forward!"),
        "todays_challenge": ai_data.get("todays_challenge", "Code something today."),
        "recommended_learning_path": ai_data.get("recommended_learning_path", [])
    }

    return jsonify(response_data)

    # --- CHAT ROUTE ---
@app.route('/api/chat', methods=['POST'])
def chat_with_mentor():
    data = request.json
    student_id = data.get('student_id')
    user_message = data.get('message')
    
    # 1. Get the Student's Context from DB
    student = Student.query.get_or_404(student_id)
    
    # 2. Build a Context-Aware Prompt
    # We use the Stable Model alias we fixed earlier
    model = genai.GenerativeModel('gemini-flash-latest')
    
    prompt = f"""
    You are 'Nexus', a wise and encouraging Career Mentor.
    
    STUDENT CONTEXT:
    - Name: {student.name}
    - Target Role: {student.target_role}
    - Known Skills: {student.skills}
    
    USER QUESTION: "{user_message}"
    
    INSTRUCTIONS:
    - Answer specifically for a {student.target_role}.
    - Be concise (max 3 sentences).
    - If they ask about learning, reference their specific skill gaps.
    """
    
    try:
        response = model.generate_content(prompt)
        return jsonify({"reply": response.text})
    except Exception as e:
        return jsonify({"reply": "I'm having trouble connecting to the network right now."})

if __name__ == '__main__':
    app.run(debug=True)