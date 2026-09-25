const BASE = import.meta.env.VITE_API_BASE_URL || 'http://127.0.0.1:8000'

async function getJson(path) {
  const res = await fetch(`${BASE}${path}`)
  if (!res.ok) throw new Error(`HTTP ${res.status}`)
  return res.json()
}

export function getDashboard() { return getJson('/api/dashboard') }
export function getAlerts() { return getJson('/api/alerts') }
export function getFeedsStatus() { return getJson('/api/feeds/status') }

// For development: mock endpoints
export async function getMockDashboard() {
  return fetch('/mock/dashboard.json').then(r => r.json())
}

export default { getDashboard, getAlerts, getFeedsStatus }
