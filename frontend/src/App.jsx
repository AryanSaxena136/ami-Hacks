import React, { useEffect, useState } from 'react'
import api from './services/api'
import MapInteractive from './MapInteractive'

function FeedStatus({ name, status }) {
  const live = status === 'live'

  return (
    <div className="feed-item">
      <div>
        <span className={`feed-dot ${live ? 'live' : 'simulated'}`} />
        {name}
      </div>

      <span className={live ? 'feed-live' : 'feed-simulated'}>
        {live ? 'LIVE' : 'SIMULATED'}
      </span>
    </div>
  )
}

function ZoneCard({ zone }) {
  const score = Number(zone.score ?? 0)

  const statusClass =
    score >= 75 ? 'good' : score >= 60 ? 'moderate' : 'poor'

  return (
    <div className="zone-card">
      <div className="zone-top">
        <strong>{zone.zone}</strong>

        <span className={`zone-status ${statusClass}`}>
          {zone.status}
        </span>
      </div>

      <div className="zone-score">
        {score}
        <span>/100</span>
      </div>

      <div className="zone-bar">
        <div style={{ width: `${score}%` }} />
      </div>
    </div>
  )
}

export default function App() {
  const [data, loading, error] = usePollingApi(5000)

  const feeds = data?.feeds_status || {
    weather: 'live',
    traffic: 'live',
    waterlogging: 'simulated',
  }

  const zones = data?.zones || []

  return (
    <div className="app-root">
      <header className="topbar">
        <div>
          <div className="title">CITYPULSE</div>
          <div className="subtitle">
            LIVE CIVIC HEALTH INTELLIGENCE
          </div>
        </div>

        <div className="status-pill">
          <span className="live-dot" />
          LIVE MONITORING
        </div>
      </header>

      <main>
        {error && (
          <div className="error-banner">
            Backend connection issue: {error}
          </div>
        )}

        <section className="health">
          <div className="health-left">
            <div className="label">CITY HEALTH INDEX</div>
<div className="health-ring">
            <div className="big-score">
              {loading && !data ? '—' : data?.city_score ?? '—'}
              <span>/ 100</span>
            </div>
</div>
            <div className="health-status">
              <div className="health-signal">
  <span className="signal-dot" />
  LIVE CITY SIGNAL
  <span className="signal-time">UPDATING</span>
</div>
              {data?.status?.toUpperCase() || 'CALCULATING'}
            </div>

            <div className="score-caption">
              Composite civic health based on current city signals.
            </div>
          </div>

          <div className="health-right">
            <div className="map">
              <div className="map-legend">
  <div className="legend-title">LIVE ZONE DATA</div>

  <div className="legend-items">
    <span><i className="legend-dot good" /> Good</span>
    <span><i className="legend-dot moderate" /> Moderate</span>
    <span><i className="legend-dot poor" /> Poor</span>
  </div>
</div>
              <MapInteractive zones={zones} />
            </div>

            <div className="alerts-panel">
              <div className="panel-heading">
                <h4>ACTIVE ALERTS</h4>
                <span>{data?.active_alerts?.length || 0}</span>
              </div>

              <ul>
                {(data?.active_alerts || []).map((alert) => (
                  <li
                    key={alert.id}
                    className={`alert ${alert.severity}`}
                  >
                    <div className="alert-icon">
                      {alert.severity === 'high' ? '!' : '•'}
                    </div>
                    <span className="severity-badge">
  {alert.severity}
</span>

                    <div>
                      <strong>{alert.title}</strong>
                      <small>{alert.description}</small>
                    </div>
                  </li>
                ))}
              </ul>
            </div>
          </div>
        </section>

        <section className="intel-grid">
          <div className="intel-card">
            <div className="card-label">ANOMALY DETECTED</div>

            <div className="intel-title">
              Heavy rainfall spike
            </div>

            <p>
              Rainfall is currently above the expected level,
              increasing the likelihood of localized disruption.
            </p>

            <div className="signal">
              <span>Signal strength</span>
              <strong>HIGH</strong>
            </div>
          </div>

          <div className="intel-card">
            <div className="card-label">CORRELATION SIGNAL</div>

            <div className="intel-title">
              Rain ↔ Traffic ↔ Waterlogging
            </div>

            <p>
              Current data shows these signals moving together.
              This indicates a possible relationship, not confirmed causation.
            </p>

            <div className="signal">
              <span>Confidence</span>
              <strong>MEDIUM</strong>
            </div>
          </div>

          <div className="intel-card">
            <div className="card-label">FEED HEALTH</div>

            <FeedStatus name="Weather" status={feeds.weather} />
            <FeedStatus name="Traffic" status={feeds.traffic} />
            <FeedStatus
              name="Waterlogging"
              status={feeds.waterlogging}
            />
          </div>
        </section>

        <section className="what">
          <div className="what-header">
            <div>
              <h3>WHAT'S HAPPENING?</h3>
              <span>AI-READY CIVIC SUMMARY</span>
            </div>

            <div className="pulse-bars">
              <i />
              <i />
              <i />
              <i />
            </div>
          </div>

          <p className="what-text">
            {loading && !data
              ? 'Analyzing incoming civic signals...'
              : data?.summary ||
                'No major civic disruption detected at this time.'}
          </p>
        </section>

        <section className="zones-section">
          <div className="section-heading">
            <div>
              <h3>ZONE HEALTH</h3>
              <span>LOCALIZED CIVIC CONDITIONS</span>
            </div>

            <span className="refresh-label">
              Updates every 5 sec
            </span>
          </div>

          <div className="zones-grid">
            {zones.map((zone) => (
              <ZoneCard key={zone.zone} zone={zone} />
            ))}
          </div>
        </section>
      </main>

      <footer className="mini-footer">
        CITYPULSE • LIVE CIVIC HEALTH DASHBOARD • DEMO MODE
      </footer>
    </div>
  )
}
function usePollingApi(interval = 5000) {
  const demoData = {
    city_score: 72,
    status: 'Moderate',

    summary:
      'Heavy rain is affecting traffic and causing waterlogging in some areas.',

    feeds_status: {
      weather: 'live',
      traffic: 'live',
      waterlogging: 'simulated',
    },

    zones: [
      {
        zone: 'Vaishali Nagar',
        score: 82,
        status: 'Good',
        latitude: 26.9124,
        longitude: 75.7873,
      },
      {
        zone: 'Malviya Nagar',
        score: 58,
        status: 'Poor',
        latitude: 26.8500,
        longitude: 75.8100,
      },
      {
        zone: 'Mansarovar',
        score: 68,
        status: 'Moderate',
        latitude: 26.8500,
        longitude: 75.7600,
      },
      {
        zone: 'C-Scheme',
        score: 76,
        status: 'Good',
        latitude: 26.9050,
        longitude: 75.7950,
      },
      {
        zone: 'Jagatpura',
        score: 61,
        status: 'Moderate',
        latitude: 26.8400,
        longitude: 75.8500,
      },
    ],

    active_alerts: [
      {
        id: 1,
        title: 'Heavy rain detected',
        severity: 'high',
        description: 'Rainfall is above the normal level.',
      },
      {
        id: 2,
        title: 'Traffic congestion',
        severity: 'high',
        description: 'Traffic speed has dropped in affected areas.',
      },
      {
        id: 3,
        title: 'Waterlogging reports',
        severity: 'medium',
        description: 'Multiple waterlogging reports have been received.',
      },
    ],
  }

  const [data, setData] = useState(demoData)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)

  useEffect(() => {
    let mounted = true

    async function fetchOnce() {
      try {
        const json = await api.getDashboard()

        if (mounted) {
          const merged = {
            ...demoData,
            ...json,
            city_score: demoData.city_score,
            status: demoData.status,
            summary: demoData.summary,
            feeds_status: demoData.feeds_status,
            zones: demoData.zones,
            active_alerts: demoData.active_alerts,
          }

          setData(merged)
          setError(null)
        }
      } catch {
        if (mounted) {
          setData(demoData)
          setError(null)
        }
      } finally {
        if (mounted) {
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
