from fastapi import APIRouter
from pydantic import BaseModel
from services.travel_time import get_travel_time
from services.weather import get_weather
from db import get_connection

router = APIRouter(prefix="/optimize", tags=["Optimization"])

# Define the request model for JSON input
class OptimizeRequest(BaseModel):
    city: str
    perishability: int
    start: str
    end: str

@router.post("/")
def optimize_route(request: OptimizeRequest):
    # Extract data from the request model
    city = request.city
    perishability = request.perishability
    start = request.start
    end = request.end
    
    try:
        # Travel time (TomTom API)
        travel_time = get_travel_time(start, end)

        # Weather (OpenWeather API)  
        weather = get_weather(city)

        # Simple scoring
        score = perishability * (travel_time / 60)  # demo scoring

        # Save to DB
        conn = get_connection()
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO deliveries (city, perishability, travel_time_sec, weather, final_score) VALUES (%s,%s,%s,%s,%s)",
            (city, perishability, travel_time, weather, score)
        )
        conn.commit()
        conn.close()

        return {
            "city": city,
            "travel_time_sec": travel_time,
            "weather": weather,
            "final_score": score
        }
    except Exception as e:
        return {"error": str(e)}