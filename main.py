from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="CityPulse API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/api/dashboard")
def dashboard():
    return {
        "city_score": 72,
        "status": "Moderate",
        "summary": "Heavy rain is affecting traffic and causing waterlogging in some areas.",
        "zones": [
            {
                "zone": "Vaishali Nagar",
                "score": 82,
                "status": "Good",
                "latitude": 26.9124,
                "longitude": 75.7873,
            },
            {
                "zone": "Malviya Nagar",
                "score": 58,
                "status": "Poor",
                "latitude": 26.8500,
                "longitude": 75.8100,
            },
            {
                "zone": "Mansarovar",
                "score": 68,
                "status": "Moderate",
                "latitude": 26.8500,
                "longitude": 75.7600,
            },
            {
                "zone": "C-Scheme",
                "score": 76,
                "status": "Good",
                "latitude": 26.9050,
                "longitude": 75.7950,
            },
            {
                "zone": "Jagatpura",
                "score": 61,
                "status": "Moderate",
                "latitude": 26.8400,
                "longitude": 75.8500,
            },
        ],
        "active_alerts": [
            {
                "id": 1,
                "title": "Heavy rain detected",
                "severity": "high",
                "description": "Rainfall is above the normal level.",
            },
            {
                "id": 2,
                "title": "Traffic congestion",
                "severity": "high",
                "description": "Traffic speed has dropped in affected areas.",
            },
            {
                "id": 3,
                "title": "Waterlogging reports",
                "severity": "medium",
                "description": "Multiple waterlogging reports have been received.",
            },
        ],
    }


@app.get("/api/alerts")
def alerts():
    return dashboard()["active_alerts"]


@app.get("/api/feeds/status")
def feeds_status():
    return {
        "weather": "live",
        "traffic": "live",
        "waterlogging": "simulated",
    }


@app.get("/")
def root():
    return {"message": "CityPulse API is running"}