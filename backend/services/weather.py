import os, requests
from dotenv import load_dotenv
import logging

load_dotenv()
WEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY")

def get_weather(city: str):
    try:
        if not WEATHER_API_KEY:
            raise ValueError("OPENWEATHER_API_KEY not configured")
            
        url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={WEATHER_API_KEY}&units=metric"
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        
        data = response.json()
        return data["weather"]["description"]
        
    except Exception as e:
        logging.error(f"Weather API error: {e}")
        return "unknown"  # Default weather if API fails
