import os
import time
import random
import urllib.request
import urllib.parse
from datetime import datetime, timezone

SENSOR_ID = os.environ.get('SENSOR_ID', '1')
LATITUDE = os.environ.get('LAT', '0.0')
LONGITUDE = os.environ.get('LON', '0.0')
SERVER_URL = os.environ.get('SERVER_URL', 'http://iot_server:8080/store')

SENSOR_TYPES_ENV = os.environ.get('TYPE', 'Temperature Sensor')
SENSOR_TYPES = [t.strip() for t in SENSOR_TYPES_ENV.split(',')]

def generate_value(sensor_type):
    if sensor_type == 'Temperature Sensor':
        return round(random.uniform(-10.0, 40.0), 2)
    elif sensor_type == 'Pressure Sensor':
        return round(random.uniform(980.0, 1050.0), 2)
    elif sensor_type == 'Air Quality Sensor':
        return round(random.uniform(0.0, 150.0), 2)
    elif sensor_type == 'CO2 Sensor':
        return round(random.uniform(400.0, 2000.0), 2)
    return round(random.uniform(0.0, 100.0), 2)

# send the data
for _ in range(15):
    try:
        timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S")

        for s_type in SENSOR_TYPES:
            value = generate_value(s_type)
            params = {
                'sensor_id': SENSOR_ID,
                'latitude': LATITUDE,
                'longitude': LONGITUDE,
                'type': s_type,
                'value': value,
                'timestamp': timestamp
            }
            
            query_string = urllib.parse.urlencode(params)
            full_url = f"{SERVER_URL}?{query_string}"

            with urllib.request.urlopen(full_url) as response:
                response.read()
                print(f"[{timestamp}] Sent {value} for {s_type} (Sensor {SENSOR_ID})")
                
    except Exception as e:
        print(f"Error connecting to server: {e}")
        
    time.sleep(15)
