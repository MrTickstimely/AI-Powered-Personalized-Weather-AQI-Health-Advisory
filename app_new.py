import os
import requests
import streamlit as st
from dotenv import load_dotenv

load_dotenv()
WAQI_TOKEN = os.getenv("WAQI_TOKEN")

st.set_page_config(page_title="Personal Weather & AQI Advisory", page_icon="🌤️")
st.title("🌤️ Personalized Weather & AQI Health Advisory")

# --- City input ---
city_options = ["Bhopal", "Delhi", "Mumbai", "Bengaluru", "Chennai", "Kolkata", "Hyderabad", "Pune", "Other"]
city_choice = st.selectbox("Select your city", city_options)

if city_choice == "Other":
    city = st.text_input("Enter your city name")
else:
    city = city_choice

# --- Profile inputs ---
st.subheader("Your Profile")
age_group = st.selectbox("Age group", ["Child (0-12)", "Teen (13-19)", "Adult (20-59)", "Senior (60+)"])
health_condition = st.selectbox("Health condition", ["None", "Asthma", "Heart condition", "Pregnant", "Other respiratory issue"])
occupation = st.selectbox("Occupation type", ["Indoor / desk job", "Outdoor worker", "Athlete / very active"])

if st.button("Get My Advisory"):
    if not city:
        st.error("Please enter a city name.")
    else:
        with st.spinner("Fetching live conditions..."):
            geo_url = "https://geocoding-api.open-meteo.com/v1/search"
            geo_resp = requests.get(geo_url, params={"name": city, "count": 1}).json()

            if not geo_resp.get("results"):
                st.error("City not found. Try a different spelling.")
            else:
                lat = geo_resp["results"][0]["latitude"]
                lon = geo_resp["results"][0]["longitude"]

                weather_url = "https://api.open-meteo.com/v1/forecast"
                weather_params = {
                    "latitude": lat,
                    "longitude": lon,
                    "current": "temperature_2m,relative_humidity_2m"
                }
                weather_data = requests.get(weather_url, params=weather_params).json()["current"]

                aqi_url = f"https://api.waqi.info/feed/geo:{lat};{lon}/?token={WAQI_TOKEN}"
                aqi_resp = requests.get(aqi_url).json()
                aqi_value = aqi_resp["data"]["aqi"] if aqi_resp["status"] == "ok" else "N/A"
                aqi_station = aqi_resp["data"]["city"]["name"] if aqi_resp["status"] == "ok" else ""

                col1, col2, col3 = st.columns(3)
                col1.metric("Temperature", f"{weather_data['temperature_2m']} °C")
                col2.metric("Humidity", f"{weather_data['relative_humidity_2m']} %")
                col3.metric("AQI", aqi_value)
                if aqi_station:
                    st.caption(f"AQI station: {aqi_station}")

                from groq import Groq
                client = Groq(api_key=os.getenv("GROQ_API_KEY"))
                prompt = f"""A person with this profile:
- Age group: {age_group}
- Health condition: {health_condition}
- Occupation: {occupation}
Current conditions in {city}:
- Temperature: {weather_data['temperature_2m']}°C
- Humidity: {weather_data['relative_humidity_2m']}%
- AQI: {aqi_value}
Write a short, plain-English health advisory (3-4 sentences) telling them whether it's safe to go outside, any precautions to take, and why — tailored specifically to their profile. Be direct and practical, not generic."""
                chat_completion = client.chat.completions.create(
                    messages=[{"role": "user", "content": prompt}],
                    model="qwen/qwen3.8-27b",
                )
                advisory = chat_completion.choices[0].message.content
                st.subheader("Your Personalized Advisory")
                st.info(advisory)