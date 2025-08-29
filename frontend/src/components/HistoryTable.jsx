import React from "react";

function HistoryTable({ history }) {
  return (
    <div className="bg-white p-6 shadow rounded-lg">
      <h2 className="text-xl font-semibold mb-4">Delivery History</h2>
      <table className="table-auto w-full border-collapse border">
        <thead>
          <tr className="bg-gray-200">
            <th className="border p-2">City</th>
            <th className="border p-2">Weather</th>
            <th className="border p-2">Travel Time</th>
            <th className="border p-2">Score</th>
          </tr>
        </thead>
        <tbody>
          {history.map((h, idx) => (
            <tr key={idx} className="text-center">
              <td className="border p-2">{h.city || "-"}</td>
              <td className="border p-2">{h.weather}</td>
              <td className="border p-2">{h.travel_time_sec} sec</td>
              <td className="border p-2">{h.final_score}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

export default HistoryTable;