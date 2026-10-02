from fastapi import FastAPI, Depends, HTTPException, WebSocket
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from .database import Base, engine, get_db
from .models import (
    User,
    Organization,
    Location,
    Asset,
    Sensor,
    SensorReading,
    Alert,
    MaintenanceRecord,
)
from .schemas import (
    LoginRequest,
    OrganizationCreate,
    LocationCreate,
    AssetCreate,
    SensorCreate,
    ReadingCreate,
    MaintenanceCreate,
)
from .alert_engine import evaluate_reading


Base.metadata.create_all(bind=engine)

app = FastAPI(title="InfraSense API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

connected_clients = []


@app.get("/")
def root():
    return {"message": "InfraSense API is running"}


@app.post("/api/auth/login")
def login(data: LoginRequest, db: Session = Depends(get_db)):
    user = (
        db.query(User)
        .filter(
            User.username == data.username,
            User.password == data.password,
        )
        .first()
    )

    if not user:
        raise HTTPException(
            status_code=401,
            detail="Invalid username or password",
        )

    return {
        "id": user.id,
        "name": user.name,
        "role": user.role,
    }


@app.post("/api/organizations")
def create_organization(
    data: OrganizationCreate,
    db: Session = Depends(get_db),
):
    organization = Organization(name=data.name)
    db.add(organization)
    db.commit()
    db.refresh(organization)
    return organization


@app.get("/api/organizations")
def get_organizations(db: Session = Depends(get_db)):
    return db.query(Organization).all()


@app.post("/api/locations")
def create_location(
    data: LocationCreate,
    db: Session = Depends(get_db),
):
    location = Location(**data.model_dump())
    db.add(location)
    db.commit()
    db.refresh(location)
    return location


@app.get("/api/locations")
def get_locations(db: Session = Depends(get_db)):
    return db.query(Location).all()


@app.post("/api/assets")
def create_asset(
    data: AssetCreate,
    db: Session = Depends(get_db),
):
    asset = Asset(**data.model_dump())
    db.add(asset)
    db.commit()
    db.refresh(asset)
    return asset


@app.get("/api/assets")
def get_assets(db: Session = Depends(get_db)):
    return db.query(Asset).all()


@app.get("/api/assets/{asset_id}")
def get_asset(
    asset_id: int,
    db: Session = Depends(get_db),
):
    asset = db.query(Asset).filter(Asset.id == asset_id).first()

    if not asset:
        raise HTTPException(
            status_code=404,
            detail="Asset not found",
        )

    return asset


@app.post("/api/sensors")
def create_sensor(
    data: SensorCreate,
    db: Session = Depends(get_db),
):
    sensor = Sensor(**data.model_dump())
    db.add(sensor)
    db.commit()
    db.refresh(sensor)
    return sensor


@app.get("/api/assets/{asset_id}/sensors")
def get_asset_sensors(
    asset_id: int,
    db: Session = Depends(get_db),
):
    return db.query(Sensor).filter(Sensor.asset_id == asset_id).all()


@app.post("/api/readings")
async def create_reading(
    data: ReadingCreate,
    db: Session = Depends(get_db),
):
    asset = db.query(Asset).filter(Asset.id == data.asset_id).first()

    if not asset:
        raise HTTPException(
            status_code=404,
            detail="Asset not found",
        )

    status, message = evaluate_reading(
        data.vibration,
        data.strain,
        data.tilt,
        data.temperature,
    )

    reading = SensorReading(
        sensor_id=data.sensor_id,
        asset_id=data.asset_id,
        vibration=data.vibration,
        strain=data.strain,
        tilt=data.tilt,
        temperature=data.temperature,
        status=status,
    )

    db.add(reading)
    db.commit()
    db.refresh(reading)

    asset.status = status

    if status != "SAFE":
        alert = Alert(
            asset_id=data.asset_id,
            reading_id=reading.id,
            severity=status,
            message=message,
        )
        db.add(alert)

    db.commit()

    payload = {
        "asset_id": data.asset_id,
        "sensor_id": data.sensor_id,
        "timestamp": reading.timestamp.isoformat(),
        "vibration": reading.vibration,
        "strain": reading.strain,
        "tilt": reading.tilt,
        "temperature": reading.temperature,
        "status": status,
        "message": message,
    }

    disconnected = []

    for client in connected_clients:
        try:
            await client.send_json(payload)
        except Exception:
            disconnected.append(client)

    for client in disconnected:
        if client in connected_clients:
            connected_clients.remove(client)

    return payload


@app.get("/api/assets/{asset_id}/readings")
def get_asset_readings(
    asset_id: int,
    db: Session = Depends(get_db),
):
    return (
        db.query(SensorReading)
        .filter(SensorReading.asset_id == asset_id)
        .order_by(SensorReading.timestamp.desc())
        .limit(100)
        .all()
    )


@app.get("/api/alerts")
def get_alerts(db: Session = Depends(get_db)):
    return (
        db.query(Alert)
        .order_by(Alert.created_at.desc())
        .limit(100)
        .all()
    )


@app.get("/api/dashboard/summary")
def dashboard_summary(db: Session = Depends(get_db)):
    assets = db.query(Asset).all()

    return {
        "total": len(assets),
        "safe": sum(asset.status == "SAFE" for asset in assets),
        "warning": sum(asset.status == "WARNING" for asset in assets),
        "critical": sum(asset.status == "CRITICAL" for asset in assets),
        "open_alerts": db.query(Alert)
        .filter(Alert.status == "OPEN")
        .count(),
    }


@app.post("/api/maintenance")
def create_maintenance(
    data: MaintenanceCreate,
    db: Session = Depends(get_db),
):
    record = MaintenanceRecord(**data.model_dump())
    db.add(record)
    db.commit()
    db.refresh(record)
    return record


@app.get("/api/maintenance")
def get_maintenance(db: Session = Depends(get_db)):
    return (
        db.query(MaintenanceRecord)
        .order_by(MaintenanceRecord.id.desc())
        .all()
    )


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    connected_clients.append(websocket)

    try:
        while True:
            await websocket.receive_text()
    except Exception:
        if websocket in connected_clients:
            connected_clients.remove(websocket)