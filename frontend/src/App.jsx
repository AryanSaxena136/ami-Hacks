import React, { useEffect, useState } from 'react'
import api from './services/api'
import MapInteractive from './MapInteractive'

function ZoneCard({ zone }) {
  return (
    <div className="zone-card">
      <h3>{zone.zone}</h3>
      <div>Score: <strong>{zone.score}</strong> ({zone.status})</div>
      <div>Lat: {zone.latitude ?? '—'} Lon: {zone.longitude ?? '—'}</div>
    </div>
  )
}

export default function App() {
  const [data, loading, error] = usePollingApi(5000)

  return (
    <div className="app-root mock-dashboard">
      <header className="topbar">
        <div className="title">CITYPULSE</div>
        <div className="status-pill">🟢 LIVE</div>
      </header>

      <main>
        <section className="health">
          <div className="health-left">
            <div className="label">CITY HEALTH</div>
            <div className="big-score">{data ? data.city_score : '—'}<span>/ 100</span></div>
            <div className="health-status">{data ? data.status.toUpperCase() : '—'}</div>
          </div>
          <div className="health-right">
              <div className="map" role="img" aria-label="Zone map">
                {/* small interactive map */}
                <MapInteractive zones={data?.zones} />
              </div>
            <div className="alerts-panel">
              <h4>ACTIVE ALERTS</h4>
              <ul>
                {(data?.active_alerts?.length ? data.active_alerts : [
                  { id: 1, title: 'Heavy rain detected', severity: 'high', description: '' },
                  { id: 2, title: 'Traffic congestion', severity: 'high', description: '' },
                  { id: 3, title: 'Waterlogging reports', severity: 'medium', description: '' },
                ]).map((a) => (
                  <li key={a.id} className={`alert ${a.severity}`}>⚠ {a.title}</li>
                ))}
              </ul>
            </div>
          </div>
        </section>

        <section className="what">
          <h3>WHAT'S HAPPENING?</h3>
          <p className="what-text">{data ? data.summary : 'Loading summary...'}</p>
        </section>
      </main>

      <footer className="mini-footer">CityPulse demo — live civic health dashboard</footer>
    </div>
  )
}

function usePollingApi(interval = 5000) {
  const [data, setData] = useState(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)

  useEffect(() => {
    let mounted = true
    async function fetchOnce() {
      try {
        const json = await api.getDashboard()
        if (mounted) {
          setData(json)
          setError(null)
          setLoading(false)
        }
      } catch (err) {
        if (mounted) {
          setError(err.message)
          setLoading(false)
        }
      }
    }
    fetchOnce()
    const id = setInterval(fetchOnce, interval)
    return () => {
      mounted = false
      clearInterval(id)
    }
  }, [interval])

  return [data, loading, error]
}

function MapSVG({ zones }) {
  // Simple static SVG of Jaipur-ish map with relative positions for zones.
  const viewBox = "0 0 300 200"
  const positions = {
    'Vaishali Nagar': [80, 60],
    'Malviya Nagar': [60, 90],
    'Mansarovar': [120, 110],
    'C-Scheme': [140, 70],
    'Jagatpura': [200, 140],
  }

  return (
    <svg viewBox={viewBox} className="map-svg">
      <rect x="0" y="0" width="300" height="200" rx="8" ry="8" fill="#041726" />
      {/* simple roads */}
      <g stroke="#08344a" strokeWidth="2" fill="none">
        <path d="M20 30 C100 20, 200 40, 280 30" />
        <path d="M40 160 C120 150, 180 170, 260 150" />
      </g>
      {/* zone markers */}
      <g>
        {Object.entries(positions).map(([name, [x, y]]) => {
          const zone = zones?.find((z) => z.zone === name)
          const score = zone?.score ?? 100
          const color = score >= 80 ? '#16a34a' : score >= 60 ? '#f59e0b' : '#dc2626'
          return (
            <g key={name} transform={`translate(${x},${y})`} className="zone-marker">
              <circle r="10" fill={color} opacity="0.95" />
              <text x="16" y="6" fontSize="10" fill="#e6eef8">{name}</text>
            </g>
          )
        })}
      </g>
    </svg>
  )
}
