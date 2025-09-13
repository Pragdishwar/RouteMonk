import os, requests
from dotenv import load_dotenv
import logging

load_dotenv()
WEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY")

def get_weather_by_coordinates(lat: float, lng: float):
    """Get weather using coordinates directly"""
    try:
        if not WEATHER_API_KEY:
            raise ValueError("OPENWEATHER_API_KEY not configured")

        # Use coordinates instead of city name
        url = f"http://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lng}&appid={WEATHER_API_KEY}&units=metric"
        response = requests.get(url, timeout=10)
        response.raise_for_status()

        data = response.json()
        if isinstance(data, dict) and "weather" in data and isinstance(data["weather"], list) and len(data["weather"]) > 0:
            # Return both weather and location name
            weather_desc = data["weather"][0]["description"]
            location_name = data.get("name", "Unknown Location")
            return {
                "weather": weather_desc,
                "location": location_name,
                "temperature": data["main"]["temp"]
            }
        else:
            logging.error(f"Weather response not valid: {data}")
            return {"weather": "unknown", "location": "unknown", "temperature": None}
    except Exception as e:
        logging.error(f"Weather API error for coordinates {lat},{lng}: {e}")
        return {"weather": "unknown", "location": "unknown", "temperature": None}

def get_weather(city: str):
    """Keep the old function for backward compatibility"""
    try:
        if not WEATHER_API_KEY:
            raise ValueError("OPENWEATHER_API_KEY not configured")

        url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={WEATHER_API_KEY}&units=metric"
        response = requests.get(url, timeout=10)
        response.raise_for_status()

        data = response.json()
        if isinstance(data, dict) and "weather" in data and isinstance(data["weather"], list) and len(data["weather"]) > 0:
            return data["weather"][0]["description"]
        else:
            logging.error(f"Weather response not valid: {data}")
            return "unknown"
    except Exception as e:
        logging.error(f"Weather API error for city '{city}': {e}")
        return "unknown"