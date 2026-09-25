# CityPulse

CityPulse is a live civic intelligence dashboard that tracks city health across zones using weather, traffic, and incident signals. It combines real-time monitoring, anomaly detection, and AI-ready summarization into one operational dashboard for city agencies and public-safety monitoring.

## Problem it solves

City systems often generate fragmented signals across different feeds, making it hard to understand whether conditions are improving, worsening, or becoming dangerous. CityPulse brings these signals together into a single city health view, highlights risky zones, and explains what is happening in plain language.

## Key features

- City health index across multiple zones
- Live weather, traffic, and incident monitoring
- Alert generation for high-risk civic conditions
- Zone-level scoring and localized status updates
- Correlation analysis between rainfall, congestion, and incidents
- AI-ready summary generation for operators
- Responsive dashboard UI for demo and hackathon use

## Tech stack

- Python 3.12+
- FastAPI
- SQLAlchemy
- SQLite
- React + Vite
- Tailwind CSS
- LangChain Groq / OpenAI-compatible LLM support
- pytest

## Project structure

```text
ami-Hacks/
├── backend/
│   ├── app/
│   │   ├── core/
│   │   ├── feeds/
│   │   ├── models/
│   │   ├── routes/
│   │   ├── schemas/
│   │   └── services/
│   ├── tests/
│   ├── .env
│   ├── README.md
│   ├── requirements.txt
│   └── citypulse.db
├── frontend/
│   ├── src/
│   ├── package.json
│   ├── vite.config.*
│   └── index.html
├── .gitignore
├── pyproject.toml
├── README.md
└── main.py
```

## Quick start

### 1) Backend setup

```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Create a `.env` file in the backend folder if needed and add your API values, for example:

```env
GROK_API_KEY=your_key_here
GROK_MODEL=grok-2-latest
GROK_BASE_URL=https://api.x.ai/v1
```

Then run:

```bash
cd backend
source .venv/bin/activate
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

The backend will be available at:
- http://localhost:8000
- http://localhost:8000/docs

### 2) Frontend setup

```bash
cd frontend
npm install
npm run dev -- --host 0.0.0.0
```

The frontend will run at:
- http://localhost:5173

## API highlights

- GET /api/health
- POST /api/ingest/simulate
- GET /api/data/latest
- GET /api/alerts
- GET /api/dashboard

## Demo behavior

The app is designed as a hackathon-ready MVP with simulated civic streams. It demonstrates how a city operations dashboard can combine live signal feeds, anomaly detection, and natural-language summaries without requiring a production data pipeline.

## Why this is unique

CityPulse is not just a weather dashboard or a basic map. It is built around city operations intelligence:

- health is scored by zone
- anomalies are identified across signals
- correlations explain patterns in a human-readable way
- summaries translate raw data into actionable insight for operators

## Future scope

- connect to live municipal APIs
- add authenticated admin workflows
- integrate GIS layers and real road/utility data
- improve the AI summary layer with full operator actions and recommendations
- expand to multi-city monitoring and alert escalation

## License

This project is licensed under the MIT License.
