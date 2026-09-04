import os
import requests
from dotenv import load_dotenv

load_dotenv()
token = os.getenv("WAQI_TOKEN")

city = "bhopal"
url = f"https://api.waqi.info/feed/{city}/?token={token}"

response = requests.get(url)
data = response.json()

print("Status:", data["status"])
print("AQI data:", data["data"])