const API_BASE = import.meta.env.VITE_API_BASE_URL;

useEffect(() => {
  axios.get(`${API_BASE}/history/`)
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
    const res = await axios.post(`${API_BASE}/optimize/`, null, {
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

    const histRes = await axios.get(`${API_BASE}/history/`);
    setHistory(histRes.data);

  } catch (err) {
    console.error(err);
    alert("Optimization failed");
  }
};
