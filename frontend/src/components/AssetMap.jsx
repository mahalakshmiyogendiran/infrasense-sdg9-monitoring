import {
  MapContainer,
  Marker,
  Popup,
  TileLayer,
} from "react-leaflet";

import "leaflet/dist/leaflet.css";

function AssetMap({ assets }) {
  return (
    <MapContainer
      center={[13.0827, 80.2707]}
      zoom={11}
      style={{
        height: "400px",
        width: "100%",
        borderRadius: "12px",
      }}
    >
      <TileLayer
        attribution="&copy; OpenStreetMap contributors"
        url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
      />

      {assets.map((asset) => {
        if (
          asset.latitude === null ||
          asset.longitude === null
        ) {
          return null;
        }

        return (
          <Marker
            key={asset.id}
            position={[
              asset.latitude,
              asset.longitude,
            ]}
          >
            <Popup>
              <strong>{asset.name}</strong>
              <br />
              Code: {asset.asset_code}
              <br />
              Type: {asset.asset_type}
              <br />
              Status: {asset.status}
            </Popup>
          </Marker>
        );
      })}
    </MapContainer>
  );
}

export default AssetMap;