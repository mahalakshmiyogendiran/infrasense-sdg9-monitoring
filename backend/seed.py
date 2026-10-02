from .database import Base, SessionLocal, engine
from .models import (
    Asset,
    Location,
    Organization,
    Sensor,
    User,
)

Base.metadata.create_all(bind=engine)

db = SessionLocal()

try:
    # Users
    users = db.query(User).all()

    if not users:
        db.add_all([
            User(
                name="System Admin",
                username="admin",
                password="admin123",
                role="admin",
            ),
            User(
                name="Maintenance Engineer",
                username="engineer",
                password="engineer123",
                role="engineer",
            ),
            User(
                name="Dashboard Viewer",
                username="viewer",
                password="viewer123",
                role="viewer",
            ),
        ])

        db.commit()

    # Organization
    organization = db.query(Organization).first()

    if not organization:
        organization = Organization(
            name="Chennai Infrastructure Authority"
        )

        db.add(organization)
        db.commit()
        db.refresh(organization)

    # Locations
    locations = db.query(Location).all()

    if not locations:
        location1 = Location(
            organization_id=organization.id,
            city="Chennai",
            area="Anna Nagar",
            address="Anna Nagar Main Road",
            latitude=13.0850,
            longitude=80.2101,
        )

        location2 = Location(
            organization_id=organization.id,
            city="Chennai",
            area="Tambaram",
            address="Tambaram Main Road",
            latitude=12.9249,
            longitude=80.1000,
        )

        db.add_all([location1, location2])
        db.commit()
        db.refresh(location1)
        db.refresh(location2)
    else:
        location1 = locations[0]

        if len(locations) > 1:
            location2 = locations[1]
        else:
            location2 = locations[0]

    # Assets
    assets = db.query(Asset).all()

    if not assets:
        asset1 = Asset(
            location_id=location1.id,
            asset_code="BR-001",
            name="Anna Nagar Bridge",
            asset_type="Bridge",
            latitude=13.0850,
            longitude=80.2101,
            status="SAFE",
        )

        asset2 = Asset(
            location_id=location1.id,
            asset_code="BL-001",
            name="Anna Nagar Public Building",
            asset_type="Building",
            latitude=13.0870,
            longitude=80.2120,
            status="SAFE",
        )

        asset3 = Asset(
            location_id=location2.id,
            asset_code="BR-002",
            name="Tambaram Bridge",
            asset_type="Bridge",
            latitude=12.9249,
            longitude=80.1000,
            status="SAFE",
        )

        db.add_all([asset1, asset2, asset3])
        db.commit()

        db.refresh(asset1)
        db.refresh(asset2)
        db.refresh(asset3)
    else:
        asset1 = assets[0]

        if len(assets) > 1:
            asset2 = assets[1]
        else:
            asset2 = assets[0]

        if len(assets) > 2:
            asset3 = assets[2]
        else:
            asset3 = assets[0]

    # Sensors
    sensors = db.query(Sensor).all()

    if not sensors:
        db.add_all([
            Sensor(
                asset_id=asset1.id,
                sensor_code="BR-001-VIB",
                sensor_type="Vibration",
                status="ACTIVE",
            ),
            Sensor(
                asset_id=asset1.id,
                sensor_code="BR-001-TILT",
                sensor_type="Tilt",
                status="ACTIVE",
            ),
            Sensor(
                asset_id=asset2.id,
                sensor_code="BL-001-STRAIN",
                sensor_type="Strain",
                status="ACTIVE",
            ),
            Sensor(
                asset_id=asset3.id,
                sensor_code="BR-002-VIB",
                sensor_type="Vibration",
                status="ACTIVE",
            ),
            Sensor(
                asset_id=asset3.id,
                sensor_code="BR-002-TILT",
                sensor_type="Tilt",
                status="ACTIVE",
            ),
        ])

        db.commit()

    print("Seed data created successfully.")
    print("Users: admin, engineer, viewer")
    print("Assets: BR-001, BL-001, BR-002")
    print("Sensors created successfully.")

finally:
    db.close()