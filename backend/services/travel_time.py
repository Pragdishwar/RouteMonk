import os, requests
from dotenv import load_dotenv
import logging

load_dotenv()
TOMTOM_API_KEY = os.getenv("TOMTOM_API_KEY")

def get_travel_time(start: str, end: str):
    try:
        if not TOMTOM_API_KEY:
            raise ValueError("TOMTOM_API_KEY not configured")
            
        url = f"https://api.tomtom.com/routing/1/calculateRoute/{start}:{end}/json?key={TOMTOM_API_KEY}&traffic=true"
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        
        data = response.json()
        return data["routes"]["summary"]["travelTimeInSeconds"]
        
    except Exception as e:
        logging.error(f"Travel time API error: {e}")
        return 1800  # Default 30 minutes if API fails
