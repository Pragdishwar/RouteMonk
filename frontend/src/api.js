import axios from "axios";

// Change baseURL later when deploying backend
const API = axios.create({
  baseURL: "http://127.0.0.1:8000",
});

export const optimizeRoute = (data) => API.post("/optimize", data);
export const getHistory = () => API.get("/history");