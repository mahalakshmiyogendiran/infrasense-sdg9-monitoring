from pydantic import BaseModel


class LoginRequest(BaseModel):
    username: str
    password: str


class OrganizationCreate(BaseModel):
    name: str


class LocationCreate(BaseModel):
    organization_id: int
    city: str
    area: str
    address: str
    latitude: float
    longitude: float


class AssetCreate(BaseModel):
    location_id: int
    asset_code: str
    name: str
    asset_type: str
    latitude: float | None = None
    longitude: float | None = None


class SensorCreate(BaseModel):
    asset_id: int
    sensor_code: str
    sensor_type: str


class ReadingCreate(BaseModel):
    sensor_id: int
    asset_id: int
    vibration: float
    strain: float
    tilt: float
    temperature: float


class MaintenanceCreate(BaseModel):
    asset_id: int
    alert_id: int | None = None
    engineer_name: str
    action_taken: str | None = None
    status: str = "ASSIGNED"
    remarks: str | None = None