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
    axios
      .get("https://routemonk-backend.onrender.com/history/")
      .then((res) => setHistory(res.data.history || []))
      .catch(() => console.log("History fetch failed"));
  }, []);

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!start || !end) {
      alert("Please select start and destination on map");
      return;
    }

    try {
      const res = await axios.post(
        "https://routemonk-backend.onrender.com/optimize/",
        null,
        {
          params: {
            start: `${start.lat},${start.lng}`,
            end: `${end.lat},${end.lng}`,
            perishability: Number(perishability),
            city,
          },
        }
      );
      setResult(res.data);

      // refresh history
      const histRes = await axios.get(
        "https://routemonk-backend.onrender.com/history/"
      );
      setHistory(histRes.data.history || []);
    } catch (err) {
      console.error(err);
      if (err.response?.status === 422) {
        alert("Invalid coordinates or city. Please check your input.");
      } else if (err.response?.status === 500) {
        alert("Server error. Please check backend and try again.");
      } else {
        alert("Optimization failed");
      }
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
          onChange={(e) => setPerishability(Number(e.target.value))}
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
        <button
          type="submit"
          className="bg-blue-600 text-white px-4 py-2 rounded"
        >
          Optimize Route
        </button>
      </form>

      {/* Optimization Result */}
      {result && (
        <div className="p-4 bg-green-100 rounded">
          <h2 className="font-bold">✅ Optimized Result</h2>
          <p>Travel Time: {Math.round(result.travel_time_sec / 60)} min</p>
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
              <th>ID</th>
              <th>City</th>
              <th>Time (min)</th>
              <th>Weather</th>
              <th>Score</th>
            </tr>
          </thead>
          <tbody>
            {Array.isArray(history) &&
              history.map((h, index) => (
                <tr key={h[0] || index} className="text-center border">
                  <td>{h[0]}</td>
                  <td>{h[1]}</td>
                  <td>{Math.round(h[2] / 60)}</td>
                  <td>{h[3]}</td>
                  <td>{h[4]}</td>
                </tr>
              ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}

export default App;
