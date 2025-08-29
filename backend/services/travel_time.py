import os, requests
from dotenv import load_dotenv
load_dotenv()

TOMTOM_API_KEY = os.getenv("TOMTOM_API_KEY")

def get_travel_time(start: str, end: str):
    url = f"https://api.tomtom.com/routing/1/calculateRoute/{start}:{end}/json?key={TOMTOM_API_KEY}&traffic=true"
    res = requests.get(url).json()
    return res["routes"][0]["summary"]["travelTimeInSeconds"]
