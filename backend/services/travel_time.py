import os, requests
from dotenv import load_dotenv
import logging

load_dotenv()
TOMTOM_API_KEY = os.getenv("TOMTOM_API_KEY")

def get_travel_time(start: str, end: str):
    try:
        url = f"https://api.tomtom.com/routing/1/calculateRoute/{start}:{end}/json?key={TOMTOM_API_KEY}&traffic=true"
        res = requests.get(url, timeout=10)
        data = res.json()
        if isinstance(data, dict) and "routes" in data:
            return data["routes"][0]["summary"]["travelTimeInSeconds"]
        else:
            logging.error(f"TomTom response not valid: {data}")
            return 1800  # fallback value
    except Exception as e:
        logging.error(f"Travel time API error: {e}")
        return 1800

