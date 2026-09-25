import React, { useEffect } from 'react'
import { MapContainer, TileLayer, Marker, Popup } from 'react-leaflet'
import 'leaflet/dist/leaflet.css'
import L from 'leaflet'

// fix marker icon paths for leaflet in many bundlers
delete L.Icon.Default.prototype._getIconUrl
L.Icon.Default.mergeOptions({
  iconRetinaUrl: 'https://unpkg.com/leaflet@1.9.4/dist/images/marker-icon-2x.png',
  iconUrl: 'https://unpkg.com/leaflet@1.9.4/dist/images/marker-icon.png',
  shadowUrl: 'https://unpkg.com/leaflet@1.9.4/dist/images/marker-shadow.png',
})

export default function MapInteractive({ zones = [] }) {
  // default center over Jaipur-ish coords
  const center = [26.9124, 75.7873]

  return (
    <div style={{ width: '100%', height: '100%', borderRadius: 8, overflow: 'hidden' }}>
      <MapContainer
        center={center}
        zoom={11}
        scrollWheelZoom
        dragging
        zoomControl
        style={{ width: '100%', height: '100%' }}
      >
        <TileLayer
          attribution='&copy; OpenStreetMap contributors'
          url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
        />
        {zones?.map((z) => (
          <Marker key={z.zone} position={[z.latitude || center[0], z.longitude || center[1]]}>
            <Popup>
              <strong>{z.zone}</strong><br />Score: {z.score}<br />Status: {z.status}
            </Popup>
          </Marker>
        ))}
      </MapContainer>
    </div>
  )
}
