import os, requests
from dotenv import load_dotenv
import logging

load_dotenv()
WEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY")

def get_weather(city: str):
    try:
        url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={WEATHER_API_KEY}&units=metric"
        res = requests.get(url, timeout=10)
        data = res.json()
        if isinstance(data, dict) and "weather" in data and isinstance(data["weather"], list) and len(data["weather"]) > 0:
            return data["weather"][0]["description"]
        else:
            logging.error(f"Weather response not valid: {data}")
            return "unknown"
    except Exception as e:
        logging.error(f"Weather API error: {e}")
        return "unknown"

