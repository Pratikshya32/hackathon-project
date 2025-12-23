import os
from dotenv import load_dotenv
import google.generativeai as genai

# Load environment variables
load_dotenv()

GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')
print(f"API Key loaded: {GOOGLE_API_KEY[:20]}..." if GOOGLE_API_KEY else "No API key found")

genai.configure(api_key=GOOGLE_API_KEY)

# Test the model
try:
    model = genai.GenerativeModel('models/gemini-2.5-flash')
    print("✅ Model initialized successfully!")
    
    # Test a simple request
    response = model.generate_content("Say 'Hello, Debate Gravity is working!' in one sentence.")
    print(f"\n✅ API Response: {response.text}")
    print("\n🎉 Everything is working correctly!")
    
except Exception as e:
    print(f"❌ Error: {e}")
