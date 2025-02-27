import requests
import time

API_URL = "https://your-service-url.onrender.com/keep-alive"

while True:
    try:
        response = requests.get(API_URL)
        print("Keep-alive ping:", response.status_code)
    except Exception as e:
        print("Error:", e)
    time.sleep(600)  # Ping every 10 minutes
