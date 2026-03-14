"""
Test Script for Real-Time Activity Tracking
Adds sample browsing activities with current timestamps
"""
import requests
from datetime import datetime
import time

API_URL = "http://127.0.0.1:8000/track"

# Sample activities
activities = [
    {
        "type": "browsing",
        "url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
        "title": "YouTube - Latest Video",
        "timestamp": datetime.now().isoformat(),
        "details": {"source": "test_script"}
    },
    {
        "type": "browsing",
        "url": "https://stackoverflow.com/questions/latest",
        "title": "Stack Overflow - Latest Questions",
        "timestamp": datetime.now().isoformat(),
        "details": {"source": "test_script"}
    },
    {
        "type": "browsing",
        "url": "https://github.com/trending",
        "title": "GitHub Trending Repositories",
        "timestamp": datetime.now().isoformat(),
        "details": {"source": "test_script"}
    }
]

def send_activity(activity):
    """Send activity to tracking endpoint"""
    try:
        response = requests.post(API_URL, json=activity)
        if response.status_code == 200:
            print(f"✓ Tracked: {activity['title']}")
        else:
            print(f"✗ Failed: {response.status_code}")
    except Exception as e:
        print(f"✗ Error: {e}")

if __name__ == "__main__":
    print("🔄 Sending test activities to real-time tracker...")
    print(f"Current time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    
    for activity in activities:
        send_activity(activity)
        time.sleep(0.5)
    
    print(f"\n✅ Done! Check http://localhost:3000 to see real-time logs")
