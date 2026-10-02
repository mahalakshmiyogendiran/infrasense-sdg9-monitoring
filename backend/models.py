from datetime import datetime

from sqlalchemy import (
    Column,
    Integer,
    String,
    Float,
    DateTime,
    ForeignKey,
)

from .database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    username = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    role = Column(String, default="viewer")


class Organization(Base):
    __tablename__ = "organizations"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)


class Location(Base):
    __tablename__ = "locations"

    id = Column(Integer, primary_key=True)
    organization_id = Column(Integer, ForeignKey("organizations.id"))
    city = Column(String, nullable=False)
    area = Column(String, nullable=False)
    address = Column(String, nullable=False)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)


class Asset(Base):
    __tablename__ = "assets"

    id = Column(Integer, primary_key=True)
    location_id = Column(Integer, ForeignKey("locations.id"))
    asset_code = Column(String, unique=True, nullable=False)
    name = Column(String, nullable=False)
    asset_type = Column(String, nullable=False)
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)
    status = Column(String, default="SAFE")


class Sensor(Base):
    __tablename__ = "sensors"

    id = Column(Integer, primary_key=True)
    asset_id = Column(Integer, ForeignKey("assets.id"))
    sensor_code = Column(String, unique=True, nullable=False)
    sensor_type = Column(String, nullable=False)
    status = Column(String, default="ACTIVE")


class SensorReading(Base):
    __tablename__ = "sensor_readings"

    id = Column(Integer, primary_key=True)
    sensor_id = Column(Integer, ForeignKey("sensors.id"))
    asset_id = Column(Integer, ForeignKey("assets.id"))
    timestamp = Column(DateTime, default=datetime.utcnow)
    vibration = Column(Float, nullable=False)
    strain = Column(Float, nullable=False)
    tilt = Column(Float, nullable=False)
    temperature = Column(Float, nullable=False)
    status = Column(String, nullable=False)


class Alert(Base):
    __tablename__ = "alerts"

    id = Column(Integer, primary_key=True)
    asset_id = Column(Integer, ForeignKey("assets.id"))
    reading_id = Column(Integer, ForeignKey("sensor_readings.id"))
    severity = Column(String, nullable=False)
    message = Column(String, nullable=False)
    status = Column(String, default="OPEN")
    created_at = Column(DateTime, default=datetime.utcnow)


class MaintenanceRecord(Base):
    __tablename__ = "maintenance_records"

    id = Column(Integer, primary_key=True)
    asset_id = Column(Integer, ForeignKey("assets.id"))
    alert_id = Column(Integer, ForeignKey("alerts.id"), nullable=True)
    engineer_name = Column(String, nullable=False)
    inspection_date = Column(DateTime, nullable=True)
    action_taken = Column(String, nullable=True)
    status = Column(String, default="ASSIGNED")
    remarks = Column(String, nullable=True)