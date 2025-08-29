import React, { useState } from "react";

function RouteForm({ onSubmit }) {
  const [form, setForm] = useState({
    start_lat: "",
    start_lon: "",
    end_lat: "",
    end_lon: "",
    perishability: 5,
    city: "",
  });

  const handleChange = (e) => {
    setForm({ ...form, [e.target.name]: e.target.value });
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    onSubmit(form);
  };

  return (
    <form onSubmit={handleSubmit} className="bg-white p-6 shadow rounded-lg">
      <h2 className="text-xl font-semibold mb-4">Optimize Route</h2>

      {["start_lat", "start_lon", "end_lat", "end_lon", "city"].map((field) => (
        <input
          key={field}
          type="text"
          name={field}
          placeholder={field.replace("_", " ")}
          value={form[field]}
          onChange={handleChange}
          className="border p-2 w-full mb-3 rounded"
          required
        />
      ))}

      <input
        type="number"
        name="perishability"
        placeholder="Perishability (1-10)"
        value={form.perishability}
        onChange={handleChange}
        className="border p-2 w-full mb-3 rounded"
        min="1"
        max="10"
        required
      />

      <button
        type="submit"
        className="bg-blue-500 hover:bg-blue-600 text-white py-2 px-4 rounded w-full"
      >
        Optimize
      </button>
    </form>
  );
}

export default RouteForm;