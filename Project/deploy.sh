#!/bin/bash

echo "=== 1. Limpiando contenedores antiguos ==="
docker-compose down
# Ahora borramos los 4 posibles sensores anteriores
docker rm -f iot_server sensor_1 sensor_2 sensor_3 sensor_4 2>/dev/null

echo "=== 2. Borrando red e imágenes antiguas ==="
docker network rm iot_network 2>/dev/null
docker rmi -f iot_server_img virtual_sensor_img 2>/dev/null

echo "=== 3. Creando la nueva red ==="
docker network create iot_network

echo "=== 4. Construyendo las nuevas imágenes ==="
docker build -t iot_server_img -f docker/Dockerfile .
docker build -t virtual_sensor_img -f docker/Dockerfile.sensor .

echo "=== 5. Levantando el clúster distribuido Hadoop (Grado 5) ==="
docker-compose up -d

echo "=== 6. Iniciando el servidor web (Flask + SQLite) ==="
sleep 3
docker run -d --network iot_network --name iot_server -p 8080:8080 iot_server_img

echo "=== 7. Iniciando los 4 sensores virtuales múltiples ==="

# Sensor 1: Temperatura y Presión
docker run -d --network iot_network -e SENSOR_ID=1 -e LAT=45.0 -e LON=9.0 \
  -e TYPE="Temperature Sensor,Pressure Sensor" \
  --name sensor_1 virtual_sensor_img

# Sensor 2: Calidad de Aire y CO2
docker run -d --network iot_network -e SENSOR_ID=2 -e LAT=45.5 -e LON=9.5 \
  -e TYPE="Air Quality Sensor,CO2 Sensor" \
  --name sensor_2 virtual_sensor_img

# Sensor 3: Temperatura y Calidad de Aire
docker run -d --network iot_network -e SENSOR_ID=3 -e LAT=46.0 -e LON=10.0 \
  -e TYPE="Temperature Sensor,Air Quality Sensor" \
  --name sensor_3 virtual_sensor_img

# Sensor 4: Los 4 tipos a la vez
docker run -d --network iot_network -e SENSOR_ID=4 -e LAT=44.0 -e LON=8.0 \
  -e TYPE="Temperature Sensor,Pressure Sensor,Air Quality Sensor,CO2 Sensor" \
  --name sensor_4 virtual_sensor_img

echo ""
echo "✅ ¡Limpieza y despliegue completados con éxito!"
echo "➡️  El servidor está corriendo en: http://localhost:8080"
echo "➡️  Los 4 sensores ya están enviando múltiples datos simultáneamente."
