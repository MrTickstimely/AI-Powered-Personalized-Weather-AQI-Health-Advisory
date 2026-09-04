import requests

# Bhopal coordinates as a test
lat, lon = 23.2599, 77.4126

url = "https://api.open-meteo.com/v1/forecast"
params = {
    "latitude": lat,
    "longitude": lon,
    "current": "temperature_2m,relative_humidity_2m",
    "hourly": "temperature_2m"
}

response = requests.get(url, params=params)
data = response.json()

print("Status code:", response.status_code)
print("Current weather:", data["current"])