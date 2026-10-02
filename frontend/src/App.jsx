import { useEffect, useState } from "react";
import "./App.css";

import Login from "./components/Login";
import AssetMap from "./components/AssetMap";
import SensorChart from "./components/SensorChart";

const API_URL = "http://127.0.0.1:8000";

function App() {
  const [user, setUser] = useState(null);
  const [assets, setAssets] = useState([]);
  const [alerts, setAlerts] = useState([]);
  const [summary, setSummary] = useState({
    total: 0,
    safe: 0,
    warning: 0,
    critical: 0,
    open_alerts: 0,
  });

  const [selectedAsset, setSelectedAsset] = useState(null);
  const [readings, setReadings] = useState([]);
  const [liveReading, setLiveReading] = useState(null);

  async function loadDashboard() {
    try {
      const [
        assetsResponse,
        alertsResponse,
        summaryResponse,
      ] = await Promise.all([
        fetch(`${API_URL}/api/assets`),
        fetch(`${API_URL}/api/alerts`),
        fetch(`${API_URL}/api/dashboard/summary`),
      ]);

      const assetsData = await assetsResponse.json();
      const alertsData = await alertsResponse.json();
      const summaryData = await summaryResponse.json();

      setAssets(assetsData);
      setAlerts(alertsData);
      setSummary(summaryData);

      setSelectedAsset((currentAsset) => {
        if (currentAsset) {
          return (
            assetsData.find(
              (asset) => asset.id === currentAsset.id
            ) || currentAsset
          );
        }

        return assetsData.length > 0
          ? assetsData[0]
          : null;
      });
    } catch (error) {
      console.error("Dashboard loading error:", error);
    }
  }

  async function loadReadings(assetId) {
    try {
      const response = await fetch(
        `${API_URL}/api/assets/${assetId}/readings`
      );

      const data = await response.json();
      setReadings(data.reverse());
    } catch (error) {
      console.error("Reading loading error:", error);
    }
  }

  useEffect(() => {
    if (!user) {
      return;
    }

    loadDashboard();

    const refreshTimer = setInterval(() => {
      loadDashboard();
    }, 5000);

    const socket = new WebSocket(
      "ws://127.0.0.1:8000/ws"
    );

    socket.onopen = () => {
      socket.send("dashboard-connected");
    };

    socket.onmessage = (event) => {
      const data = JSON.parse(event.data);

      setLiveReading(data);

      if (
        selectedAsset &&
        data.asset_id === selectedAsset.id
      ) {
        setReadings((oldReadings) => [
          ...oldReadings.slice(-49),
          data,
        ]);
      }
    };

    socket.onerror = () => {
      console.log("WebSocket connection error");
    };

    return () => {
      clearInterval(refreshTimer);
      socket.close();
    };
  }, [user, selectedAsset]);

  useEffect(() => {
    if (user && selectedAsset) {
      loadReadings(selectedAsset.id);
    }
  }, [user, selectedAsset]);

  function getStatusClass(status) {
    return String(status || "SAFE").toLowerCase();
  }

  if (!user) {
    return <Login onLogin={setUser} />;
  }

  return (
    <div className="app">
      <header className="topbar">
        <div>
          <h1>InfraSense</h1>
          <p>
            Smart Infrastructure Health Monitoring System
          </p>
        </div>

        <div className="header-right">
          <div className="live-indicator">
            <span>●</span> LIVE MONITORING
          </div>

          <div className="user-area">
            <span>
              {user.name} ({user.role})
            </span>

            <button onClick={() => setUser(null)}>
              Logout
            </button>
          </div>
        </div>
      </header>

      <section className="summary-grid">
        <div className="summary-card">
          <span>Total Assets</span>
          <strong>{summary.total}</strong>
        </div>

        <div className="summary-card safe-card">
          <span>Safe</span>
          <strong>{summary.safe}</strong>
        </div>

        <div className="summary-card warning-card">
          <span>Warning</span>
          <strong>{summary.warning}</strong>
        </div>

        <div className="summary-card critical-card">
          <span>Critical</span>
          <strong>{summary.critical}</strong>
        </div>

        <div className="summary-card">
          <span>Open Alerts</span>
          <strong>{summary.open_alerts}</strong>
        </div>
      </section>

      <main className="dashboard-layout">
        <section className="panel asset-panel">
          <h2>Infrastructure Assets</h2>

          {assets.length === 0 && (
            <p>No infrastructure assets found.</p>
          )}

          {assets.map((asset) => (
            <button
              key={asset.id}
              className={`asset-row ${
                selectedAsset?.id === asset.id
                  ? "selected"
                  : ""
              }`}
              onClick={() => setSelectedAsset(asset)}
            >
              <div>
                <strong>{asset.name}</strong>

                <small>
                  {asset.asset_code} · {asset.asset_type}
                </small>
              </div>

              <span
                className={`status ${getStatusClass(
                  asset.status
                )}`}
              >
                {asset.status}
              </span>
            </button>
          ))}
        </section>

        <section className="panel readings-panel">
          <h2>
            {selectedAsset
              ? selectedAsset.name
              : "Select an infrastructure asset"}
          </h2>

          {liveReading &&
            selectedAsset &&
            liveReading.asset_id === selectedAsset.id && (
              <div
                className={`live-reading ${getStatusClass(
                  liveReading.status
                )}`}
              >
                <h3>Latest Live Reading</h3>

                <p>
                  Vibration:{" "}
                  <b>{liveReading.vibration}</b>
                </p>

                <p>
                  Strain: <b>{liveReading.strain}</b>
                </p>

                <p>
                  Tilt: <b>{liveReading.tilt}</b>
                </p>

                <p>
                  Temperature:{" "}
                  <b>{liveReading.temperature}</b>
                </p>

                <strong>{liveReading.status}</strong>
              </div>
            )}

          <h3>Live Sensor Charts</h3>
          <SensorChart readings={readings} />

          <h3>Historical Readings</h3>

          <div className="table-wrapper">
            <table>
              <thead>
                <tr>
                  <th>Time</th>
                  <th>Vibration</th>
                  <th>Strain</th>
                  <th>Tilt</th>
                  <th>Temperature</th>
                  <th>Status</th>
                </tr>
              </thead>

              <tbody>
                {readings.map((reading) => (
                  <tr
                    key={
                      reading.id ||
                      `${reading.timestamp}-${reading.vibration}`
                    }
                  >
                    <td>
                      {new Date(
                        reading.timestamp
                      ).toLocaleTimeString()}
                    </td>

                    <td>{reading.vibration}</td>
                    <td>{reading.strain}</td>
                    <td>{reading.tilt}</td>
                    <td>{reading.temperature}</td>

                    <td>
                      <span
                        className={`status ${getStatusClass(
                          reading.status
                        )}`}
                      >
                        {reading.status}
                      </span>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </section>

        <section className="panel alert-panel">
          <h2>Alert Log</h2>

          {alerts.length === 0 && (
            <p>No alerts available.</p>
          )}

          {alerts.map((alert) => (
            <div className="alert-item" key={alert.id}>
              <span
                className={`status ${getStatusClass(
                  alert.severity
                )}`}
              >
                {alert.severity}
              </span>

              <p>{alert.message}</p>

              <small>
                {new Date(
                  alert.created_at
                ).toLocaleString()}
              </small>
            </div>
          ))}
        </section>
      </main>

      <section className="panel map-panel">
        <h2>Infrastructure Map</h2>
        <AssetMap assets={assets} />
      </section>
    </div>
  );
}

export default App;