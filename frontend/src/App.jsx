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
      .then((res) => {
        console.log("History response:", res.data);
        setHistory(res.data.history || []);
      })
      .catch((err) => {
        console.log("History fetch failed:", err);
      });
  }, []);

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!start || !end) {
      alert("Please select start and destination on map");
      return;
    }

    try {
      // Send JSON body data (matching your deployed backend)
      const requestData = {
        city: city,
        perishability: Number(perishability),
        start: `${start.lat},${start.lng}`,
        end: `${end.lat},${end.lng}`
      };

      console.log("Sending request data:", requestData);

      const res = await axios.post(
        "https://routemonk-backend.onrender.com/optimize/",
        requestData,
        {
          headers: {
            'Content-Type': 'application/json',
          }
        }
      );
      
      console.log("Optimization result:", res.data);
      setResult(res.data);

      // refresh history
      const histRes = await axios.get(
        "https://routemonk-backend.onrender.com/history/"
      );
      console.log("Updated history:", histRes.data);
      setHistory(histRes.data.history || []);
      
    } catch (err) {
      console.error("Full error:", err);
      console.error("Error response:", err.response?.data);
      
      if (err.response?.status === 422) {
        alert("Invalid input data. Please check your coordinates and city name.");
      } else if (err.response?.status === 500) {
        alert("Server error. Please try again later.");
      } else if (err.code === 'ERR_NETWORK') {
        alert("Cannot connect to backend server.");
      } else {
        alert(`Request failed: ${err.response?.status || 'Unknown'} - ${err.message}`);
      }
    }
  };

  return (
    <div className="container mx-auto p-4">
      <h1 className="text-3xl font-bold text-center mb-6">🚚 RouteMonk</h1>

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
        <div className="bg-blue-100 p-4 rounded mb-4">
          <h3 className="font-bold mb-2">🛣️ Route Info</h3>
          <p>ETA: {Math.round(routeSummary.travelTimeInSeconds / 60)} min</p>
          <p>Distance: {(routeSummary.lengthInMeters / 1000).toFixed(2)} km</p>
        </div>
      )}

      {/* Input Form */}
      <form onSubmit={handleSubmit} className="bg-gray-100 p-4 rounded mb-4">
        <input
          type="text"
          placeholder="City (e.g., Mumbai, Chennai, Bengaluru)"
          value={city}
          onChange={(e) => setCity(e.target.value)}
          className="border p-2 w-full rounded mb-2"
          required
        />
        <input
          type="number"
          placeholder="Perishability (1-10)"
          min="1"
          max="10"
          value={perishability}
          onChange={(e) => setPerishability(Number(e.target.value))}
          className="border p-2 w-full rounded mb-2"
        />
        <select
          value={vehicle}
          onChange={(e) => setVehicle(e.target.value)}
          className="border p-2 w-full rounded mb-2"
        >
          <option value="truck">Truck</option>
          <option value="van">Van</option>
          <option value="bike">Bike</option>
        </select>
        <button
          type="submit"
          className="bg-blue-500 text-white p-2 rounded w-full hover:bg-blue-600"
          disabled={!start || !end || !city}
        >
          Optimize Route
        </button>
      </form>

      {/* Optimization Result */}
      {result && (
        <div className="bg-green-100 p-4 rounded mb-4">
          <h3 className="font-bold mb-2">✅ Optimized Result</h3>
          <p><strong>City:</strong> {result.city}</p>
          <p><strong>Travel Time:</strong> {Math.round(result.travel_time_sec / 60)} min</p>
          <p><strong>Weather:</strong> {result.weather || 'Unknown'}</p>
          <p><strong>Final Score:</strong> {result.final_score?.toFixed?.(2) || result.final_score}</p>
        </div>
      )}

      {/* History */}
      <div className="bg-gray-50 p-4 rounded">
        <h3 className="font-bold mb-4">📜 Past Deliveries</h3>
        {Array.isArray(history) && history.length > 0 ? (
          <div className="overflow-x-auto">
            <table className="w-full border-collapse border">
              <thead>
                <tr className="bg-gray-200">
                  <th className="border p-2">ID</th>
                  <th className="border p-2">City</th>
                  <th className="border p-2">Time (min)</th>
                  <th className="border p-2">Weather</th>
                  <th className="border p-2">Score</th>
                </tr>
              </thead>
              <tbody>
                {history.map((h, index) => {
                  // Database columns: [id, city, perishability, travel_time_sec, weather, final_score, created_at]
                  // Correct mapping:
                  const id = h[0];
                  const city = h[1]; 
                  const perishability = h[2];
                  const travel_time_sec = h[3];
                  const weather = h[4];
                  const final_score = h[5];
                  const created_at = h[6];
                  
                  return (
                    <tr key={index} className="hover:bg-gray-100">
                      <td className="border p-2">{id}</td>
                      <td className="border p-2">{city}</td>
                      <td className="border p-2">{Math.round(travel_time_sec / 60)}</td>
                      <td className="border p-2">{weather || 'Unknown'}</td>
                      <td className="border p-2">{typeof final_score === 'number' ? final_score.toFixed(2) : final_score}</td>
                    </tr>
                  );
                })}
              </tbody>
            </table>
          </div>
        ) : (
          <p className="text-gray-500">No delivery history yet. Complete your first route optimization!</p>
        )}
      </div>
    </div>
  );
}

export default App;