import { MapContainer, TileLayer, Marker, Polyline, useMapEvents } from "react-leaflet";
import "leaflet/dist/leaflet.css";
import { useState, useEffect } from "react";
import axios from "axios";
import L from "leaflet";

// Custom marker icons
const startIcon = new L.Icon({
  iconUrl: "https://maps.google.com/mapfiles/ms/icons/green-dot.png",
  iconSize: [32, 32],
});

const endIcon = new L.Icon({
  iconUrl: "https://maps.google.com/mapfiles/ms/icons/red-dot.png",
  iconSize: [32, 32],
});

function LocationPicker({ onSelect, resetTrigger, onRoute }) {
  const [start, setStart] = useState(null);
  const [end, setEnd] = useState(null);
  const [routeCoords, setRouteCoords] = useState([]);
  const [routeColor, setRouteColor] = useState("blue");

  useMapEvents({
    click(e) {
      if (!start) {
        setStart(e.latlng);
        onSelect(e.latlng, "start");
      } else if (!end) {
        setEnd(e.latlng);
        onSelect(e.latlng, "end");
      }
    },
  });

  // Reset markers and route when reset is triggered
  useEffect(() => {
    setStart(null);
    setEnd(null);
    setRouteCoords([]);
    setRouteColor("blue");
  }, [resetTrigger]);

  // Fetch route when both start and end are set
  useEffect(() => {
    const fetchRoute = async () => {
      if (start && end) {
        try {
          const url = `https://api.tomtom.com/routing/1/calculateRoute/${start.lat},${start.lng}:${end.lat},${end.lng}/json?traffic=true&key=YOUR_TOMTOM_API_KEY`;
          const res = await axios.get(url);

          const points = res.data.routes[0].legs[0].points.map(p => [p.latitude, p.longitude]);
          setRouteCoords(points);

          const summary = res.data.routes[0].summary;
          onRoute(summary);

          // Dynamic color based on ETA
          const etaMinutes = summary.travelTimeInSeconds / 60;
          if (etaMinutes < 20) setRouteColor("green");
          else if (etaMinutes <= 45) setRouteColor("orange");
          else setRouteColor("red");

        } catch (err) {
          console.error("Route fetch failed", err);
        }
      }
    };
    fetchRoute();
  }, [start, end]);

  return (
    <>
      {start && <Marker position={start} icon={startIcon}></Marker>}
      {end && <Marker position={end} icon={endIcon}></Marker>}
      {routeCoords.length > 0 && (
        <Polyline positions={routeCoords} color={routeColor} weight={5} />
      )}
    </>
  );
}

export default function MapSelector({ onPick, onRoute }) {
  const [resetKey, setResetKey] = useState(0);

  const handleReset = () => {
    setResetKey(prev => prev + 1);
    onPick(null, "start");
    onPick(null, "end");
    onRoute(null);
  };

  return (
    <div>
      <MapContainer center={[12.9716, 77.5946]} zoom={13} style={{ height: "500px", width: "100%" }}>
        {/* Base Map */}
        <TileLayer
          url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
          attribution="&copy; OpenStreetMap contributors"
        />

        {/* TomTom Traffic Overlay */}
        <TileLayer
          url={`https://api.tomtom.com/traffic/map/4/tile/flow/relative0/{z}/{x}/{y}.png?key=YOUR_TOMTOM_API_KEY`}
          attribution="Traffic © TomTom"
        />

        <LocationPicker onSelect={onPick} resetTrigger={resetKey} onRoute={onRoute} />
      </MapContainer>

      {/* Reset Button */}
      <div className="mt-2 text-center">
        <button 
          onClick={handleReset} 
          className="bg-red-600 text-white px-4 py-2 rounded"
        >
          Reset Points
        </button>
      </div>
    </div>
  );
}
