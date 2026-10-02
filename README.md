\# InfraSense



\## Smart IoT-Based Infrastructure Health Monitoring System



InfraSense is a software prototype for monitoring the health of bridges and buildings using simulated IoT sensor data.



The system generates vibration, strain, tilt and temperature readings, stores them in a database, evaluates threshold conditions and displays Safe, Warning or Critical statuses through a real-time dashboard.



\## SDG Alignment



This project supports Sustainable Development Goal 9:



\- Build resilient infrastructure

\- Promote innovation

\- Improve infrastructure monitoring

\- Support preventive maintenance

\- Encourage technology-based infrastructure management



\## Features



\- Multi-location infrastructure monitoring

\- Bridge and building asset management

\- Virtual IoT sensor simulator

\- Vibration, strain, tilt and temperature data

\- Safe, Warning and Critical status

\- Real-time dashboard updates

\- Historical sensor readings

\- Alert log

\- Infrastructure map

\- Role-based login

\- Maintenance tracking



\## Technology Stack



\- Frontend: React.js

\- Backend: Python FastAPI

\- Database: SQLite

\- Real-time communication: WebSocket

\- Charts: Recharts

\- Map: React Leaflet

\- Sensor simulation: Python



\## System Architecture



Virtual Sensor Simulator  

↓  

FastAPI Backend  

↓  

Threshold Alert Engine  

↓  

SQLite Database  

↓  

WebSocket  

↓  

React Dashboard



\## Run the Backend



```powershell

python -m venv .venv

.\\.venv\\Scripts\\Activate.ps1

pip install -r requirements.txt

uvicorn backend.main:app --reload --port 8000

```



\## Run the Frontend



```powershell

cd frontend

npm install

npm run dev

```



\## Run the Simulator



From the project root:



```powershell

python simulator/virtual\_sensors.py

```



\## Demo Accounts



```text

Admin:

Username: admin

Password: admin123



Engineer:

Username: engineer

Password: engineer123



Viewer:

Username: viewer

Password: viewer123

```



\## Important Note



This is a software prototype validated using simulated IoT telemetry. It provides early warnings and maintenance support. It does not certify whether a building or bridge is structurally safe or unsafe. Final structural decisions must be made by qualified civil or structural engineers.



\## Future Enhancements



\- Physical ESP32 sensor integration

\- MQTT communication

\- Email and SMS notifications

\- PostgreSQL or TimescaleDB

\- PDF report generation

\- Machine-learning anomaly detection

\- Professional engineering validation

