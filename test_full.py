import requests
import json

# Test the Flask API endpoint
url = "http://127.0.0.1:5000/chat"
payload = {"message": "Climate change is a serious problem"}

print("🧪 Testing Debate Gravity API...")
print(f"📤 Sending: {payload['message']}")

try:
    response = requests.post(url, json=payload)
    print(f"\n📊 Status Code: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        print(f"✅ AI Response: {data.get('response', 'No response')}")
        print("\n🎉 Application is working perfectly!")
    else:
        print(f"❌ Error: {response.text}")
        
except Exception as e:
    print(f"❌ Connection Error: {e}")
