from fastapi import APIRouter
from pydantic import BaseModel
from services.travel_time import get_travel_time
from services.weather import get_weather_by_coordinates  # Use the new coordinate-based function
from db import get_connection
import logging

router = APIRouter(prefix="/optimize", tags=["Optimization"])

# Define the request model for JSON input
class OptimizeRequest(BaseModel):
    perishability: int
    start: str  # "lat,lng" format
    end: str    # "lat,lng" format

@router.post("/")
def optimize_route(request: OptimizeRequest):
    # Extract data from the request model
    perishability = request.perishability
    start = request.start
    end = request.end
    
    travel_time = None
    weather_info = None
    score = None
    
    try:
        # Travel time (TomTom API)
        travel_time = get_travel_time(start, end)
        logging.info(f"Travel time result: {travel_time} (type: {type(travel_time)})")

        # Get weather from START coordinates (you could also use END or midpoint)
        try:
            start_lat, start_lng = map(float, start.split(','))
            weather_info = get_weather_by_coordinates(start_lat, start_lng)
            logging.info(f"Weather result: {weather_info}")
        except ValueError as coord_error:
            logging.error(f"Invalid coordinate format: {start} - {coord_error}")
            weather_info = {"weather": "unknown", "location": "invalid coordinates", "temperature": None}

        # Extract weather and location
        weather = weather_info.get("weather", "unknown")
        location = weather_info.get("location", "Unknown Location")
        temperature = weather_info.get("temperature")

        # Simple scoring
        score = perishability * (travel_time / 60)  # demo scoring
        logging.info(f"Calculated score: {score}")

        # Save to DB with better error handling
        try:
            conn = get_connection()
            cur = conn.cursor()
            
            # Log the data being inserted
            logging.info(f"Inserting: location={location}, perishability={perishability}, travel_time={travel_time}, weather={weather}, score={score}")
            
            cur.execute(
                "INSERT INTO deliveries (city, perishability, travel_time_sec, weather, final_score) VALUES (%s,%s,%s,%s,%s)",
                (location, perishability, travel_time, weather, score)
            )
            conn.commit()
            conn.close()
            
            logging.info("✅ Database insert successful")
            
        except Exception as db_error:
            logging.error(f"❌ Database insert failed: {db_error}")
            return {
                "error": f"Database insert failed: {str(db_error)}",
                "city": location,
                "travel_time_sec": travel_time,
                "weather": weather,
                "temperature": temperature,
                "final_score": score
            }

        return {
            "city": location,
            "travel_time_sec": travel_time,
            "weather": weather,
            "temperature": temperature,
            "final_score": score,
            "coordinates": {
                "start": start,
                "end": end
            }
        }
        
    except Exception as e:
        logging.error(f"❌ Optimization failed: {e}")
        return {
            "error": str(e),
            "city": weather_info.get("location") if weather_info else "unknown",
            "travel_time_sec": travel_time,
            "weather": weather_info.get("weather") if weather_info else "unknown",
            "temperature": weather_info.get("temperature") if weather_info else None,
            "final_score": score
        }