import os
import time
import random
import urllib.request
import urllib.parse
from datetime import datetime, timezone

SENSOR_ID = os.environ.get('SENSOR_ID', '1')
LATITUDE = os.environ.get('LAT', '0.0')
LONGITUDE = os.environ.get('LON', '0.0')
SENSOR_TYPE = os.environ.get('TYPE', 'Temperature Sensor')
SERVER_URL = os.environ.get('SERVER_URL', 'http://iot_server:8080/store')

def generate_value(sensor_type):
    if sensor_type == 'Temperature Sensor':
        return round(random.uniform(-10.0, 40.0), 2) # °C
    elif sensor_type == 'Pressure Sensor':
        return round(random.uniform(980.0, 1050.0), 2) # hPa
    elif sensor_type == 'Air Quality Sensor':
        return round(random.uniform(0.0, 150.0), 2) # PM10
    elif sensor_type == 'CO2 Sensor':
        return round(random.uniform(400.0, 2000.0), 2) # ppm
    return round(random.uniform(0.0, 100.0), 2)

print(f"Starting Sensor {SENSOR_ID} ({SENSOR_TYPE}) at Lat: {LATITUDE}, Lon: {LONGITUDE}")

for _ in range(10)
    try:
        value = generate_value(SENSOR_TYPE)
        timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S")

        params = {
            'sensor_id': SENSOR_ID,
            'latitude': LATITUDE,
            'longitude': LONGITUDE,
            'type': SENSOR_TYPE,
            'value': value,
            'timestamp': timestamp
        }
        
        query_string = urllib.parse.urlencode(params)
        full_url = f"{SERVER_URL}?{query_string}"

        with urllib.request.urlopen(full_url) as response:
            response.read()
            print(f"[{timestamp}] Sent {value} for {SENSOR_TYPE}")
            
    except Exception as e:
        print(f"Error connecting to server: {e}")
        
    time.sleep(15)
