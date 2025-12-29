import os
from dotenv import load_dotenv
import google.generativeai as genai

# 1. Try loading variables
load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")

print("------------------------------------------------")
print(f"DEBUG: Checking API Key...")

if not api_key:
    print("❌ ERROR: API Key is MISSING or None.")
    print("   -> Check your .env file name (it must be just '.env')")
    print("   -> Check if GOOGLE_API_KEY=... is inside it.")
else:
    print(f"✅ API Key found: {api_key[:5]}... (hidden)")

    # 2. Try connecting to Google
    print("\nDEBUG: Testing connection to Google Gemini...")
    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-flash-latest')
        response = model.generate_content("Say 'Hello Nexus' if you can hear me.")
        print(f"✅ SUCCESS! AI Responded: {response.text}")
    except Exception as e:
        print(f"❌ CONNECTION ERROR: {e}")
        print("   -> If this says '403', your API Key is invalid.")
        print("   -> If this says 'ConnectTimeout', it's your internet/proxy.")
print("------------------------------------------------")