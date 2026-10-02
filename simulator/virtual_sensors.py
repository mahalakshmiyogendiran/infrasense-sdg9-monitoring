import random
import time
import requests

API_URL = "http://127.0.0.1:8000/api/readings"

sensor_pairs = [
    {"asset_id": 1, "sensor_id": 1},
    {"asset_id": 2, "sensor_id": 3},
    {"asset_id": 3, "sensor_id": 4},
]

while True:
    for item in sensor_pairs:
        abnormal = random.random() < 0.20

        if abnormal:
            vibration = round(random.uniform(1.05, 1.50), 2)
            strain = round(random.uniform(80, 110), 2)
            tilt = round(random.uniform(4.10, 6.00), 2)
            temperature = round(random.uniform(40, 55), 2)
        else:
            vibration = round(random.uniform(0.20, 0.50), 2)
            strain = round(random.uniform(10, 40), 2)
            tilt = round(random.uniform(0.20, 1.80), 2)
            temperature = round(random.uniform(25, 38), 2)

        payload = {
            "asset_id": item["asset_id"],
            "sensor_id": item["sensor_id"],
            "vibration": vibration,
            "strain": strain,
            "tilt": tilt,
            "temperature": temperature,
        }

        try:
            response = requests.post(API_URL, json=payload)

            print(
                "Asset:",
                item["asset_id"],
                "| Status:",
                response.status_code,
                "| Data:",
                payload,
            )

        except requests.exceptions.ConnectionError:
            print("Backend connection failed. Is FastAPI running?")

        except Exception as error:
            print("Error:", error)

    print("-" * 60)
    time.sleep(5)