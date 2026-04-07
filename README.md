# 🚚 RouteMonk

RouteMonk is a full-stack web application designed to optimize delivery routes by considering real-time weather constraints and the perishability of goods. By leveraging dynamic mapping, routing APIs, and live weather conditions, RouteMonk provides an intelligent score to ensure perishables reach their destinations safely and efficiently.

## ✨ Features

- **Interactive Map Selection:** Easily set start and destination points using an interactive map powered by React-Leaflet.
- **Route Optimization:** Calculates precise travel times considering real-time traffic data via the TomTom API.
- **Weather Integration:** Automatically detects real-time weather conditions and temperature based on route coordinates using the OpenWeather API.
- **Intelligent Scoring:** Computes a calculated "Final Score" based on the perishability condition of goods and estimated travel time.
- **Historical Tracking:** Saves all generated optimization routes to a PostgreSQL database, allowing users to view a comprehensive history of past deliveries.

## 🛠️ Tech Stack

### Frontend
- **Framework:** React.js powered by Vite
- **Styling:** Tailwind CSS
- **Mapping:** React-Leaflet
- **HTTP Client:** Axios

### Backend
- **Framework:** Python 3 & FastAPI
- **Database:** PostgreSQL (with SQLAlchemy layer)
- **Containerization:** Docker & Docker Compose
- **External API Integrations:**
  - [TomTom Routing API](https://developer.tomtom.com/routing-api) - For accurate route distance and ETA calculations.
  - [OpenWeather API](https://openweathermap.org/api) - To fetch precise local weather data.

## 🚀 Getting Started

### Prerequisites
- Node.js (v18+)
- Python 3.9+
- Docker and Docker Compose (optional, for backend containerization)
- PostgreSQL (if running locally without Docker)

### Environment Variables setup
Create a `.env` file in the `backend/` directory with the following keys and values:
```env
OPENWEATHER_API_KEY=your_openweather_api_key
TOMTOM_API_KEY=your_tomtom_api_key
DATABASE_URL=postgresql://user:password@localhost:5432/routemonk
```

### 1. Running the Backend (API)

**Option A: Using Docker (Recommended)**
Provides an out-of-the-box FastAPI server alongside a ready-to-use Postgres database container.
```bash
cd backend
docker-compose up --build
```

**Option B: Local Standard Setup**
If utilizing a local Postgres server, ensure your `.env` `DATABASE_URL` is accurately configured.
```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --reload
```

### 2. Running the Frontend (UI)
Ensure your backend server is active before starting up the visual interface.
```bash
cd frontend
npm install
npm run dev
```

## 🌐 Core API Endpoints

- `GET /` - Root endpoint to check backend health status.
- `POST /optimize/` - Computes optimal route duration, fetches local weather data, applies optimization logic based on coordinates and perishability, and logs the result persistently.
- `GET /history/` - Retrieves a formatted array of past historical delivery calculations from the PostgreSQL database.

## 💡 Operating Workflow
1. The user interfaces with the Leaflet map to strictly assign a **start** and **end** destination.
2. The user inputs the targeted **perishability** score (1-10) of the cargo.
3. The frontend application dispatches coordinates to the FastAPI backend.
4. The backend securely triggers the **TomTom API** to evaluate the realistic travel duration.
5. Concurrently, the backend queries the **OpenWeather API** regarding the starting atmospheric conditions and temperature parameters.
6. A custom route score operates algorithmically over the calculated travel time correlated against item perishability.
7. Final analytics are permanently archived into the **PostgreSQL** database and instantaneously returned to the frontend display dashboard.
