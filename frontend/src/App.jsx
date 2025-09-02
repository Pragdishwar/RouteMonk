import { useState, useEffect } from "react";
import axios from "axios";
import MapSelector from "./MapSelector";

function App() {
  const [start, setStart] = useState(null);
  const [end, setEnd] = useState(null);
  const [perishability, setPerishability] = useState(5);
  const [city, setCity] = useState("");
  const [vehicle, setVehicle] = useState("truck");
  const [result, setResult] = useState(null);
  const [history, setHistory] = useState([]);
  const [routeSummary, setRouteSummary] = useState(null);

  // Fetch delivery history on load
  useEffect(() => {
    axios.get("http://127.0.0.1:8000/history/")
      .then(res => setHistory(res.data))
      .catch(() => console.log("History fetch failed"));
  }, []);

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!start || !end) {
      alert("Please select start and destination on map");
      return;
    }

    try {
      const res = await axios.post("http://127.0.0.1:8000/optimize/", null, {
        params: {
          start_lat: start.lat,
          start_lon: start.lng,
          end_lat: end.lat,
          end_lon: end.lng,
          perishability,
          city,
        },
      });
      setResult(res.data);

      // refresh history
      const histRes = await axios.get("http://127.0.0.1:8000/history/");
      setHistory(histRes.data);

    } catch (err) {
      console.error(err);
      alert("Optimization failed");
    }
  };

  return (
    <div className="p-6 space-y-6">
      <h1 className="text-3xl font-bold text-center">🚚 RouteMonk</h1>

      {/* Map Selector */}
      <MapSelector 
        onPick={(coords, type) => {
          if (type === "start") setStart(coords);
          if (type === "end") setEnd(coords);
        }} 
        onRoute={(summary) => setRouteSummary(summary)}
      />

      {/* Route Summary */}
      {routeSummary && (
        <div className="p-4 bg-yellow-100 rounded">
          <h2 className="font-bold">🛣️ Route Info</h2>
          <p>ETA: {Math.round(routeSummary.travelTimeInSeconds / 60)} min</p>
          <p>Distance: {(routeSummary.lengthInMeters / 1000).toFixed(2)} km</p>
        </div>
      )}

      {/* Input Form */}
      <form onSubmit={handleSubmit} className="space-y-4">
        <input 
          type="text" 
          placeholder="City" 
          value={city}
          onChange={(e) => setCity(e.target.value)}
          className="border p-2 w-full rounded"
        />
        <input 
          type="number"
          placeholder="Perishability (1-10)"
          value={perishability}
          onChange={(e) => setPerishability(e.target.value)}
          className="border p-2 w-full rounded"
        />
        <select 
          value={vehicle}
          onChange={(e) => setVehicle(e.target.value)}
          className="border p-2 w-full rounded"
        >
          <option value="truck">Truck</option>
          <option value="van">Van</option>
          <option value="bike">Bike</option>
        </select>
        <button type="submit" className="bg-blue-600 text-white px-4 py-2 rounded">
          Optimize Route
        </button>
      </form>

      {/* Optimization Result */}
      {result && (
        <div className="p-4 bg-green-100 rounded">
          <h2 className="font-bold">✅ Optimized Result</h2>
          <p>Travel Time: {Math.round(result.travel_time_sec/60)} min</p>
          <p>Weather: {result.weather}</p>
          <p>Final Score: {result.final_score}</p>
        </div>
      )}

      {/* History */}
      <div>
        <h2 className="font-bold text-xl">📜 Past Deliveries</h2>
        <table className="w-full border mt-2">
          <thead>
            <tr className="bg-gray-200">
              <th>ID</th><th>City</th><th>Time (min)</th><th>Weather</th><th>Score</th>
            </tr>
          </thead>
          <tbody>
            {history.map((h) => (
              <tr key={h.id} className="text-center border">
                <td>{h.id}</td>
                <td>{h.city}</td>
                <td>{Math.round(h.travel_time_sec/60)}</td>
                <td>{h.weather}</td>
                <td>{h.final_score}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}

export default App;
