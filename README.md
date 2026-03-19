steps on how to set it up:

1. sudo bash deploy.sh

The server, sensors and hadoop should be running.

Links to see activated sensors (retrieve):
    http://127.0.0.1:8080/retrieve?sensor_id=1&start_time=2020-01-01%2000:00:00&end_time=2030-12-31%2023:59:59
    http://127.0.0.1:8080/retrieve?sensor_id=2&start_time=2020-01-01%2000:00:00&end_time=2030-12-31%2023:59:59
    http://127.0.0.1:8080/retrieve?sensor_id=3&start_time=2020-01-01%2000:00:00&end_time=2030-12-31%2023:59:59
    http://127.0.0.1:8080/retrieve?sensor_id=4&start_time=2020-01-01%2000:00:00&end_time=2030-12-31%2023:59:59

Add data (store):
    http://localhost:8080/store?sensor_id=1&latitude=45.0&longitude=9.0&type=Temperature%20Sensor&value=23.5&timestamp=2025-03-19%2010:00:00

Download .txt (fetch):
    http://localhost:8080/fetch?type=Temperature%20Sensor

Types of default messurement types:
    Temperature Sensor | Temperature%20Sensor
    Pressure Sensor | Pressure%20Sensor
    Air Quality Sensor | Air%20Quality%20Sensor
    CO2 Sensor | CO2%20Sensor
    
2. run run_analysis.sh LATITUDE LONGITUDE DISTANCE TYPE
    LATITUDE, LONGITUDE, DISTANCE and TYPE are adjustable parameters, the default types are listed above. If no parameter is set, some default values will be used
