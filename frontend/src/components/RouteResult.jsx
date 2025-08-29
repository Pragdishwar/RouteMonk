import React from "react";

function RouteResult({ result }) {
  return (
    <div className="bg-green-100 p-4 rounded shadow">
      <h3 className="font-semibold text-lg mb-2">Optimized Result</h3>
      <p>⏱ Travel Time: {result.travel_time_sec} sec</p>
      <p>☁️ Weather: {result.weather}</p>
      <p>📊 Score: {result.final_score}</p>
    </div>
  );
}

export default RouteResult;